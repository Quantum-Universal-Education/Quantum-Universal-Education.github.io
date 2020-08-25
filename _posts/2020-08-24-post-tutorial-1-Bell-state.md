---
title: Tutorial 1: Bell State
categories:
  - Blog
tags:
  - jupyter notebook
  - Qiskit
  - Cirq
  - QDK
  - Silq
  - Strawberry Fields
  - Hello World
  - Python
  - quantum programming
author: Alberto Maldonado Romo
---

# Quantum Entanglement between Two Qubits


"The Bell state, $\left|x_{1} x_{2}\right\rangle=\frac{1}{\sqrt{2}}|00\rangle+\frac{1}{\sqrt{2}}|11\rangle$, is of particular interest: if we pick any of the two qubits to measure, we would obtain outcome j0i or j1i with equal probability; and the other qubit is guaranteed to be measured in the same state as the first. This “correlation” between the two qubits are called quantum entanglement. However, this is not to be confused with two correlated random bits each with equal probability of being observed |0> or |1> . 
Proof of the distinction is omitted for the sake of brevity; we refer the interested reader to
the studies on “local hidden variables” theory, Bell’s inequality, and the CHSH
game. In essence, the measurement of one qubit intrinsically alters and determines the
state of the other. Perhaps even more surprising is that these two qubits can be physically
far apart as long as they were previous entangled as a Bell state. To form such a relationship
between the two qubits, they must interact with each other, either directly through a two-
qubit gate as shown above, or indirectly through a photon or a third qubit *(Ding (2020),Chong (2020),
University of Chicago, book,Quantum Computer Systems: Research for Noisy Intermediate-Scale Quantum Computers
Synthesis Lectures on Computer Architecture)*".




The simplest example for quantum computation is to generate a Bell state from the controlled-not gate to or Cnot with a previous superposition of the qubit and control with the Hadamard gate.

![bell_state.png](/assets/quantum_programs/1_bell_state/bell_state.png)

# Qiskit Program
The cirq code to perform the previously mentioned state of bell is described.


```python
import qiskit
from qiskit.quantum_info import Statevector # the state vector of the required qubits is generated
from qiskit.visualization import plot_state_qsphere # plot the qubits in a qsphere

sv = Statevector.from_label('00') # show the input state 00
plot_state_qsphere(sv.data)  #plot the previous state
```




![png](/assets/quantum_programs/1_bell_state/output_2_0.png)




```python
mycircuit = qiskit.QuantumCircuit(2,2)# generate the circuit's bell state 
mycircuit.h(0)
mycircuit.cx(0,1)
mycircuit.draw('mpl')
```




![png](/assets/quantum_programs/1_bell_state/output_3_0.png)




```python
new_sv = sv.evolve(mycircuit) # show the output vector state 
print(new_sv)
plot_state_qsphere(new_sv.data) # show the plot of  the output qubits
```

    Statevector([0.70710678+0.j, 0.        +0.j, 0.        +0.j,
                 0.70710678+0.j],
                dims=(2, 2))





![png](/assets/quantum_programs/1_bell_state/output_4_1.png)




```python
counts = new_sv.sample_counts(shots=1000) # simulate  with 1000 iterations

from qiskit.visualization import plot_histogram
plot_histogram(counts) # plot the output istogram
```




![png](/assets/quantum_programs/1_bell_state/output_5_0.png)



### Qiskit Real Quantum Computing 

Generate the same circuit on a real quantum computing that use 15 qubits.


```python
qiskit.IBMQ.load_account() # load the token
provider = qiskit.IBMQ.get_provider('ibm-q') # select the provider
backend = provider.get_backend('ibmq_16_melbourne') # select the name of the quatum computer to use
print("real device:",backend.name())
```

    real device: ibmq_16_melbourne



```python
mycircuit.measure([0,1],[0,1]) # we apply the measurement 
job = qiskit.execute( mycircuit, backend)
result = job.result()
counts =result.get_counts(mycircuit) # obtain he output values
print("counts: ", counts ) # show the result
```

    counts:  {'01': 47, '00': 502, '11': 442, '10': 33}



```python
qiskit.visualization.plot_histogram(counts) # plot the histogram 
```




![png](/assets/quantum_programs/1_bell_state/output_9_0.png)



# Cirq Program
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
    m0=0001000110111001000100001000101111100110101111010100101000011000000101101011101111010110001111001011
    m1=0001000110111001000100001000101111100110101111010100101000011000000101101011101111010110001111001011



```python
counts = cirq.plot_state_histogram(result) # cal the method to generate a plot 
```


![png](/assets/quantum_programs/1_bell_state/output_12_0.png)



```python
print("Probabiity =", counts/shots) # print the probabilities of every qubit_state
```

    Probabiity = [0.51 0.   0.   0.49]


# QDK Program
The QDK (using Q#) code to perform the previously mentioned state of bell is described.


```python
open Microsoft.Quantum.Canon;
open Microsoft.Quantum.Intrinsic;

operation SetQubitState(desired : Result, target : Qubit) : Unit {
    if (desired != M(target)) { // change the target qubit with the  desired value
        X(target);
    }
}

@EntryPoint()
operation TestBellState(count : Int, initial : Result) : (Int, Int) { // generate the Bell State
    mutable numOnes = 0;  // vriable to count  
    using (qubit = Qubit()) {  // call a qubit

    for (test in 1..count) { // for from 1 to 1000
        SetQubitState(initial, qubit); // call the  function with (Zero/One,qubit)
        H(qubit); // superposition of the value
        let res = M(qubit); // measurement  the value of the quit

        // Count the number of ones we saw:
         if (res == One) {
               set numOnes += 1;
                }
            }

            SetQubitState(Zero, qubit);
        }

    // Return number of times we saw a |0> and number of times we saw a |1>
    return (count - numOnes, numOnes); 
    }
```

    /snippet:(1,94): warning QS6003: The namespace is already open.
    /snippet:(2,10): warning QS6003: The namespace is already open.





<ul><li>SetQubitState</li><li>TestBellState</li></ul>




```python
operation BellState(): Unit{
    let (nZero,nOne) = TestBellState(1000,Zero); // call the function with 1000 iterations and flag to detect Zero state
    Message($"Probablity of obtain the state |00> :{nZero} ");// print results
    Message($"Probablity of obtain the state |11> :{nOne} ");

}
```




<ul><li>BellState</li></ul>




```python
%simulate BellState
```

    Probablity of obtain the state |00> :510 
    Probablity of obtain the state |11> :490 





    ()



# Silq Program


The silq code to perform the previously mentioned state of bell is described.

## Introduction to Silq


For this first example we must take into account the following properties of the silq language:


### B type variables are Boolean variables.



```python
x := false:B; // variable boolean x with the value in False

// x, means variable name
// :=, means  assignment 
// false, means value in false;
// :B, indicates the type of false value
```

### Apply pre-defined functions


```python
x := H(x); // the Hadamard gate is applied to the boolean variable x and assigned to the same variable x

// x, means variable name
```

### Generate a function


```python
def classicalExample(x:𝔹,f:𝔹->𝔹){ // generate a examle function that has a boolean variable x 
                                    //and function f that  Boolean mapping to another Boolean
  return f(x);              // return the function f
}
```

To know more about the documentation  check the following link : https://silq.ethz.ch/documentation

## Generate cnot function

To generate the denied controlled gate it is necessary to indicate two boolean variables: x,y where x represents the control qubit and if it is true it denies the variable y.


```python
// B means the boolean type 
// const mens constant value in this case in the boolean variable x

def cnot(const x:B,y:B):B{ //generate the function Cnot gate
  if x{  // if x is true  apply the sentence inside the {} 
    y := X(y);  // apply X gate in the boolean variable x
  }
  return y; // return the only 
}
```

## Define main function

We initialize the boolean variables x,y in false or zero state, to the variable x we apply the Hadamard gate, followed by the cnot function where x is the control qubit over the qubit y. Finally, we measure and return the values of the qubits (obtaining their classic values from the two qubits used in the program).



```python
def main(){ // main function

  x := false:B;    // A boolean (B type) variable x is initialized in false or zero state (|0>)
  y := false:B;    // A boolean (B type) variable x is initialized in false or zero state (|0>)
  x := H(x);       // Applying Hadamard to the boolean variable x
  y := cnot(x,y);  // It called the function cnot(x,y)
  return  measure(x,y);  // return the measure by the x and y variables or qubits.
}
```

## Expected outputs


```python
(1,1)
 or
(0,0)
```

The previous silq code is in the file called bell_state.sql

# Strawberry Fields


The strawberry fields code to perform the previously mentioned state of bell is described.



```python
import strawberryfields as sf
from strawberryfields import ops
```


```python
# create a quantum program with 3 qubits
prog = sf.Program(2)

# describe the circuit 
with prog.context as q:
    ops.Rgate(1.57) | q[0] # call the Sgate 
    ops.CXgate() | (q[0], q[1]) # call the BSGate
    ops.MeasureFock() | q # perform the measurement on all qubits of the variable q 

prog.print()
eng = sf.Engine("fock", backend_options={"cutoff_dim": 5}) # generate the simulation
result = eng.run(prog)
print(result.state)
state = result.state
state.trace()
state.dm().shape # density matrix
result.samples #print the output states
```

    Rgate(1.57) | (q[0])
    CXgate(1) | (q[0], q[1])
    MeasureFock | (q[0], q[1])
    <FockState: num_modes=2, cutoff=5, pure=True, hbar=2>





    array([[0, 0]])


