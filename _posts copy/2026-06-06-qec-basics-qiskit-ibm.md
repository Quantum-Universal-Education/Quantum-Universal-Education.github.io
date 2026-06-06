---
title: "Protecting Quantum Information: A Hands-On Introduction to Quantum Error Correction with Qiskit"
categories:
  - Blog
tags:
  - tutorial
  - quantum-error-correction
  - Qiskit
  - jupyter notebook
  - quantum computing
  - IBM Quantum
  - qiskit-aer
author:
  - Quantum Universal Education Contributors
  - Curate Section
---

Quantum computers store information in physical systems: superconducting circuits, ions, photons, atoms, spins, and other devices. Physical systems are never perfectly isolated. A qubit can be changed by a stray interaction with its environment, an imperfect gate, a measurement error, or a short loss of coherence.

This tutorial introduces the first idea behind quantum error correction (QEC): protect one logical bit of quantum information by spreading it across several physical qubits and decoding the result. We will use a three-qubit repetition code because it is small enough to draw, simulate, and run as a tiny optional IBM hardware experiment.

The goal is not to build a full fault-tolerant quantum computer. The goal is to learn the basic pattern:

1. encode information into more qubits;
2. add a simple noise model;
3. decode measurement results;
4. compare physical and logical error rates.

The full notebook is in `notebooks/qec_basics_qiskit_ibm.ipynb`. The simulator results below were generated from that notebook with Qiskit Aer. No IBM hardware results are included in this post.

![Physical error rate versus decoded logical error rate](/assets/images/qec-basics/qec_physical_vs_logical.png)

## Why errors matter

Classical computers already fight errors. A bit stored in memory can flip from `0` to `1`, or a message sent across a network can lose a symbol. Classical error correction handles this by adding extra information. For example, sending `000` instead of one `0` lets a receiver correct one flipped bit by majority vote.

Qubits are more delicate than classical bits. A qubit can have bit-flip errors, phase-flip errors, coherent over-rotations, measurement errors, crosstalk from nearby qubits, and decoherence. Also, an unknown quantum state cannot be copied perfectly. This is the no-cloning theorem, and it means quantum error correction cannot simply make backup copies of an arbitrary qubit.

The QEC idea is different from copying. We encode one **logical qubit** into several **physical qubits**. Then we learn information about the error without directly measuring the protected logical state. In large QEC codes, that error information is called a **syndrome**. In this first tutorial, our syndrome will be simple: after measurement, we ask which value appears in the majority.

## Dependencies

Install the tutorial dependencies with:

```bash
python -m pip install -r requirements-qec-tutorial.txt
```

The simulator part uses:

- `qiskit`
- `qiskit-aer`
- `numpy`
- `matplotlib`
- `pandas`
- `nbconvert` and `ipykernel` for notebook execution/export
- `pylatexenc` for circuit drawings

Use your preferred Jupyter front end, such as JupyterLab or Notebook, to open the notebook interactively.

The optional hardware section uses `qiskit-ibm-runtime`. It is disabled by default and does not need IBM credentials to run the simulator notebook.

To run the notebook locally:

```bash
python -m venv .venv-qec
source .venv-qec/bin/activate
python -m pip install -r requirements-qec-tutorial.txt
python -m pip install jupyterlab
jupyter lab notebooks/qec_basics_qiskit_ibm.ipynb
```

## A tiny code: the three-qubit repetition code

The three-qubit bit-flip repetition code stores one logical bit in three physical qubits:

$$
|0_L\rangle = |000\rangle, \qquad |1_L\rangle = |111\rangle.
$$

Here the subscript $L$ means "logical". The three physical qubits are the actual qubits in the circuit. The logical qubit is the encoded information we care about.

If one physical qubit flips, then `000` might become `001`, `010`, or `100`. A majority vote still decodes this as logical `0`. If two or three physical qubits flip, the majority vote gives the wrong logical value.

For independent bit flips with probability $p$ on each physical qubit:

- an unencoded bit fails with probability $p$;
- a three-qubit majority-vote code fails when two or three qubits flip:

$$
P_{\text{fail},3}(p) = 3p^2(1-p) + p^3 = 3p^2 - 2p^3.
$$

This code helps when $p < 1/2$. It also uses more qubits, and a real device would add noise during the extra gates. This toy model is useful because the main idea can be checked exactly.

```python
def repetition_logical_failure_probability(n: int, p: float) -> float:
    """Return the majority-vote failure probability for an odd repetition code."""
    if n % 2 != 1 or n < 1:
        raise ValueError("n must be a positive odd integer")
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be between 0 and 1")

    first_bad_weight = (n + 1) // 2
    return sum(
        math.comb(n, k) * (p**k) * ((1 - p) ** (n - k))
        for k in range(first_bad_weight, n + 1)
    )
```

## Build the circuits

The first circuit stores a single physical bit for one memory step. The second circuit stores the same logical value using three physical qubits. The `id` gates mark the memory step. Our noise model attaches bit-flip errors to those `id` gates, so the encoding and measurement are noiseless in the first simulation.

![Unencoded one-qubit memory circuit](/assets/images/qec-basics/qec_unencoded_circuit.png)

![Three-qubit repetition-code memory circuit](/assets/images/qec-basics/qec_repetition_circuit.png)

```python
from qiskit import QuantumCircuit


def make_unencoded_memory_circuit(initial_state: int = 0, memory_gates: int = 1) -> QuantumCircuit:
    """Create a one-qubit memory circuit measured in the computational basis."""
    if initial_state not in (0, 1):
        raise ValueError("initial_state must be 0 or 1")
    if memory_gates < 1:
        raise ValueError("memory_gates must be at least 1")

    circuit = QuantumCircuit(1, 1, name=f"unencoded_{initial_state}")
    if initial_state == 1:
        circuit.x(0)
    circuit.barrier()
    for _ in range(memory_gates):
        circuit.id(0)
    circuit.barrier()
    circuit.measure(0, 0)
    return circuit


def make_repetition_memory_circuit(initial_state: int = 0, memory_gates: int = 1) -> QuantumCircuit:
    """Create a three-qubit repetition-code memory circuit."""
    if initial_state not in (0, 1):
        raise ValueError("initial_state must be 0 or 1")
    if memory_gates < 1:
        raise ValueError("memory_gates must be at least 1")

    circuit = QuantumCircuit(3, 3, name=f"repetition3_{initial_state}")
    if initial_state == 1:
        circuit.x(0)

    circuit.cx(0, 1)
    circuit.cx(0, 2)
    circuit.barrier()
    for qubit in range(3):
        for _ in range(memory_gates):
            circuit.id(qubit)
    circuit.barrier()
    circuit.measure([0, 1, 2], [0, 1, 2])
    return circuit
```

## Decode measurement results

Qiskit returns counts such as `{'111': 3500, '011': 200, ...}`. For the repetition code, the decoder counts how many `1` values appear in each bitstring. If two or three bits are `1`, it decodes logical `1`; otherwise it decodes logical `0`.

This decoder is intentionally simple. It is a majority-vote decoder, not a full stabilizer decoder.

```python
def decode_majority_vote(bitstring: str) -> int:
    """Decode a measured bitstring by majority vote."""
    cleaned = bitstring.replace(" ", "")
    if not cleaned or any(bit not in "01" for bit in cleaned):
        raise ValueError(f"Invalid bitstring: {bitstring!r}")

    ones = cleaned.count("1")
    zeros = len(cleaned) - ones
    if ones == zeros:
        raise ValueError("Majority vote needs an odd number of bits")
    return int(ones > zeros)


def logical_error_rate(counts: Mapping[str, int], expected_logical_value: int) -> float:
    """Compute the decoded logical error rate from measurement counts."""
    if expected_logical_value not in (0, 1):
        raise ValueError("expected_logical_value must be 0 or 1")
    total = sum(counts.values())
    if total <= 0:
        raise ValueError("counts must contain at least one shot")

    errors = sum(
        count
        for bitstring, count in counts.items()
        if decode_majority_vote(bitstring) != expected_logical_value
    )
    return errors / total
```

## Add a bit-flip noise model

A bit-flip error applies an $X$ gate by accident. The model below adds an $X$ after each `id` gate with probability $p$. This is not a complete hardware noise model. It is a controlled classroom model that lets us test the repetition-code formula.

```python
from qiskit_aer.noise import NoiseModel, pauli_error
from qiskit_aer.primitives import SamplerV2 as AerSampler


def make_bitflip_noise_model(p: float) -> NoiseModel:
    """Build an Aer noise model that applies X after each id gate with probability p."""
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be between 0 and 1")

    error = pauli_error([("X", p), ("I", 1 - p)])
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error, ["id"])
    return noise_model


def counts_from_sampler_result_item(result_item) -> dict[str, int]:
    """Extract counts from a Qiskit SamplerV2 result item."""
    data = result_item.data
    register_names = list(data.keys())
    if not register_names:
        raise ValueError("Sampler result does not contain classical data")
    bit_array = getattr(data, register_names[0])
    return dict(bit_array.get_counts())


def run_aer_sampler(circuits, p: float, shots: int = 4000, seed: int = 52) -> list[dict[str, int]]:
    """Run circuits with Aer SamplerV2 and the bit-flip noise model."""
    sampler = AerSampler(
        default_shots=shots,
        seed=seed,
        options={"backend_options": {"noise_model": make_bitflip_noise_model(p)}},
    )
    result = sampler.run(list(circuits), shots=shots).result()
    return [counts_from_sampler_result_item(item) for item in result]
```

For $p = 0.12$ and 4000 shots, the notebook produced:

```text
unencoded {'1': 3539, '0': 461}
logical error rate: 0.1153

encoded {'111': 2697, '101': 362, '011': 388, '110': 389,
         '010': 50, '001': 50, '100': 59, '000': 5}
logical error rate: 0.0410
```

The encoded histogram has most shots near `111`, plus smaller bars such as `011`, `101`, and `110`, where one physical bit flipped. Majority vote still decodes those one-flip outcomes as logical `1`. Outcomes with two or three flipped bits decode incorrectly.

![Three-qubit repetition code outcome histogram at p = 0.12](/assets/images/qec-basics/qec_histogram_p012.png)

## Physical error rate versus logical error rate

Now we repeat the experiment for several values of $p$. We compare four quantities:

- simulated unencoded logical error rate;
- simulated three-qubit decoded logical error rate;
- theory for one physical bit, $p$;
- theory for the three-qubit code, $3p^2 - 2p^3$.

Finite-shot sampling means the simulated points will not land exactly on the theory curves.

| $p$ | unencoded simulation | encoded simulation | unencoded theory | encoded theory |
|---:|---:|---:|---:|---:|
| 0.00 | 0.0000 | 0.0000 | 0.00 | 0.0000 |
| 0.05 | 0.0425 | 0.0072 | 0.05 | 0.0073 |
| 0.10 | 0.0965 | 0.0250 | 0.10 | 0.0280 |
| 0.15 | 0.1430 | 0.0590 | 0.15 | 0.0608 |
| 0.20 | 0.2088 | 0.1135 | 0.20 | 0.1040 |
| 0.25 | 0.2547 | 0.1478 | 0.25 | 0.1562 |
| 0.30 | 0.3198 | 0.2115 | 0.30 | 0.2160 |
| 0.35 | 0.3558 | 0.2932 | 0.35 | 0.2818 |
| 0.40 | 0.3952 | 0.3512 | 0.40 | 0.3520 |
| 0.45 | 0.4462 | 0.4200 | 0.45 | 0.4253 |
| 0.50 | 0.4998 | 0.4922 | 0.50 | 0.5000 |

For small $p$, the encoded curve is below the unencoded curve. This is the core lesson of the repetition code: using three physical qubits can reduce the logical error rate when the physical error rate is low enough. At $p = 0.5$, random guessing wins no advantage, and both curves meet at $0.5$.

The experiment is deliberately idealized. We did not add gate errors to the encoding circuit. On real hardware, the extra gates and measurements also introduce errors.

## Miniature version of a modern QEC benchmark

Modern QEC experiments often ask whether the logical error rate improves when the code distance increases or when repeated syndrome measurements are used. A full state-of-the-art replication needs many qubits, many measurement rounds, calibrated devices, and careful decoding.

We can still reproduce the smallest conceptual version in a classical simulation of repetition codes: compare one physical bit with odd repetition codes of length 3, 5, and 7. This is not a surface-code threshold theorem. It is a threshold-style teaching plot for independent bit flips and majority vote.

![Threshold-style repetition code plot](/assets/images/qec-basics/qec_repetition_threshold_style.png)

The longer repetition codes do better at small $p$, but all curves meet at $p = 0.5$. Above $p = 0.5$, majority vote would usually pick the wrong value. Real quantum codes protect against richer noise and need a decoder that uses syndrome measurements, not just a final majority vote.

## Beyond the toy model

The three-qubit repetition code protects against one bit flip. It does **not** protect a general quantum state from all possible errors.

A useful way to see the limitation is to remember that a general qubit can be written as

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle.
$$

A bit flip changes $|0\rangle$ to $|1\rangle$ and $|1\rangle$ to $|0\rangle$. A phase flip leaves the measurement values alone but changes the relative sign of the superposition. The three-qubit bit-flip code does not detect that phase error in the same basis.

More complete QEC codes use **stabilizer checks**. A stabilizer check is a measurement that reveals error information without revealing the encoded state itself. The surface code is a leading family of stabilizer codes because its checks are local on a two-dimensional grid and it has a threshold: below a sufficiently low physical error rate, increasing the code distance can reduce the logical error rate.

Present-day devices still have noisy gates, measurement errors, leakage, crosstalk, and calibration drift. QEC research is about making the logical error rate improve despite those costs. This tutorial is a teaching example, not a full fault-tolerant processor.

## Optional: run a tiny version on real IBM quantum hardware

This section is disabled by default in the notebook:

```python
RUN_ON_IBM = False
```

The optional run uses Qiskit Runtime `SamplerV2` in job mode with `mode=backend`. It does not use a session. The batch is intentionally small: three circuits with 256 shots each by default.

To run it, set an environment variable outside the notebook:

```bash
export QISKIT_IBM_TOKEN="your-api-key"
# Optional if you want to select a specific instance:
export QISKIT_IBM_INSTANCE="your-instance-crn-or-name"
```

Do not paste tokens into the notebook, do not print tokens, and do not save credentials into the repository. IBM Open Plan usage is limited to about 10 minutes per 28-day rolling window, so check your account usage before enabling this cell.

The optional batch uses these circuits:

1. one unencoded logical `1` memory circuit;
2. one three-qubit encoded logical `1` memory circuit;
3. one three-qubit encoded logical `1` circuit with one deliberate `X` before measurement.

The third circuit is a small demonstration of majority-vote decoding with one known bit flip:

![Three-qubit repetition circuit with one deliberate X](/assets/images/qec-basics/qec_known_single_flip_circuit.png)

The hardware code uses the current Runtime V2 sampler pattern:

```python
RUN_ON_IBM = False
IBM_SHOTS = 256


def run_ibm_sampler_optional(circuits, shots: int = IBM_SHOTS) -> list[dict[str, int]] | None:
    """Run a tiny SamplerV2 job on IBM hardware when RUN_ON_IBM is True."""
    if not RUN_ON_IBM:
        print("IBM hardware run skipped. Set RUN_ON_IBM = True only after checking your IBM plan usage.")
        return None

    token = os.getenv("QISKIT_IBM_TOKEN")
    if not token:
        print("QISKIT_IBM_TOKEN is not set. Use the Aer simulator results above instead.")
        return None

    try:
        from qiskit.transpiler import generate_preset_pass_manager
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as RuntimeSampler
    except ImportError as exc:
        print(f"qiskit-ibm-runtime is not available: {exc}")
        return None

    channel = os.getenv("QISKIT_IBM_CHANNEL", "ibm_quantum_platform")
    instance = os.getenv("QISKIT_IBM_INSTANCE") or None
    service = QiskitRuntimeService(channel=channel, token=token, instance=instance)

    def usable_backend(backend) -> bool:
        try:
            status = backend.status()
            configuration = backend.configuration()
            return bool(status.operational) and not bool(configuration.simulator)
        except Exception:
            return False

    try:
        backend = service.least_busy(min_num_qubits=3, filters=usable_backend)
    except Exception as exc:
        print(f"Could not select an IBM backend: {exc}")
        return None

    print(f"Submitting {len(circuits)} circuits x {shots} shots = {len(circuits) * shots} shots.")

    try:
        pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=1)
        isa_circuits = pass_manager.run(list(circuits))
        sampler = RuntimeSampler(mode=backend)
        job = sampler.run(isa_circuits, shots=shots)
        result = job.result()
    except Exception as exc:
        print(f"IBM hardware job did not complete: {exc}")
        return None

    return [counts_from_sampler_result_item(item) for item in result]
```

If you enable the hardware run, decode the returned bitstrings with the same `logical_error_rate` function. Treat the result as a small hardware-friendly demonstration. It is not an active QEC experiment with repeated syndrome measurements and feedback.

## Common mistakes

> **Confusing detection with correction.** Detecting that an error may have happened is not the same as correcting it. In this tutorial, final measurement and majority vote correct one bit flip only after the circuit has ended.
>
> **Assuming QEC violates no-cloning.** QEC encodes information into correlations among qubits. It does not make independent copies of an unknown quantum state.
>
> **Thinking the three-qubit repetition code corrects all quantum errors.** It corrects one bit flip in this simple setting. It does not protect against general phase errors.
>
> **Forgetting that extra gates can add noise.** In the clean simulation, encoding gates are perfect. On hardware, those gates can introduce errors.
>
> **Treating simulator results as hardware results.** The plots above are simulator results with an injected bit-flip model. Hardware results should be reported only if the hardware cell was actually run.

## Video demo

Issue #52 asks for a video demo or explanation. This pull request includes a complete 3-5 minute recording script and scene outline at:

```text
assets/images/qec-basics/qec_tutorial_video_script.md
```

Video link: **TODO: add a public recording link after a contributor records and hosts the demo.**

## What to try next

A natural extension is the phase-flip repetition code. The idea is to place Hadamard gates before and after the memory step so that phase flips become bit flips in the rotated basis. After that, study stabilizer measurements and the surface code.

For a first project, keep the circuits small. Change one thing at a time: the physical error rate, the number of shots, the repetition length, or whether measurement error is included.


## Contributor note

Contributor note: I first found QEC approachable by starting with the three-qubit repetition code, because it turns the abstract idea of a logical qubit into a simple majority-vote experiment. If you are new to the field, begin with small circuits like the ones above, then move to stabilizers and surface-code tutorials.

## References

[1] Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information: 10th Anniversary Edition*, Cambridge University Press, 2010. DOI: [10.1017/CBO9780511976667](https://doi.org/10.1017/CBO9780511976667).

[2] Peter W. Shor, "Scheme for reducing decoherence in quantum computer memory," *Physical Review A* 52, R2493-R2496, 1995. DOI: [10.1103/PhysRevA.52.R2493](https://doi.org/10.1103/PhysRevA.52.R2493).

[3] Andrew M. Steane, "Error Correcting Codes in Quantum Theory," *Physical Review Letters* 77, 793-797, 1996. DOI: [10.1103/PhysRevLett.77.793](https://doi.org/10.1103/PhysRevLett.77.793).

[4] Daniel Gottesman, *Stabilizer Codes and Quantum Error Correction*, Ph.D. thesis, Caltech, 1997. arXiv: [quant-ph/9705052](https://arxiv.org/abs/quant-ph/9705052).

[5] Eric Dennis, Alexei Kitaev, Andrew Landahl, and John Preskill, "Topological quantum memory," *Journal of Mathematical Physics* 43, 4452-4505, 2002. DOI: [10.1063/1.1499754](https://doi.org/10.1063/1.1499754).

[6] Austin G. Fowler, Matteo Mariantoni, John M. Martinis, and Andrew N. Cleland, "Surface codes: Towards practical large-scale quantum computation," *Physical Review A* 86, 032324, 2012. DOI: [10.1103/PhysRevA.86.032324](https://doi.org/10.1103/PhysRevA.86.032324).

[7] Google Quantum AI, "Suppressing quantum errors by scaling a surface code logical qubit," *Nature* 614, 676-681, 2023. DOI: [10.1038/s41586-022-05434-1](https://doi.org/10.1038/s41586-022-05434-1).

[8] Google Quantum AI and Collaborators, "Quantum error correction below the surface code threshold," *Nature* 638, 920-926, 2025. DOI: [10.1038/s41586-024-08449-y](https://doi.org/10.1038/s41586-024-08449-y).

[9] Qiskit documentation: [https://quantum.cloud.ibm.com/docs/en/api/qiskit](https://quantum.cloud.ibm.com/docs/en/api/qiskit).

[10] Qiskit Aer noise model guide: [https://quantum.cloud.ibm.com/docs/en/guides/build-noise-models](https://quantum.cloud.ibm.com/docs/en/guides/build-noise-models).

[11] Qiskit Runtime SamplerV2 API: [https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/sampler-v2](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/sampler-v2).

[12] IBM Quantum plans overview: [https://quantum.cloud.ibm.com/docs/en/guides/plans-overview](https://quantum.cloud.ibm.com/docs/en/guides/plans-overview).
