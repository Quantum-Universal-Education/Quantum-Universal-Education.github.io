```
---
title: "Angle Embedding in Quantum Machine Learning: Why Input Scaling Matters"
layout: post
author: "Jaeuk Kim"
date: 2026-06-16
categories: ["Quantum Machine Learning", "Tutorial"]
tags: ["QML", "Angle Embedding", "Input Scaling", "Quantum Machine Learning", "UnitaryHack"]
---
```


# Angle Embedding in Quantum Machine Learning: Why Input Scaling Matters

Quantum machine learning, or QML, often begins with a simple question:

> How do we put classical data into a quantum circuit?

One common answer is **angle embedding**. In angle embedding, classical numbers are used as rotation angles for quantum gates.

For example, suppose we have three classical features:

```python
features = [0.1, 0.5, 1.2]
```

We can encode them into three qubits using rotation gates:

```text
qubit 0 → RY(0.1)
qubit 1 → RY(0.5)
qubit 2 → RY(1.2)
```

This method is simple and useful, but it has one important property:

> Quantum rotation gates are periodic.

Very large input values can wrap around the rotation period. As a result, different classical values may produce identical or very similar quantum-circuit responses.

This tutorial explains:

1. what angle embedding is,
2. why rotation-gate periodicity matters,
3. how large inputs can cause aliasing,
4. how to diagnose problematic input ranges,
5. and how bounded preprocessing can make QML workflows more stable.

---

## 1. What is angle embedding?

In classical machine learning, data is commonly represented as a vector.

For example, an image, sensor signal, or medical measurement may be represented as:

```python
features = [0.2, -1.4, 3.1, 0.7]
```

A quantum circuit cannot receive this vector in exactly the same way as a conventional neural network. We first need an **encoding method** that maps classical values to quantum operations.

Angle embedding is one of the simplest encoding methods. Each classical feature becomes the angle of a quantum rotation gate:

```text
x_i → RY(x_i)
```

For a four-dimensional input vector, a simple encoding circuit could apply one rotation to each qubit:

```text
RY(x_0) on qubit 0
RY(x_1) on qubit 1
RY(x_2) on qubit 2
RY(x_3) on qubit 3
```

The encoded quantum state can then be processed by parameterized gates and measured to produce a prediction.

---

## 2. Why are rotation gates periodic?

A rotation angle behaves like an angle on a circle.

For example:

```text
0 radians
2π radians
4π radians
```

represent zero, one full rotation, and two full rotations.

For an `RY`-encoded qubit measured with the Pauli-Z operator, the expectation value is:

```text
⟨Z⟩ = cos(x)
```

The cosine function is periodic:

```text
cos(x) = cos(x + 2πk)
```

where `k` is any integer.

Therefore, two classical values separated by `2π` can produce the same measured circuit response.

For small, carefully scaled values, this may not be a problem:

```python
features = [0.1, 0.3, 0.8]
```

However, unbounded values such as:

```python
features = [10.0, 100.0, 1000.0]
```

can wrap around the rotation period many times.

This can create an **aliasing problem**.

---

## 3. What is angle aliasing?

Aliasing occurs when different input values become difficult or impossible to distinguish after encoding.

Consider these two values:

```python
import numpy as np

a = 0.1
b = 0.1 + 2 * np.pi
```

They are different classical values, but they produce the same Pauli-Z expectation value after a single `RY` rotation:

```python
np.cos(a) == np.cos(b)
```

Because of periodic wrapping, a quantum model may not preserve the original distance or ordering between large classical values.

This issue is especially relevant when the input comes from:

* raw neural-network activations,
* unnormalized datasets,
* score-based generative models,
* sensor values with large dynamic ranges,
* optimization variables without known bounds,
* or any classical feature that can grow without a fixed limit.

Angle aliasing is not necessarily an error in the quantum circuit. It is a consequence of combining unbounded classical inputs with periodic quantum operations.

---

## 4. A bounded preprocessing strategy

One way to reduce repeated angle wrapping is to bound the input before applying angle embedding.

A simple transformation is:

```python
angles = np.pi * np.tanh(features)
```

The hyperbolic tangent maps any real-valued input into:

```text
(-1, 1)
```

Multiplying by `π` maps the values into:

```text
(-π, π)
```

This ensures that the encoded values remain within one controlled angular interval.

```python
import numpy as np

features = np.array(
    [-100.0, -10.0, -1.0, 0.0, 1.0, 10.0, 100.0]
)

bounded_angles = np.pi * np.tanh(features)

print(bounded_angles)
```

This is not a universal solution for every QML task. The transformation also compresses very large values near `-π` or `π`, which may remove some magnitude information.

It should therefore be treated as one possible preprocessing strategy rather than a mandatory rule.

Other possible approaches include:

* standardization,
* min-max scaling,
* clipping,
* learned scaling parameters,
* data-dependent feature maps,
* and problem-specific normalization.

---

## 5. Diagnosing the input scale

Before applying angle embedding, it is useful to inspect the feature distribution.

A simple diagnostic is:

```python
import numpy as np

fraction_over_pi = np.mean(np.abs(features) > np.pi)
fraction_over_2pi = np.mean(np.abs(features) > 2 * np.pi)

print("Fraction over π:", fraction_over_pi)
print("Fraction over 2π:", fraction_over_2pi)
```

You can also inspect the maximum and median absolute values:

```python
print("Maximum magnitude:", np.max(np.abs(features)))
print("Median magnitude:", np.median(np.abs(features)))
```

A large fraction of values above `π` or `2π` does not automatically prove that the model will fail.

However, it indicates that the circuit receives values spanning multiple rotation periods and that aliasing should be investigated.

---

## 6. Running the PennyLane quantum-circuit demo

The complete example included with this tutorial uses PennyLane to create a one-qubit quantum circuit.

Each feature is encoded using an `RY` rotation, and the circuit measures the expectation value of the Pauli-Z operator.

```python
import pennylane as qml

device = qml.device("default.qubit", wires=1)


@qml.qnode(device)
def angle_embedding_response(angle: float) -> float:
    qml.RY(angle, wires=0)
    return qml.expval(qml.PauliZ(0))
```

The complete script compares:

* raw input angles,
* raw angles wrapped into `[-π, π)`,
* bounded angles produced by `π × tanh(x)`,
* quantum-circuit responses produced by raw angles,
* and quantum-circuit responses produced by bounded angles.

Install the required packages:

```bash
pip install -r assets/quantum_programs/angle_embedding_qml/requirements.txt
```

Run the example:

```bash
python assets/quantum_programs/angle_embedding_qml/angle_embedding_demo.py
```

The script prints diagnostic values and saves a comparison figure.

![Angle embedding input-scaling comparison](/assets/quantum_programs/angle_embedding_qml/angle_embedding_input_scaling_demo.png)

[View the complete Python example](/assets/quantum_programs/angle_embedding_qml/angle_embedding_demo.py)

---

## 7. Understanding the result

The upper part of the generated figure compares the angles entering the circuit.

The raw angles repeatedly wrap between `-π` and `π` as the input value increases. This produces an oscillating pattern because increasingly large feature values cross multiple rotation periods.

The bounded transformation:

```python
np.pi * np.tanh(features)
```

produces a smooth and monotonic mapping into `(-π, π)`.

The lower part of the figure compares the corresponding Pauli-Z expectation values.

With raw angles, the circuit response oscillates repeatedly because:

```text
⟨Z⟩ = cos(x)
```

With bounded angles, the input remains within one controlled angular interval and avoids repeated wrapping across multiple periods.

The bounded response may still saturate for very large positive or negative inputs. This illustrates an important trade-off:

* raw encoding preserves the unbounded numerical value but can alias repeatedly,
* bounded encoding avoids repeated wrapping but compresses extreme values.

The correct choice depends on the application and the meaning of the features.

---

## 8. Why this matters in hybrid QML

A typical hybrid classical-quantum model may look like this:

```text
classical neural network
        ↓
feature vector
        ↓
input scaling
        ↓
angle embedding
        ↓
variational quantum circuit
        ↓
measurement
        ↓
prediction
```

The classical network may produce features with a much larger range than the quantum circuit expects.

If those values are passed directly into rotation gates, the quantum layer may receive highly aliased representations.

In this situation, changing the quantum ansatz or adding more trainable parameters may not solve the underlying encoding problem.

The input transformation should therefore be treated as part of the quantum-model architecture.

---

## 9. Practical checklist

Before using angle embedding in a QML model, ask:

* Are the input features normalized?
* Can the feature values become unbounded?
* What are the maximum and median feature magnitudes?
* How many values exceed `π` or `2π`?
* Does the quantum response change smoothly with the input?
* Are different classical inputs producing nearly identical measurements?
* Would standardization or min-max scaling be sufficient?
* Would a bounded transformation such as `π × tanh(x)` be appropriate?
* Does bounding the inputs cause excessive saturation?
* Have the preprocessing choices been compared experimentally?

It is also important to compare the quantum model against a suitable classical baseline.

A performance difference should not automatically be attributed to the use of a quantum circuit if the models use different parameter counts, preprocessing steps, or architectural roles.

---

## 10. Dependencies

The runnable example requires:

* NumPy
* Matplotlib
* PennyLane

Install the dependencies listed for the tutorial:

```bash
pip install -r assets/quantum_programs/angle_embedding_qml/requirements.txt
```

The `requirements.txt` file should contain:

```text
numpy
matplotlib
pennylane
```

---

## 11. Video demonstration

A short video walkthrough should demonstrate:

1. the angle-embedding concept,
2. the periodic behavior of rotation gates,
3. the raw and bounded input values,
4. execution of the PennyLane example,
5. and interpretation of the generated figure.

Replace `VIDEO_URL` with a public or unlisted video link before submitting the pull request.

[Watch the video demonstration](VIDEO_URL)

---

## 12. AI assistance disclosure

ChatGPT was used to assist with:

* organizing the tutorial structure,
* improving educational wording,
* reviewing the Markdown formatting,
* and drafting portions of the example code.

The contributor manually reviewed, edited, executed, and verified the final tutorial and code.

---

## 13. Personal note

I became interested in this topic while researching how variational quantum circuits can be integrated into machine-learning and generative-model pipelines.

One lesson from this work is that QML is not only about adding quantum circuits to classical models. It is also necessary to understand how classical information enters the quantum circuit.

Angle embedding appears simple, but the scale and distribution of its input features can strongly affect the behavior of the quantum model.

For beginners, the main lesson is:

> In quantum machine learning, data preprocessing is part of the quantum-model design.
