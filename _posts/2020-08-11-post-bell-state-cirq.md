---
title: Bell State in Cirq
categories:
  - Blog
tags:
  - jupyter notebook
  - Cirq
  - Bell State
  - Python
  - quantum programming
author: Alberto Maldonado Romo
---

# About Cirq

Cirq is a software library for writing, manipulating, and optimizing quantum circuits and then running them against quantum computers and simulators. Cirq attempts to expose the details of hardware, instead of abstracting them away, because, in the Noisy Intermediate-Scale Quantum (NISQ) regime, these details determine whether or not it is possible to execute a circuit at all.

# Installation
The official link https://cirq.readthedocs.io/en/stable/install.html has the comands to install in Docker and Windows/Linux/Mac Os X distributions.

# Bell State

The simplest example for quantum computation is to generate a Bell state from the controlled-not gate to or Cnot with a previous superposition of the qubit and control with the Hadamard gate.

![bell_state.png](/assets/quantum_programs/bell_state/cirq/Images/bell_state.png)

# Program

The cirq code to perform the previously mentioned state of bell is described.


```python
import cirq # call the library


q0 = cirq.GridQubit(0, 0) # call the qubit (0,0)
q1 = cirq.GridQubit(0, 1) # call the qubit (0,1)


circuit = cirq.Circuit() # call the method circuit


circuit.append(cirq.H(q0)) # adder  in the circuit the Hadamard gate in q0 
circuit.append(cirq.CX(q0,q1)) # adder in the circuit the CX or Cnot gate between q0 and q1

circuit.append(cirq.measure(q0, key='m0'))  # adder the measure in q0
circuit.append(cirq.measure(q1, key='m1')) # adder the measure in q1

print("Circuit:")
print(circuit) # print the circuit at this moment

# Simulate the circuit.

shots = 100 # number of shots in the simulation
simulator = cirq.Simulator() # call the Simulator method
result = simulator.run(circuit, repetitions=shots) # run the circuit in shots time (100 times)
print("Results:")
print(result) # show the results
```

    Circuit:
    (0, 0): ───H───@───M('m0')───
                   │
    (0, 1): ───────X───M('m1')───
    Results:
    m0=1110000011000110110110100000111011001101111011000101011001000000011111010110111100100110100010101011
    m1=1110000011000110110110100000111011001101111011000101011001000000011111010110111100100110100010101011



```python
counts = cirq.plot_state_histogram(result) # cal the method to generate a plot 
print("Probabiity =", counts/shots) # print the probabilities of every qubit_state
```


![png](/assets/quantum_programs/bell_state/cirq/Bell_state_cirq_files/Bell_state_cirq/Bell_state_cirq_5_0.png)


    Probabiity = [0.49 0.   0.   0.51]

