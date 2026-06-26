---
title: "Making Noisy Quantum Computers More Useful: A Hands-On Introduction to Quantum Error Mitigation with Qiskit"
categories:
  - Blog
tags:
  - quantum-error-mitigation
  - Qiskit
  - jupyter notebook
  - tutorial
  - quantum computing
  - IBM Quantum
  - noisy quantum hardware
author:
  - Quantum Universal Education Contributors
---

A thermometer gives noisy readings, so a careful scientist repeats the measurement and reports an average with uncertainty. A quantum computer also gives statistical data, but the noise can come from quantum gates, measurements, idle qubits, calibration drift, crosstalk, and unwanted coupling to the environment.

Many near-term quantum algorithms estimate **expectation values**: averages of many measurement outcomes. **Quantum error mitigation (QEM)** tries to reduce bias in those estimates by using extra experiments and classical post-processing.

QEM is different from quantum error correction. Error correction protects information by encoding it into larger logical qubits and correcting errors during the computation. Error mitigation does not correct every physical error. It tries to infer a better estimate of an ideal noiseless value from noisy data.

In this tutorial we will build a small Bell-state experiment, add simulator noise, implement readout error mitigation from first principles, and use a simple zero-noise extrapolation fit. The optional IBM Quantum section is disabled by default and is designed for a tiny shot budget.

![Bell circuit](/assets/images/qem-basics/qem_bell_circuit.png)

## Learning goals

By the end you should be able to:

- explain why noisy quantum computers return biased estimates;
- distinguish error suppression, error mitigation, and quantum error correction;
- estimate `ZZ`, `XX`, and `YY` correlations of a Bell state;
- build a small Qiskit Aer noise model;
- calibrate and invert a two-qubit readout assignment matrix;
- perform a basic zero-noise extrapolation experiment;
- run the tutorial fully in simulator mode without IBM credentials.

## Dependencies

The notebook was validated with:

```bash
python -m pip install -r requirements-qem-tutorial.txt
```

The requirements file contains:

```text
qiskit==2.4.1
qiskit-aer==0.17.2
qiskit-ibm-runtime==0.47.0
numpy==2.3.5
matplotlib==3.10.8
pandas==2.2.3
jupyter==1.1.1
nbconvert==7.17.1
ipykernel==7.2.0
pylatexenc==2.10
```

`pylatexenc` is only used to draw circuit diagrams with Matplotlib. The hardware section reads a token from an environment variable and does not run unless `RUN_ON_IBM = True`.

## 1. Why quantum computers give noisy answers

A classical bit can flip if a memory cell or communication channel is noisy. Qubits are more delicate. A gate might rotate a qubit by a slightly wrong angle. A two-qubit gate might entangle the qubits imperfectly. A measurement device might report `0` when the qubit was measured as `1`. Even waiting can be harmful because qubits interact with their surroundings.

This tutorial focuses on **observable estimation**. An observable is a quantity we estimate by running a circuit many times. Each shot gives one measurement result. The average over many shots estimates the expectation value.

The important distinction is:

- **Error suppression** reduces errors before or during execution, for example with transpilation choices, dynamical decoupling, gate twirling, or measurement twirling.
- **Error mitigation** uses extra experiments and classical post-processing after noisy data are collected.
- **Quantum error correction** encodes quantum information into larger logical qubits and corrects errors during the computation.

QEM is useful for learning and for some near-term experiments, but it is not a replacement for fault-tolerant quantum computing.

## 2. A tiny observable-estimation problem

We prepare the Bell state

$$
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}.
$$

This state has simple ideal correlations:

$$
\langle ZZ\rangle = 1, \quad \langle XX\rangle = 1, \quad \langle YY\rangle = -1.
$$

A value near `1` means the two measurement signs usually agree. A value near `-1` means the signs usually disagree. A value near `0` means the correlation has mostly washed out.

```python
from qiskit import QuantumCircuit


def make_bell_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(2, name="bell_phi_plus")
    circuit.h(0)
    circuit.cx(0, 1)
    return circuit


def make_observable_circuit(observable: str) -> QuantumCircuit:
    observable = observable.upper()
    if len(observable) != 2 or any(symbol not in "IXYZ" for symbol in observable):
        raise ValueError("Use a two-character observable made from I, X, Y, and Z.")

    circuit = make_bell_circuit()
    for qubit, pauli in enumerate(reversed(observable)):
        if pauli == "X":
            circuit.h(qubit)
        elif pauli == "Y":
            circuit.sdg(qubit)
            circuit.h(qubit)
    circuit.measure_all()
    return circuit
```

The reversed loop is there because Qiskit count strings are displayed as `c1 c0`. The rightmost bit corresponds to qubit 0.

## 3. Noisy simulation with Qiskit Aer

We use a compact noise model: small one-qubit depolarizing noise, stronger two-qubit depolarizing noise, and asymmetric readout error.

```python
from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error


def build_simple_noise_model(
    one_qubit_depol: float = 0.002,
    two_qubit_depol: float = 0.02,
    readout_p0_to_1: float = 0.03,
    readout_p1_to_0: float = 0.05,
) -> NoiseModel:
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(one_qubit_depol, 1), ["h", "x", "sx", "s", "sdg"]
    )
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(two_qubit_depol, 2), ["cx"]
    )
    noise_model.add_all_qubit_readout_error(
        ReadoutError([[1 - readout_p0_to_1, readout_p0_to_1],
                      [readout_p1_to_0, 1 - readout_p1_to_0]])
    )
    return noise_model
```

In a clean notebook run with 4000 shots, the raw noisy estimates were:

| observable | ideal | raw noisy | raw standard error |
|---|---:|---:|---:|
| ZZ | 1.0 | 0.8295 | 0.0088 |
| XX | 1.0 | 0.8255 | 0.0089 |
| YY | -1.0 | -0.8235 | 0.0090 |

The ideal `ZZ` measurement only returns `00` and `11`. The noisy model also produces `01` and `10`.

![Noisy versus ideal histogram](/assets/images/qem-basics/qem_noisy_vs_ideal_histogram.png)

## 4. Readout error mitigation from first principles

Readout error means the measurement device can report the wrong classical bit. We estimate this by preparing all computational basis states and measuring them:

- prepare `00`, `01`, `10`, and `11`;
- measure each state many times;
- build an assignment matrix;
- invert the matrix and apply it to the observed probability vector.

The assignment matrix column for `prepared 01`, for example, tells us the distribution of reported bitstrings when `01` was prepared.

![Readout assignment matrix](/assets/images/qem-basics/qem_readout_assignment_matrix.png)

```python
import numpy as np

STATES_2Q = ("00", "01", "10", "11")


def apply_readout_mitigation(counts, assignment_matrix):
    observed = counts_to_probability_vector(counts)
    corrected = np.linalg.pinv(assignment_matrix) @ observed
    corrected = np.clip(corrected, 0.0, None)
    return corrected / corrected.sum()
```

The pseudo-inverse is more forgiving than a direct inverse. The clipping step handles tiny negative probabilities caused by finite-shot noise. This is a practical teaching choice, not a guarantee that mitigation always works.

For the same 4000-shot simulator run, readout mitigation moved the estimates closer to the ideal values:

| observable | ideal | raw noisy | readout mitigated |
|---|---:|---:|---:|
| ZZ | 1.0 | 0.8295 | 0.9855 |
| XX | 1.0 | 0.8255 | 0.9783 |
| YY | -1.0 | -0.8235 | -0.9743 |

![Raw versus readout-mitigated expectations](/assets/images/qem-basics/qem_raw_vs_readout_mitigated.png)

Readout mitigation costs extra shots because the calibration circuits must also be measured. It can also increase variance if the assignment matrix is poorly estimated or nearly singular.

## 5. Zero-noise extrapolation

Zero-noise extrapolation, or ZNE, estimates the answer at zero noise by running noisier versions of the same ideal circuit. A digital way to increase noise is gate folding:

$$
U \quad \rightarrow \quad U U^\dagger U.
$$

The folded circuit has the same ideal action as the original, but it uses more gates. More gates usually means more noise. We run noise factors 1, 3, and 5, fit a line, and evaluate the line at noise factor 0.

```python
def fit_zero_noise_limit(noise_factors, expectations):
    coefficients = np.polyfit(noise_factors, expectations, deg=1)
    polynomial = np.poly1d(coefficients)
    return float(polynomial(0.0)), coefficients
```

For `ZZ`, the clean notebook run gave:

| noise factor | raw ZZ | readout-mitigated ZZ |
|---:|---:|---:|
| 1 | 0.8245 | 0.9777 |
| 3 | 0.8065 | 0.9565 |
| 5 | 0.7750 | 0.9194 |

The raw ZNE estimate was `0.839`, while readout mitigation plus ZNE gave `0.995`. The combined estimate is close to the ideal value, but it is still an extrapolation.

![ZNE extrapolation](/assets/images/qem-basics/qem_zne_extrapolation.png)

ZNE does not know the exact noise. It assumes the observable changes smoothly as the noise is increased. If the fit model is wrong, the circuit is too noisy, or the shot noise is too large, the extrapolated value can be worse than the raw value.

## 6. Miniature version of a modern QEM workflow

Research-scale QEM studies often:

- estimate observables from noisy hardware;
- amplify noise deliberately;
- extrapolate to the zero-noise limit;
- use measurement mitigation;
- trade extra circuit executions for lower bias;
- report uncertainty and overhead.

This tutorial reproduces the smallest conceptual version: one Bell-state observable with several simulator noise strengths.

![Mitigation mini benchmark](/assets/images/qem-basics/qem_mitigation_mini_benchmark.png)

The benchmark should be read carefully. Mitigation helps most when the noise is moderate and the assumptions are reasonable. At high noise, extrapolation can become unreliable. This is why QEM results should be reported with uncertainty, calibration details, and overhead.

## 7. Error suppression versus mitigation

Real workflows may combine several ideas:

- **Transpilation optimization** can choose shorter or hardware-friendlier circuits.
- **Dynamical decoupling** inserts pulses during idle periods to reduce decoherence.
- **Pauli twirling** changes coherent error patterns into easier-to-model stochastic patterns.
- **Measurement twirling and TREX** reduce measurement-bias effects in expectation-value estimation.

Suppression changes the experiment before or during execution. Mitigation post-processes data after execution. A careful workflow states which tools were used.

## 8. Optional: run a tiny error-mitigation experiment on IBM quantum hardware

This section is included in the notebook and is disabled by default:

```python
RUN_ON_IBM = False
IBM_SHOTS = 256
```

The optional function uses `qiskit-ibm-runtime` with Runtime `EstimatorV2`, `mode=backend`, a least-busy operational backend with at least two qubits, and a tiny Bell-state observable-estimation job. It does not use sessions. It reads credentials from:

```text
QISKIT_IBM_TOKEN
QISKIT_IBM_INSTANCE  # optional
```

The function plans:

- one Bell-state circuit;
- two observables: `ZZ` and `XX`;
- 256 requested shots per Estimator job;
- one raw job with `resilience_level = 0`;
- one readout-mitigated job with `resilience_level = 1` and explicit measurement-noise-learning settings.

No IBM hardware results are included in this post. If a contributor runs the optional cell, they should report the backend, date, shot count, mitigation options, and result provenance. Tokens, account names, and private job identifiers must not be committed.

## Common mistakes

- **Thinking mitigation removes all errors.** It reduces bias under assumptions; it does not make hardware noiseless.
- **Confusing mitigation with error correction.** QEM post-processes estimates. QEC protects logical quantum information during the computation.
- **Ignoring overhead.** Calibration circuits, folded circuits, and extra shots cost time.
- **Using ZNE outside its useful regime.** If the circuit is too noisy, extrapolation can fail.
- **Trusting a mitigated value without uncertainty.** A number without an uncertainty estimate can be misleading.
- **Treating simulator results as hardware results.** Simulator noise models are useful, but they are not measured hardware data.

## Video demo

A complete 3-5 minute recording script and scene plan is included at:

```text
assets/images/qem-basics/qem_tutorial_video_script.md
```

TODO: add a public video link here after recording. No hosted video link is claimed in this PR.

## AI-use statement

AI assistance was used to help draft and check the tutorial structure, code organization, references, wording, and validation steps. The simulator code and plots were executed locally during preparation. All explanations, references, and results should be reviewed by the contributor before publication. No IBM hardware results are included.

## Contributor note

Contributor note: I first found quantum error mitigation approachable by starting with a simple question: if a quantum computer gives a noisy expectation value, can extra experiments and careful classical post-processing make the estimate less biased? Small circuits like the Bell-state example above are a good place to start before moving to larger algorithms.

## References

1. K. Temme, S. Bravyi, and J. M. Gambetta, "Error mitigation for short-depth quantum circuits," *Physical Review Letters* 119, 180509 (2017), arXiv:1612.02058.
2. Y. Li and S. C. Benjamin, "Efficient variational quantum simulator incorporating active error minimisation," *Physical Review X* 7, 021050 (2017), arXiv:1611.09301.
3. S. Endo, S. C. Benjamin, and Y. Li, "Practical quantum error mitigation for near-future applications," *Physical Review X* 8, 031027 (2018), arXiv:1712.09271.
4. T. Giurgica-Tiron, Y. Hindy, R. LaRose, A. Mari, and W. J. Zeng, "Digital zero noise extrapolation for quantum error mitigation," arXiv:2005.10921 (2020).
5. A. Kandala et al., "Error mitigation extends the computational reach of a noisy quantum processor," *Nature* 567, 491-495 (2019).
6. Qiskit documentation: <https://quantum.cloud.ibm.com/docs>
7. Qiskit Aer noise model documentation: <https://qiskit.github.io/qiskit-aer/>
8. IBM Quantum Runtime Estimator documentation: <https://quantum.cloud.ibm.com/docs/api/qiskit-ibm-runtime/estimator-v2>
9. IBM Quantum error mitigation and suppression documentation: <https://quantum.cloud.ibm.com/docs/guides/error-mitigation-and-suppression-techniques>
10. IBM Quantum Open Plan documentation: <https://quantum.cloud.ibm.com/docs/guides/plans-overview>
