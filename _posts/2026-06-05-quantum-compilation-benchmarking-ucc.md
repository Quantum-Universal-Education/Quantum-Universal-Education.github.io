---
title: "Quantum Compilation Benchmarking With Five Simulators"
categories:
  - Blog
tags:
  - unitaryHACK
  - quantum compilation
  - benchmarking
  - UCC
  - simulation
author:
  - Adam Zhang
---

# Quantum Compilation Benchmarking With Five Simulators

Quantum computers are not only about writing circuits. A circuit also has to be
compiled, translated, and tested before it can run well on real hardware or a
simulator. This tutorial shows one small but useful way to study that process:
start from one unoptimized circuit, send it to several simulators, and measure
how the runtime changes as the circuit gets wider and deeper.

The tutorial is written for high school and undergraduate students who know a
little Python and are starting to meet quantum circuits. You do not need to be a
quantum compiler expert. The goal is to build intuition, run a reproducible
benchmark, and learn how to compare results without fooling ourselves.

The code for this tutorial is included here:

- [`benchmark_ucc_simulators.py`](/assets/quantum_programs/quantum_compilation_benchmarking/benchmark_ucc_simulators.py)
- [`requirements.txt`](/assets/quantum_programs/quantum_compilation_benchmarking/requirements.txt)

## What You Will Learn

By the end, you should be able to:

1. Explain why quantum circuits are compiled before execution.
2. Describe what a benchmark is and why one circuit must be tested fairly.
3. Build a UCC-style unoptimized circuit with at least 10 qubits.
4. Import the same neutral gate list into five simulators.
5. Record runtime in a table and study how it scales with qubit count and
   circuit depth.

## The Big Idea

A quantum circuit is a recipe. It says which gates should act on which qubits.
However, a simulator or device may not understand every recipe in the same way.
Compilation is the process of rewriting the recipe into a form that is easier
for a specific backend to run.

For this benchmark, we keep the circuit deliberately unoptimized. That means we
do not ask one framework to simplify the gates while another framework receives
the original circuit. Every simulator starts from the same neutral list of
gates:

```python
("ry", (q,), (theta,))
("rz", (q,), (theta,))
("cx", (control, target), ())
```

The script then imports that same list into:

| Simulator interface | Python package | Why it is useful |
| --- | --- | --- |
| Qiskit Aer | `qiskit-aer` | Popular statevector simulator in the Qiskit ecosystem |
| Cirq Simulator | `cirq-core` | Google's circuit model framework |
| PennyLane `default.qubit` | `pennylane` | Differentiable simulation used in variational algorithms |
| Qibo | `qibo` | Fast simulation framework with multiple backend options |
| Amazon Braket LocalSimulator | `amazon-braket-sdk` | Local version of the Braket circuit interface |

## What Does UCC Mean Here?

In quantum computing, UCC can mean "unitary coupled cluster", an ansatz used in
quantum chemistry. In the unitaryHACK context, UCC also points to the Unitary
Compiler Collection, a community effort around frontend-agnostic quantum
compilation and benchmarking.

This tutorial uses a student-sized UCC-style benchmarking goal:

- use a circuit with repeated excitation-like entangling layers;
- keep it frontend-neutral before importing it into each simulator;
- compare runtimes as qubit count and depth increase;
- focus on reproducibility and fairness rather than claiming that one simulator
  is always best.

That is the same benchmarking habit used in larger compiler projects: define the
workload, keep the input controlled, and measure one thing at a time.

## Setup

Use Python 3.11 or newer. Some current quantum packages, including recent Cirq
releases, do not install on the macOS system Python 3.9 that ships with many
machines.

```bash
cd assets/quantum_programs/quantum_compilation_benchmarking
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Run the smallest complete benchmark first:

```bash
python benchmark_ucc_simulators.py --qubits 10 --depths 2 --shots 256 --repeats 2
```

Then run a scaling benchmark:

```bash
python benchmark_ucc_simulators.py \
  --qubits 10 12 14 \
  --depths 2 4 8 \
  --shots 512 \
  --repeats 3 \
  --warmups 1 \
  --output ucc_simulator_benchmark_results.csv
```

If a simulator package is missing or fails on your machine, the script marks
that row as `skipped` and keeps going. This is useful in a classroom: students
can still compare the simulators that are installed, and the error column shows
which dependency needs attention.

## Step 1: Build One Neutral Circuit

The benchmark begins with this function:

```python
def build_ucc_style_gate_list(qubits: int, depth: int) -> list[Gate]:
    gates: list[Gate] = []
    for layer in range(depth):
        for q in range(qubits):
            theta = 0.031 * (layer + 1) * (q + 1)
            gates.append(("ry", (q,), (theta,)))
            gates.append(("rz", (q,), (theta / 2,)))

        for q in range(0, qubits - 1, 2):
            angle = 0.019 * (layer + 1) * (q + 1)
            gates.extend([
                ("cx", (q, q + 1), ()),
                ("rz", (q + 1,), (angle,)),
                ("cx", (q, q + 1), ()),
            ])
```

The exact angles are less important than the structure. Each layer adds:

- single-qubit rotations, which act like variational parameters;
- controlled operations, which create correlations between qubits;
- a repeated pattern, so the circuit grows when `depth` increases.

Why require at least 10 qubits? Because a benchmark that only uses two or three
qubits can hide scaling problems. Ten qubits is still friendly to laptops, but
large enough for differences between simulators to start showing up.

## Step 2: Import The Same Circuit Into Every Simulator

Each simulator has its own circuit object. Qiskit uses `QuantumCircuit`, Cirq
uses `cirq.Circuit`, PennyLane uses a `QNode`, Qibo uses `Circuit`, and Braket
uses `braket.circuits.Circuit`.

For example, the Qiskit importer is:

```python
def run_qiskit(case: BenchmarkCase, shots: int) -> object:
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator

    circuit = QuantumCircuit(case.qubits)
    for name, qubits, params in case.gates:
        if name == "ry":
            circuit.ry(params[0], qubits[0])
        elif name == "rz":
            circuit.rz(params[0], qubits[0])
        elif name == "cx":
            circuit.cx(qubits[0], qubits[1])
    circuit.measure_all()
    backend = AerSimulator(method="statevector")
    return backend.run(circuit, shots=shots).result()
```

The other simulator functions follow the same idea. This keeps the benchmark
fair because the simulator-specific code is only an importer, not a separate
circuit design.

## Step 3: Measure Runtime

The script uses `time.perf_counter()` and repeats each run several times:

```python
def run_repeated(func: Callable[[], object], repeats: int) -> tuple[float, float]:
    samples = [time_once(func) for _ in range(repeats)]
    return statistics.median(samples), min(samples)
```

The median is usually better than a single timing measurement. Your computer may
be doing background work, downloading updates, or sharing CPU time with other
programs. A median reduces the effect of one unusually slow or fast run.

## Step 4: Record Results In A Table

The script writes a CSV file with this shape:

| simulator | qubits | depth | gate_count | shots | repeats | warmups | median_seconds | best_seconds | status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| qiskit_aer | 10 | 2 | 70 | 512 | 3 | 1 | your result | your result | ok |
| cirq | 10 | 2 | 70 | 512 | 3 | 1 | your result | your result | ok |
| pennylane_default_qubit | 10 | 2 | 70 | 512 | 3 | 1 | your result | your result | ok |
| qibo | 10 | 2 | 70 | 512 | 3 | 1 | your result | your result | ok |
| braket_local | 10 | 2 | 70 | 512 | 3 | 1 | your result | your result | ok |

The row count is:

```text
number of simulators x number of qubit sizes x number of depths
```

With five simulators, three qubit sizes, and three depths, you get 45 rows.
The `warmups` column records untimed warmup runs. This matters because the first
call to a simulator can include package imports, font-cache setup, or backend
initialization that should not be confused with steady simulation time.

## Step 5: Study Scaling

After you run the script, sort the CSV by simulator, then by qubits and depth.
Ask three questions:

1. When qubit count increases, does runtime grow gently or sharply?
2. When depth increases, does runtime grow in proportion to gate count?
3. Do different simulators have different strengths?

You should expect runtime to increase as qubits increase because statevector
simulation stores amplitudes for all computational basis states. A 10-qubit
state has 2^10 amplitudes. A 14-qubit state has 2^14 amplitudes. That is not
just four more amplitudes; it is sixteen times as many.

Depth also matters because every gate has to be applied. A deeper circuit gives
the simulator more work even when the number of qubits is unchanged.

## A Simple Plot

Once you have `ucc_simulator_benchmark_results.csv`, you can plot it:

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("ucc_simulator_benchmark_results.csv")
df = df[df["status"] == "ok"]

for simulator, group in df.groupby("simulator"):
    subset = group[group["depth"] == group["depth"].max()]
    plt.plot(subset["qubits"], subset["median_seconds"], marker="o", label=simulator)

plt.xlabel("Number of qubits")
plt.ylabel("Median runtime (seconds)")
plt.title("UCC-style benchmark scaling at maximum tested depth")
plt.legend()
plt.tight_layout()
plt.show()
```

The best plot is not always the prettiest plot. The best plot is the one that
makes the comparison honest and easy to understand.

## Short Demo Video

A short silent demo video is included with the tutorial assets:

`assets/quantum_programs/quantum_compilation_benchmarking/ucc_benchmark_demo.webm`

It walks through the classroom flow:

1. build one neutral UCC-style gate list;
2. import the same unoptimized workload into five simulator interfaces;
3. compare the benchmark rows and scaling metadata;
4. interpret the result as an educational benchmark rather than a universal
   ranking of quantum software packages.

The video was recorded from:

`assets/quantum_programs/quantum_compilation_benchmarking/demo.html`

## Common Mistakes

### Mistake 1: Comparing Different Circuits

If Qiskit receives a small circuit and Cirq receives a larger one, the timing
comparison is not meaningful. This tutorial avoids that by using one neutral
gate list.

### Mistake 2: Timing Compilation And Simulation Together Without Saying So

This script measures the time needed to build/import and run the circuit. That
is a useful beginner benchmark, but it is not the only possible benchmark. A
compiler benchmark might separately measure:

- circuit construction time;
- compilation/transpilation time;
- simulation execution time;
- memory use;
- output accuracy.

Always tell readers exactly what you measured.

### Mistake 3: Treating One Laptop As A Universal Truth

If your friend runs the same script on another machine, they may get different
seconds. That is normal. The benchmark is still valuable because the scaling
shape is informative.

## References

- Unitary Foundation, "Introducing the Unitary Compiler Collection (UCC)".
- Unitary Foundation, "Community-Driven Quantum Compilation w/ UCC".
- UCC documentation, "Unitary Compiler Collection User Guide".
- Qiskit Aer documentation.
- Cirq documentation.
- PennyLane documentation.
- Qibo documentation.
- Amazon Braket SDK documentation.

## How I Got Started

I got started in quantum computing by treating every new concept as two
questions: what is the smallest circuit that shows the idea, and what can I
measure after I run it? Benchmarking is a good doorway because it is practical.
You do not have to understand every theorem before you can learn something from
a timing table. You can start with one circuit, run it carefully, and then ask a
better question on the next pass.

If you are new to this area, that is a healthy way to begin. Build small
examples, keep notes, share your code, and do not be afraid to compare tools.
Quantum computing is still young enough that careful educational examples can
help the next person get started.
