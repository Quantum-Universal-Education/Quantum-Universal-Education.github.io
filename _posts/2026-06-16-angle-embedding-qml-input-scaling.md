---

title: "Angle Embedding in Quantum Machine Learning: Why Input Scaling Matters"
layout: post
author: Jaeuk Kim
date: 2026-06-16
categories: [Quantum Machine Learning, Tutorial]
tags: [QML, Angle Embedding, Input Scaling, Quantum Machine Learning, UnitaryHack]
----------------------------------------------------------------------------------

# Angle Embedding in Quantum Machine Learning: Why Input Scaling Matters

Quantum machine learning, or QML, often begins with a simple question:

> How do we put classical data into a quantum circuit?

One common answer is **angle embedding**. In angle embedding, classical numbers are used as rotation angles for quantum gates.

For example, if we have three classical features:

```python
features = [0.1, 0.5, 1.2]
```

we can encode them into three qubits using rotation gates:

```text
qubit 0 → Ry(0.1)
qubit 1 → Ry(0.5)
qubit 2 → Ry(1.2)
```

This is simple and useful, but it has one important detail:

> Rotation gates are periodic.

That means very large input values can wrap around and behave like smaller angles. If we do not scale our inputs carefully, different classical values may become difficult for the quantum circuit to distinguish.

This tutorial explains:

1. what angle embedding is,
2. why periodicity matters,
3. how large inputs can cause aliasing,
4. and how simple input scaling can make QML workflows more stable.

---

## 1. What is angle embedding?

In classical machine learning, data is usually represented as vectors.

For example, an image, a sensor signal, or a medical measurement can be represented as numbers:

```python
x = [0.2, -1.4, 3.1, 0.7]
```

A quantum circuit cannot directly receive this vector in the same way as a neural network.
Instead, we need an **encoding method**.

Angle embedding is one of the simplest encoding methods.

It maps each classical feature to a quantum rotation:

```text
x_i → Ry(x_i)
```

This means the value of `x_i` becomes the angle of a rotation gate.

---

## 2. Why are rotation gates periodic?

A rotation gate behaves like an angle on a circle.

For example:

```text
0 radians
2π radians
4π radians
```

all represent full rotations around the circle.

This means that angles that differ by multiples of `2π` can produce very similar circuit behavior.

For small input values, this is usually not a problem.

```python
features = [0.1, 0.3, 0.8]
```

But if the input values are very large:

```python
features = [10.0, 100.0, 1000.0]
```

then the rotation gates may wrap around many times.

This can create an **aliasing** problem.

---

## 3. What is aliasing?

Aliasing happens when different input values become hard to distinguish after encoding.

For angle embedding, this can happen because rotation gates repeat every `2π`.

For example, these two values are different as classical numbers:

```python
a = 0.1
b = 0.1 + 2 * np.pi
```

But after angle embedding, they may produce very similar quantum rotations.

So the quantum circuit may not clearly distinguish `a` from `b`.

This is especially important when the input comes from:

* raw neural network activations,
* unnormalized data,
* score-based models,
* sensor values with large ranges,
* or any feature that is not bounded.

---

## 4. A simple bounded preprocessing idea

A simple way to avoid extremely large angles is to bound the input before angle embedding.

One possible transformation is:

```python
angles = np.pi * np.tanh(features)
```

This maps any real-valued input into the range:

```text
(-π, π)
```

This does not solve every QML problem, but it is a useful safety step when inputs may be very large.

---

## 5. Small Python demo

The following code compares raw input angles and bounded input angles.

```python
import numpy as np

features = np.array([-100.0, -10.0, -1.0, 0.0, 1.0, 10.0, 100.0])

raw_angles = features
bounded_angles = np.pi * np.tanh(features)

print("Original features:")
print(features)

print("\nRaw angles:")
print(raw_angles)

print("\nBounded angles using pi * tanh(x):")
print(bounded_angles)

print("\nMaximum absolute bounded angle:")
print(np.max(np.abs(bounded_angles)))
```

Expected result:

```text
The raw angles can become very large.
The bounded angles stay within approximately -π and π.
```

---

## 6. Why this matters in QML

In QML, we often combine classical neural networks with quantum circuits.

A typical hybrid model may look like this:

```text
classical neural network
        ↓
feature vector
        ↓
angle embedding
        ↓
quantum circuit
        ↓
measurement
        ↓
prediction
```

If the feature vector contains very large values, the angle embedding step may become unstable or less informative because of periodic wrapping.

Therefore, before using angle embedding, it is useful to check:

```python
np.max(np.abs(features))
```

and to consider scaling or bounding the input.

---

## 7. Practical checklist

Before using angle embedding in a QML model, ask:

* Are my input features normalized?
* Can the input values become very large?
* Are the values bounded to a known range?
* Do many values exceed `π` or `2π`?
* Should I use a preprocessing step such as standardization, min-max scaling, or `np.pi * np.tanh(x)`?

A simple diagnostic is:

```python
fraction_over_pi = np.mean(np.abs(features) > np.pi)
fraction_over_2pi = np.mean(np.abs(features) > 2 * np.pi)

print("Fraction over pi:", fraction_over_pi)
print("Fraction over 2pi:", fraction_over_2pi)
```

If many values are larger than `π` or `2π`, input scaling should be considered.

---

## 8. Dependencies

To run the simple demo, install:

```bash
pip install numpy matplotlib
```

If you want to extend this tutorial to a real QML framework, you can later add tools such as:

```bash
pip install pennylane
```

or:

```bash
pip install qiskit
```

However, this tutorial keeps the first example simple so that beginners can understand the core idea without requiring a quantum SDK.

---

## 9. AI assistance disclosure

This tutorial was drafted with assistance from ChatGPT for structure, wording, and educational clarity.
The final content was manually reviewed and edited by the contributor.

---

## 10. Personal note

I became interested in this topic while studying how quantum circuits can be combined with machine learning models.

One lesson I learned is that QML is not only about adding quantum circuits to neural networks.
It is also important to understand how classical data enters the quantum circuit.

Angle embedding looks simple, but input scaling can strongly affect how useful the encoded quantum features are.

For beginners, this is a useful reminder:

> In QML, data preprocessing is part of the quantum model design.
