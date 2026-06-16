"""
Angle Embedding Input Scaling Demo

This demo shows why input scaling matters in angle-based quantum feature
encoding. Rotation gates are periodic, so very large input values can wrap
around the rotation period and create aliasing.

Run:
    python angle_embedding_demo.py
"""

import numpy as np
import matplotlib.pyplot as plt


def bounded_angle_preprocessing(features: np.ndarray) -> np.ndarray:
    """Map unbounded features into (-pi, pi)."""
    return np.pi * np.tanh(features)


def wrapped_angle(angles: np.ndarray) -> np.ndarray:
    """Wrap angles into the interval (-pi, pi]."""
    return (angles + np.pi) % (2 * np.pi) - np.pi


def main() -> None:
    features = np.array([-100.0, -10.0, -3.0, -1.0, 0.0, 1.0, 3.0, 10.0, 100.0])

    raw_angles = features
    bounded_angles = bounded_angle_preprocessing(features)

    raw_wrapped = wrapped_angle(raw_angles)

    print("Original features:")
    print(features)

    print("\nRaw angles:")
    print(raw_angles)

    print("\nRaw angles after wrapping to (-pi, pi]:")
    print(np.round(raw_wrapped, 4))

    print("\nBounded angles using pi * tanh(x):")
    print(np.round(bounded_angles, 4))

    print("\nMaximum absolute bounded angle:")
    print(np.max(np.abs(bounded_angles)))

    print("\nFraction of raw angles larger than pi:")
    print(np.mean(np.abs(raw_angles) > np.pi))

    print("\nFraction of bounded angles larger than pi:")
    print(np.mean(np.abs(bounded_angles) > np.pi))

    plt.figure(figsize=(8, 5))
    plt.plot(features, raw_wrapped, marker="o", label="Raw angles wrapped to (-pi, pi]")
    plt.plot(features, bounded_angles, marker="s", label="Bounded angles: pi * tanh(x)")
    plt.axhline(np.pi, linestyle="--", linewidth=1, label="pi")
    plt.axhline(-np.pi, linestyle="--", linewidth=1, label="-pi")
    plt.xlabel("Input feature value")
    plt.ylabel("Encoded angle")
    plt.title("Angle Embedding: Raw Wrapping vs Bounded Preprocessing")
    plt.legend()
    plt.tight_layout()
    plt.savefig("angle_embedding_input_scaling_demo.png", dpi=150)

    print("\nSaved plot: angle_embedding_input_scaling_demo.png")


if __name__ == "__main__":
    main()
