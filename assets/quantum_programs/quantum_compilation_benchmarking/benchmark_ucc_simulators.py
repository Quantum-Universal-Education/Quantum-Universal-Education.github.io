"""Benchmark one UCC-style unoptimized circuit across five simulators.

This script accompanies the Quantum Universal Education tutorial:
"Quantum Compilation Benchmarking With Five Simulators".

The benchmark intentionally starts from one neutral gate list and then imports
that same unoptimized circuit description into each simulator backend. The
gate list is not a chemistry-grade UCCSD ansatz. It is a student-sized
UCC-inspired compilation benchmark: excitation-like two-qubit rotations are
repeated in layers so the circuit grows with both qubit count and depth.

Run a quick benchmark:

    python benchmark_ucc_simulators.py --qubits 10 12 --depths 2 4 --shots 256

The script skips a simulator if its optional dependency is not installed.
Install all dependencies with:

    pip install -r requirements.txt
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


Gate = tuple[str, tuple[int, ...], tuple[float, ...]]


@dataclass(frozen=True)
class BenchmarkCase:
    qubits: int
    depth: int
    gates: list[Gate]


def build_ucc_style_gate_list(qubits: int, depth: int) -> list[Gate]:
    """Return a neutral circuit description shared by every simulator.

    Each layer has:

    - single-qubit rotations, which model variational parameters;
    - nearest-neighbor entanglers, which model excitation couplings;
    - a second staggered entangler pass so depth changes are visible.

    Keeping the circuit as plain Python tuples lets students see that every
    simulator receives the same unoptimized program before timing begins.
    """

    if qubits < 2:
        raise ValueError("The benchmark needs at least two qubits.")
    if depth < 1:
        raise ValueError("Depth must be positive.")

    gates: list[Gate] = []
    for layer in range(depth):
        for q in range(qubits):
            theta = 0.031 * (layer + 1) * (q + 1)
            gates.append(("ry", (q,), (theta,)))
            gates.append(("rz", (q,), (theta / 2,)))

        for q in range(0, qubits - 1, 2):
            angle = 0.019 * (layer + 1) * (q + 1)
            gates.extend(
                [
                    ("cx", (q, q + 1), ()),
                    ("rz", (q + 1,), (angle,)),
                    ("cx", (q, q + 1), ()),
                ]
            )

        for q in range(1, qubits - 1, 2):
            angle = 0.013 * (layer + 1) * (q + 1)
            gates.extend(
                [
                    ("cx", (q, q + 1), ()),
                    ("ry", (q + 1,), (angle,)),
                    ("cx", (q, q + 1), ()),
                ]
            )

    return gates


def time_once(func: Callable[[], object]) -> float:
    start = time.perf_counter()
    func()
    return time.perf_counter() - start


def run_repeated(func: Callable[[], object], repeats: int) -> tuple[float, float]:
    samples = [time_once(func) for _ in range(repeats)]
    return statistics.median(samples), min(samples)


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
        else:
            raise ValueError(name)
    circuit.measure_all()
    backend = AerSimulator(method="statevector")
    return backend.run(circuit, shots=shots).result()


def run_cirq(case: BenchmarkCase, shots: int) -> object:
    import cirq

    qubits = cirq.LineQubit.range(case.qubits)
    circuit = cirq.Circuit()
    for name, ids, params in case.gates:
        if name == "ry":
            circuit.append(cirq.ry(params[0])(qubits[ids[0]]))
        elif name == "rz":
            circuit.append(cirq.rz(params[0])(qubits[ids[0]]))
        elif name == "cx":
            circuit.append(cirq.CNOT(qubits[ids[0]], qubits[ids[1]]))
        else:
            raise ValueError(name)
    circuit.append(cirq.measure(*qubits, key="m"))
    return cirq.Simulator().run(circuit, repetitions=shots)


def run_pennylane(case: BenchmarkCase, shots: int) -> object:
    import pennylane as qml

    dev = qml.device("default.qubit", wires=case.qubits, shots=shots)

    @qml.qnode(dev)
    def circuit():
        for name, qubits, params in case.gates:
            if name == "ry":
                qml.RY(params[0], wires=qubits[0])
            elif name == "rz":
                qml.RZ(params[0], wires=qubits[0])
            elif name == "cx":
                qml.CNOT(wires=[qubits[0], qubits[1]])
            else:
                raise ValueError(name)
        return qml.sample(wires=range(case.qubits))

    return circuit()


def run_qibo(case: BenchmarkCase, shots: int) -> object:
    from qibo import Circuit, gates

    circuit = Circuit(case.qubits)
    for name, qubits, params in case.gates:
        if name == "ry":
            circuit.add(gates.RY(qubits[0], theta=params[0]))
        elif name == "rz":
            circuit.add(gates.RZ(qubits[0], theta=params[0]))
        elif name == "cx":
            circuit.add(gates.CNOT(qubits[0], qubits[1]))
        else:
            raise ValueError(name)
    circuit.add(gates.M(*range(case.qubits)))
    return circuit(nshots=shots)


def run_braket(case: BenchmarkCase, shots: int) -> object:
    from braket.circuits import Circuit
    from braket.devices import LocalSimulator

    circuit = Circuit()
    for name, qubits, params in case.gates:
        if name == "ry":
            circuit.ry(qubits[0], params[0])
        elif name == "rz":
            circuit.rz(qubits[0], params[0])
        elif name == "cx":
            circuit.cnot(qubits[0], qubits[1])
        else:
            raise ValueError(name)
    return LocalSimulator("default").run(circuit, shots=shots).result()


SIMULATORS: dict[str, Callable[[BenchmarkCase, int], object]] = {
    "qiskit_aer": run_qiskit,
    "cirq": run_cirq,
    "pennylane_default_qubit": run_pennylane,
    "qibo": run_qibo,
    "braket_local": run_braket,
}


def benchmark(
    qubits: Iterable[int],
    depths: Iterable[int],
    simulators: Iterable[str],
    shots: int,
    repeats: int,
    warmups: int,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for n in qubits:
        for d in depths:
            case = BenchmarkCase(n, d, build_ucc_style_gate_list(n, d))
            for name in simulators:
                runner = SIMULATORS[name]
                status = "ok"
                median = best = math.nan
                error = ""
                try:
                    for _ in range(warmups):
                        runner(case, shots)
                    median, best = run_repeated(lambda: runner(case, shots), repeats)
                except Exception as exc:  # optional packages and hardware vary.
                    status = "skipped"
                    error = f"{type(exc).__name__}: {exc}"
                rows.append(
                    {
                        "simulator": name,
                        "qubits": str(n),
                        "depth": str(d),
                        "gate_count": str(len(case.gates)),
                        "shots": str(shots),
                        "repeats": str(repeats),
                        "warmups": str(warmups),
                        "median_seconds": "" if math.isnan(median) else f"{median:.6f}",
                        "best_seconds": "" if math.isnan(best) else f"{best:.6f}",
                        "status": status,
                        "error": error,
                    }
                )
    return rows


def write_csv(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qubits", nargs="+", type=int, default=[10, 12, 14])
    parser.add_argument("--depths", nargs="+", type=int, default=[2, 4, 8])
    parser.add_argument("--shots", type=int, default=512)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument(
        "--warmups",
        type=int,
        default=1,
        help="Untimed warmup runs per simulator/case. Use 0 to include first-run import/cache costs.",
    )
    parser.add_argument(
        "--simulators",
        nargs="+",
        choices=sorted(SIMULATORS),
        default=sorted(SIMULATORS),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("ucc_simulator_benchmark_results.csv"),
    )
    args = parser.parse_args()

    rows = benchmark(
        args.qubits,
        args.depths,
        args.simulators,
        args.shots,
        args.repeats,
        args.warmups,
    )
    write_csv(rows, args.output)

    ok = sum(row["status"] == "ok" for row in rows)
    skipped = len(rows) - ok
    print(f"Wrote {len(rows)} benchmark rows to {args.output}")
    print(f"Successful rows: {ok}; skipped rows: {skipped}")
    for row in rows:
        print(
            f"{row['simulator']:24s} n={row['qubits']:>2s} depth={row['depth']:>2s} "
            f"median={row['median_seconds'] or '-':>10s}s status={row['status']}"
        )


if __name__ == "__main__":
    main()
