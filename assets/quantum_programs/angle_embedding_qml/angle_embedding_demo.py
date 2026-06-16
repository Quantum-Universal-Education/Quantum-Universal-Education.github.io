"""
Angle Embedding Input Scaling Demo

This tutorial demonstrates why input scaling matters in quantum machine
learning. Rotation gates are periodic, so large input values can wrap around
the rotation period and create repeated quantum circuit responses.

Run:
    python angle_embedding_demo.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pennylane as qml


def bounded_angle_preprocessing(features: np.ndarray) -> np.ndarray:
    """Map unbounded features into the interval (-pi, pi)."""
    return np.pi * np.tanh(features)


def wrapped_angle(angles: np.ndarray) -> np.ndarray:
    """Wrap angles into the interval [-pi, pi)."""
    return (angles + np.pi) % (2 * np.pi) - np.pi


# A one-qubit simulator for the angle-embedding demonstration.
device = qml.device("default.qubit", wires=1)


@qml.qnode(device)
def angle_embedding_response(angle: float) -> float:
    """Encode one feature with an RY gate and measure Pauli-Z."""
    qml.RY(angle, wires=0)
    return qml.expval(qml.PauliZ(0))


def evaluate_circuit(angles: np.ndarray) -> np.ndarray:
    """Evaluate the quantum circuit for every encoded angle."""
    return np.array(
        [float(angle_embedding_response(float(angle))) for angle in angles]
    )


def main() -> None:
    # Discrete examples for the printed diagnostics.
    sample_features = np.array(
        [-100.0, -10.0, -3.0, -1.0, 0.0, 1.0, 3.0, 10.0, 100.0]
    )

    raw_sample_angles = sample_features
    bounded_sample_angles = bounded_angle_preprocessing(sample_features)

    print("Original features:")
    print(sample_features)

    print("\nRaw angles:")
    print(raw_sample_angles)

    print("\nRaw angles wrapped into [-pi, pi):")
    print(np.round(wrapped_angle(raw_sample_angles), 4))

    print("\nBounded angles using pi * tanh(x):")
    print(np.round(bounded_sample_angles, 4))

    print("\nFraction of raw angles larger than pi:")
    print(np.mean(np.abs(raw_sample_angles) > np.pi))

    print("\nFraction of bounded angles larger than pi:")
    print(np.mean(np.abs(bounded_sample_angles) > np.pi))

    # Continuous values make the periodic circuit response easier to see.
    features = np.linspace(-20.0, 20.0, 401)

    raw_angles = features
    bounded_angles = bounded_angle_preprocessing(features)

    raw_responses = evaluate_circuit(raw_angles)
    bounded_responses = evaluate_circuit(bounded_angles)

    figure, axes = plt.subplots(2, 1, figsize=(9, 8))

    axes[0].plot(features, wrapped_angle(raw_angles), label="Raw angles, wrapped")
    axes[0].plot(features, bounded_angles, label="Bounded: pi * tanh(x)")
    axes[0].axhline(np.pi, linestyle="--", linewidth=1, label="pi")
    axes[0].axhline(-np.pi, linestyle="--", linewidth=1, label="-pi")
    axes[0].set_xlabel("Input feature")
    axes[0].set_ylabel("Encoded angle")
    axes[0].set_title("Angles Entering the Quantum Circuit")
    axes[0].legend()

    axes[1].plot(
        features,
        raw_responses,
        label="Quantum response with raw angles",
    )
    axes[1].plot(
        features,
        bounded_responses,
        label="Quantum response with bounded angles",
    )
    axes[1].set_xlabel("Input feature")
    axes[1].set_ylabel("Pauli-Z expectation value")
    axes[1].set_title("One-Qubit RY Angle-Embedding Response")
    axes[1].legend()

    figure.tight_layout()

    output_path = (
        Path(__file__).resolve().parent
        / "angle_embedding_input_scaling_demo.png"
    )
    figure.savefig(output_path, dpi=150)
    plt.close(figure)

    print(f"\nSaved plot: {output_path}")


if __name__ == "__main__":
    main()
