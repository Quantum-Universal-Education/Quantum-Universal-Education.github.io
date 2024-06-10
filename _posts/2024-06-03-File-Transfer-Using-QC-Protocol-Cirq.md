# Quantum Communication: File Transfer Using Quantum Communication Protocol with Cirq

## Introduction

Welcome to this tutorial on quantum communication using Cirq! In this tutorial, we will explore the concept of quantum communication and how it can be used for secure file transfer. Quantum communication leverages the principles of quantum mechanics to enable secure communication protocols that are theoretically unbreakable. This tutorial is designed for high school and undergraduate students and will guide you step-by-step through the essential concepts and practical implementation of a quantum communication protocol using Python and Cirq.

## Prerequisites

Before we begin, you should have a basic understanding of the following topics:

- Basic Python programming
- Basic concepts in quantum mechanics (optional but helpful)
- Basic understanding of cryptography (optional but helpful)

## Learning Outcomes

By the end of this tutorial, you will:

- Understand the basics of quantum communication and its significance
- Learn about quantum key distribution (QKD) and the BB84 protocol
- Implement a simple quantum key distribution protocol using Cirq
- Understand how quantum key distribution can be used for secure file transfer

## Table of Contents

1. Introduction to Quantum Communication
2. Quantum Key Distribution (QKD)
3. The BB84 Protocol
4. Implementation of BB84 Protocol in Cirq
5. Secure File Transfer Using Quantum Keys
6. Conclusion and Further Reading

## 1. Introduction to Quantum Communication

Quantum communication uses quantum bits (qubits) to encode information, taking advantage of quantum properties such as superposition and entanglement. Unlike classical bits, which can be either 0 or 1, qubits can exist in multiple states simultaneously, providing a higher level of security.

### Key Concepts

- **Qubit**: The basic unit of quantum information, analogous to a classical bit. A qubit can be in a state |0⟩, |1⟩, or any quantum superposition of these states.
- **Superposition**: A fundamental principle of quantum mechanics where a qubit can be in a combination of both |0⟩ and |1⟩ states simultaneously. This property is what gives quantum computers their power.
- **Entanglement**: A quantum phenomenon where two qubits become linked, and the state of one qubit directly influences the state of another, no matter the distance between them. This property is crucial for quantum communication and quantum computing.

## 2. Quantum Key Distribution (QKD)

QKD is a method used to securely share encryption keys between two parties. It relies on the principles of quantum mechanics to ensure that any attempt to eavesdrop on the communication can be detected.

### Benefits of QKD

- **Unconditional security**: QKD security is based on the laws of physics rather than computational assumptions, making it theoretically unbreakable.
- **Eavesdropping detection**: Any attempt to intercept the key changes the quantum state, alerting the communicating parties and allowing them to discard the compromised bits.

## 3. The BB84 Protocol

The BB84 protocol, proposed by Charles Bennett and Gilles Brassard in 1984, is one of the first and most well-known QKD protocols. It uses two sets of bases to encode the qubits: rectilinear (0 and 1) and diagonal (+ and x).

### Steps of the BB84 Protocol

1. **Preparation**: The sender (Alice) prepares a random sequence of qubits using two bases (rectilinear and diagonal).
2. **Transmission**: Alice sends the qubits to the receiver (Bob) over a quantum channel.
3. **Measurement**: Bob measures the qubits using randomly chosen bases.
4. **Basis Reconciliation**: Alice and Bob compare their bases over a classical channel and discard mismatched results.
5. **Key Sifting**: The remaining bits form the raw key, which can be used for encryption.

## 4. Implementation of BB84 Protocol in Cirq

We will use the Python library Cirq to simulate the BB84 protocol. Ensure you have Cirq installed in your environment:

```bash
pip install cirq
```

### Step-by-Step Implementation

#### 1. Import Libraries

```python
import random
import cirq
```

#### 2. Generate Random Bits and Bases

In this step, we generate random bits and bases for Alice.

```python
def generate_random_bits(length):
    return [random.randint(0, 1) for _ in range(length)]

def generate_random_bases(length):
    return [random.choice(['Z', 'X']) for _ in range(length)]

n = 100  # Number of qubits
alice_bits = generate_random_bits(n)
alice_bases = generate_random_bases(n)
```

- **Random Bits**: These are the bits that Alice wants to encode in the qubits.
- **Random Bases**: These are the bases (Z or X) that Alice uses to encode the bits. The Z basis represents the standard computational basis (|0⟩ and |1⟩), and the X basis represents the diagonal basis (|+⟩ and |−⟩).

#### 3. Prepare Qubits

In this step, Alice prepares the qubits according to her bits and bases.

```python
def prepare_qubits(bits, bases):
    qubits = [cirq.GridQubit(0, i) for i in range(len(bits))]
    circuit = cirq.Circuit()
    for i, (bit, base) in enumerate(zip(bits, bases)):
        if bit == 1:
            circuit.append(cirq.X(qubits[i]))
        if base == 'X':
            circuit.append(cirq.H(qubits[i]))
    return qubits, circuit

qubits, alice_circuit = prepare_qubits(alice_bits, alice_bases)
```

- **cirq.GridQubit**: Represents a qubit on a 2D grid.
- **cirq.Circuit**: A quantum circuit that contains the operations (gates) applied to the qubits.
- **cirq.X**: A quantum gate that flips the state of a qubit (|0⟩ to |1⟩ and vice versa).
- **cirq.H**: A Hadamard gate that puts a qubit into superposition (from |0⟩ to |+⟩ and from |1⟩ to |−⟩).

#### 4. Simulate Transmission and Measurement

Bob receives the qubits and measures them using his own random bases.

```python
def measure_qubits(qubits, bases, circuit):
    simulator = cirq.Simulator()
    results = []
    for i, base in enumerate(bases):
        if base == 'X':
            circuit.append(cirq.H(qubits[i]))
        circuit.append(cirq.measure(qubits[i], key=f'm{i}'))
    result = simulator.run(circuit)
    for i in range(len(qubits)):
        results.append(result.measurements[f'm{i}'][0])
    return results

bob_bases = generate_random_bases(n)
bob_results = measure_qubits(qubits, bob_bases, alice_circuit)
```

- **cirq.Simulator**: A simulator to run quantum circuits.
- **cirq.measure**: A measurement operation on a qubit.

#### 5. Basis Reconciliation and Key Sifting

Alice and Bob compare their bases and sift the key.

```python
def sift_keys(alice_bases, bob_bases, alice_bits, bob_results):
    sifted_key = []
    for a_base, b_base, a_bit, b_bit in zip(alice_bases, bob_bases, alice_bits, bob_results):
        if a_base == b_base:
            sifted_key.append(a_bit)
    return sifted_key

sifted_key = sift_keys(alice_bases, bob_bases, alice_bits, bob_results)
print("Sifted Key:", sifted_key)
```

- **Sifted Key**: The key bits that were measured using the same basis by both Alice and Bob.

## 5. Secure File Transfer Using Quantum Keys

Now that we have a secure key, we can use it for secure file transfer. We will use symmetric encryption (e.g., the One-Time Pad) for this purpose.

### Symmetric Encryption Example

```python
def encrypt_decrypt(message, key):
    encrypted_decrypted = ''.join(chr(ord(c) ^ k) for c, k in zip(message, key))
    return encrypted_decrypted

# Convert sifted_key to a string of the same length as the message
message = "Hello, Quantum World!"
key = sifted_key[:len(message)]

# Encrypt the message
encrypted_message = encrypt_decrypt(message, key)
print("Encrypted Message:", encrypted_message)

# Decrypt the message
decrypted_message = encrypt_decrypt(encrypted_message, key)
print("Decrypted Message:", decrypted_message)
```

- **Symmetric Encryption**: A method of encryption where the same key is used for both encryption and decryption.
- **One-Time Pad**: A theoretically unbreakable encryption method where a random key is used only once.

## 6. Conclusion and Further Reading

Congratulations! You have successfully implemented a simple quantum key distribution protocol using the BB84 protocol and used it for secure file transfer. Quantum communication is a fascinating field with many real-world applications, from secure communications to quantum computing.

### Further Reading

- "Quantum Computation and Quantum Information" by Michael A. Nielsen and Isaac L. Chuang
- "Introduction to Quantum Mechanics" by David J. Griffiths
- [Cirq Documentation](https://quantumai.google/cirq)

### How I Got Started in Quantum Computing

I got started in quantum computing through my fascination with quantum mechanics and its potential applications in computing and cryptography. Learning about the fundamental

 principles of quantum mechanics and their implications for information processing was incredibly exciting. I hope this tutorial has inspired you to explore the field of quantum computing and its many possibilities.

### Resources and References

- [Cirq](https://quantumai.google/cirq)
- [Quantum Cryptography](https://en.wikipedia.org/wiki/Quantum_cryptography)
- [BB84 Protocol](https://en.wikipedia.org/wiki/BB84)

Feel free to contribute to this project and share your feedback. Happy coding!

## Full Code for Reference

Here is the complete code for the BB84 protocol implementation and secure file transfer:

```python
import random
import cirq

def generate_random_bits(length):
    return [random.randint(0, 1) for _ in range(length)]

def generate_random_bases(length):
    return [random.choice(['Z', 'X']) for _ in range(length)]

n = 100  # Number of qubits
alice_bits = generate_random_bits(n)
alice_bases = generate_random_bases(n)

def prepare_qubits(bits, bases):
    qubits = [cirq.GridQubit(0, i) for i in range(len(bits))]
    circuit = cirq.Circuit()
    for i, (bit, base) in enumerate(zip(bits, bases)):
        if bit == 1:
            circuit.append(cirq.X(qubits[i]))
        if base == 'X':
            circuit.append(cirq.H(qubits[i]))
    return qubits, circuit

qubits, alice_circuit = prepare_qubits(alice_bits, alice_bases)

def measure_qubits(qubits, bases, circuit):
    simulator = cirq.Simulator()
    results = []
    for i, base in enumerate(bases):
        if base == 'X':
            circuit.append(cirq.H(qubits[i]))
        circuit.append(cirq.measure(qubits[i], key=f'm{i}'))
    result = simulator.run(circuit)
    for i in range(len(qubits)):
        results.append(result.measurements[f'm{i}'][0])
    return results

bob_bases = generate_random_bases(n)
bob_results = measure_qubits(qubits, bob_bases, alice_circuit)

def sift_keys(alice_bases, bob_bases, alice_bits, bob_results):
    sifted_key = []
    for a_base, b_base, a_bit, b_bit in zip(alice_bases, bob_bases, alice_bits, bob_results):
        if a_base == b_base:
            sifted_key.append(a_bit)
    return sifted_key

sifted_key = sift_keys(alice_bases, bob_bases, alice_bits, bob_results)
print("Sifted Key:", sifted_key)

def encrypt_decrypt(message, key):
    encrypted_decrypted = ''.join(chr(ord(c) ^ k) for c, k in zip(message, key))
    return encrypted_decrypted

# Convert sifted_key to a string of the same length as the message
message = "Hello, Quantum World!"
key = sifted_key[:len(message)]

# Encrypt the message
encrypted_message = encrypt_decrypt(message, key)
print("Encrypted Message:", encrypted_message)

# Decrypt the message
decrypted_message = encrypt_decrypt(encrypted_message, key)
print("Decrypted Message:", decrypted_message)
