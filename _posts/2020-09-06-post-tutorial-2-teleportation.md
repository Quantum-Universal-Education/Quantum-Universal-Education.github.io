# Teleporting States


"In this section, we highlight a remarkable phenomenon called “quantum teleportation,” and its important applications in gate scheduling, namely a strategy called “gate teleportation,” in which scheduling gates is equivalent to scheduling resource states. We start by  writing down an important resource state, the  EPR pair $|\psi>$, which  can be  produced in the tutorial 1: Bell State.
The teleportation-based quantum computer (QC) architecture, require which such EPR pairs are utilized as resource states. Because both quantum states and quantum gates can be transferred over long distance via a teleportation circuit, this technique is particularly useful in distributed QC architectures or in reducing communication cost in general.*(Ding (2020),Chong (2020),
University of Chicago, book,Quantum Computer Systems: Research for Noisy Intermediate-Scale Quantum Computers
Synthesis Lectures on Computer Architecture)*".




![quantum_teleportation.png](Images/quantum_teleportation.png)

# Qiskit Program
The qiskit program is generated to pass the information from one qubit to another


```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer,execute, IBMQ
from qiskit.quantum_info import Statevector # the state vector of the required qubits is generated
#The variables are initialized to generate the quantum circuit
msg =  QuantumRegister(1) # infomration
Alice = QuantumRegister(1) # emisor
Bob = QuantumRegister(1) #receptor
key1 = ClassicalRegister(1) #condition one
key2 = ClassicalRegister(1) # condition two
output  = ClassicalRegister(1) # classical bit output
circuit = QuantumCircuit(msg,Alice, Bob, key1, key2, output) # genrate the quantum circuit
```

### Initial state for the msm
The qubit is rotated with the variable zero_state using the *initialize* method that indicates how much probability for the state |0> and for the state |1> (remember that the sum of the square module of those values must be equal to 1), to display the value of the input vector and check it is used the get_statevector method


```python
import numpy as np
zero_state = 0.25 # value in zero state

circuit.initialize([np.sqrt(zero_state), np.sqrt(1-zero_state)], msg) #obtain the value for msg variable
backend = Aer.get_backend('statevector_simulator') # simulate the previous circuit
job = execute(circuit, backend)
result = job.result()
print(result.get_statevector(circuit, decimals=3)) # show the vector output at this moment with 3 decimals
```

    [0.5      +0.j 0.8660254+0.j 0.       +0.j 0.       +0.j 0.       +0.j
     0.       +0.j 0.       +0.j 0.       +0.j]


### Generate the circuit

The circuit shown in the initial figure of this post is built.


```python
circuit.barrier() 
circuit.h(Alice) 
circuit.cx(Alice,Bob) # in this par of the circuit generate the bell state from tutorial number 1


circuit.barrier()
circuit.cx(msg, Alice)
circuit.h(msg)

circuit.barrier()
circuit.measure(msg, key1)
circuit.measure(Alice, key2) # at this point in the cycle the measurement of msg and Alice is generated 


circuit.z(Bob).c_if(key1, 1) # this command if the measure in key1 if is one then  in the Bob qubit apply a Z gate
circuit.x(Bob).c_if(key2, 1) # this command if the measure in key2 if is one then  in the Bob qubit apply a X gate
```




    <qiskit.circuit.instructionset.InstructionSet at 0x7f4f57eaad10>



### Show the circuit

show the circuit that at this moment representate the same circuit for the quantum teleportation


```python
circuit.draw()
```




<pre style="word-wrap: normal;white-space: pre;background: #fff0;line-height: 1.1;font-family: &quot;Courier New&quot;,Courier,monospace">      ┌─────────────────────────┐ ░            ░      ┌───┐ ░ ┌─┐          »
q0_0: ┤ initialize(0.5,0.86603) ├─░────────────░───■──┤ H ├─░─┤M├──────────»
      └─────────────────────────┘ ░ ┌───┐      ░ ┌─┴─┐└───┘ ░ └╥┘┌─┐       »
q1_0: ────────────────────────────░─┤ H ├──■───░─┤ X ├──────░──╫─┤M├───────»
                                  ░ └───┘┌─┴─┐ ░ └───┘      ░  ║ └╥┘ ┌───┐ »
q2_0: ────────────────────────────░──────┤ X ├─░────────────░──╫──╫──┤ Z ├─»
                                  ░      └───┘ ░            ░  ║  ║  └─┬─┘ »
                                                               ║  ║ ┌──┴──┐»
c0: 1/═════════════════════════════════════════════════════════╩══╬═╡ = 1 ╞»
                                                               0  ║ └─────┘»
c1: 1/════════════════════════════════════════════════════════════╩════════»
                                                                  0        »
c2: 1/═════════════════════════════════════════════════════════════════════»
                                                                           »
«             
«q0_0: ───────
«             
«q1_0: ───────
«       ┌───┐ 
«q2_0: ─┤ X ├─
«       └─┬─┘ 
«c0: 1/═══╪═══
«      ┌──┴──┐
«c1: 1/╡ = 1 ╞
«      └─────┘
«c2: 1/═══════
«             </pre>



### Produce the simulation result

Using the get_satevector method to verify the output vector changes, where the values were changed from qubit msg to qubit Bob


```python
backend = Aer.get_backend('statevector_simulator')
job = execute(circuit, backend)
result = job.result()
print(result.get_statevector(circuit, decimals=3))
```

    [ 0.       +0.00000000e+00j -0.       +0.00000000e+00j
      0.5      +0.00000000e+00j  0.       +0.00000000e+00j
      0.       +0.00000000e+00j  0.       +0.00000000e+00j
      0.8660254-1.06057524e-16j -0.       +0.00000000e+00j]


# Cirq Program
The cirq program is generated to pass the information from one qubit to another


```python
#call the libraries
import random
import numpy as np
import cirq

msg = cirq.GridQubit(0, 0) # call the qubit (0,0)
Alice = cirq.GridQubit(0, 1) # call the qubit (0,1)
Bob = cirq.GridQubit(0, 2)

zero_state = 0.25 # generate the value for th message i n the state 0
```

The information preparation of the qubit msg is generated and the vector you have up to this point is shown


```python
sim = cirq.Simulator()
q0 = cirq.LineQubit(0)
init_value =  cirq.Circuit() # generate a qubit
init_value.append(cirq.Y(msg)**(2*np.arccos(zero_state))) # rotate the qubit 
message = sim.simulate(init_value)


print(init_value) # show the circuit fro mthe qubit msg

print(message.final_state) # show the vector state from the circuit of init_value

expected = cirq.bloch_vector_from_state_vector(message.final_state,0)
print("x: ", np.around(expected[0], 4), "y: ", np.around(expected[1], 4),
          "z: ", np.around(expected[2], 4)) # show the rotation in the coordinate x,y and z
```

    (0, 0): ───Y^(7/11)───
    [0.2924804 +0.45490175j 0.45490175+0.7075196j ]
    x:  0.9098 y:  0.0 z:  -0.415


## Generate the circuit

Repeat the before cell and adder the circuit from the quantum teleportation image.


```python
circuit = cirq.Circuit() # call the method circuit

circuit.append(cirq.Y(msg)**(2*np.arccos(zero_state))) # initialize the qubit
circuit.append([cirq.H(Alice), cirq.CNOT(Alice, Bob)]) # generate the bell state from tutorial 1
circuit.append([cirq.CNOT(msg, Alice), cirq.H(msg)]) #
circuit.append(cirq.measure(msg, Alice)) # measure the msg and Alice qubits
circuit.append([cirq.CNOT(Alice, Bob), cirq.CZ(msg, Bob)]) # depend of the previous valures apply X or Z gate

print("Circuit:")
print(circuit) # print the circuit at this moment

# Simulate the circuit.

simulator = cirq.Simulator(seed=None) # call the Simulator method
```

    Circuit:
    (0, 0): ───Y^(7/11)───────@───H───M───────@───
                              │       │       │
    (0, 1): ───H──────────@───X───────M───@───┼───
                          │               │   │
    (0, 2): ──────────────X───────────────X───@───


Show the vector state


```python
answer =  simulator.simulate(circuit)
answer.final_state # final state show the vector final
```




    array([ 0.29248038+0.45490175j,  0.45490175+0.70751953j,
            0.        +0.j        ,  0.        +0.j        ,
            0.        +0.j        , -0.        +0.j        ,
            0.        +0.j        , -0.        +0.j        ], dtype=complex64)



Print the coordinate values from the qubit Bob and obtain the same rotation from the qubit msg


```python
result = cirq.bloch_vector_from_state_vector(answer.final_state,2)
print("x: ", np.around(result[0], 4), "y: ", np.around(result[1], 4),
          "z: ", np.around(result[2], 4))
```

    x:  0.9098 y:  -0.0 z:  -0.415


# QDK Program
The QDK (using Q#) program is generated to pass the information from one qubit to another.


```python
operation Teleport (msg : Qubit, Bob : Qubit) : Unit { // generate the circuit for the quantum teeportation

    using (Alice = Qubit()) {
        // Create the bell state to send the message.
        H(Alice);
        CNOT(Alice, Bob);

        
        CNOT(msg, Alice);
        H(msg);
        let key1 = M(msg);
        let key2 = M(Alice);

        // Depend of the values i nthe measure of key1 or key2 apply a specific gate
        if (key1 == One) { Z(Bob); }
        if (key2 == One) { X(Bob); }

        // Reset the "Alice" qubit.
        Reset(Alice);
    }
}

```




<ul><li>Teleport</li></ul>



Help functions to generate the random message qubit and validate that its value is teleported to Bob's qubit


```python
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;

    // The qubit value to |+⟩.
    operation SetToPlus(q: Qubit) : Unit {
        Reset(q);
        H(q);
    }

    // The qubitvalue to |−⟩.
    operation SetToMinus(q: Qubit) : Unit {
        Reset(q);
        X(q);
        H(q);
    }

    // if the quit is |+> return true
    operation IsPlus(q: Qubit) : Bool {
        return (Measure([PauliX], [q]) == Zero);
    }

    // # Summary
    // if the qubit is |-> (return true
    operation IsMinus(q: Qubit) : Bool {
        return (Measure([PauliX], [q]) == One);
    }

    // Generate a random rotation for the qubit msg
    operation PrepareRandomMessage(q: Qubit) : Unit {
        let choice = RandomInt(2);

        if (choice == 0) {
            Message("Sending |->");
            SetToMinus(q);
        } else {
            Message("Sending |+>");
            SetToPlus(q);
        }
    }
```

    /snippet:(1,94): warning QS6003: The namespace is already open.
    /snippet:(2,10): warning QS6003: The namespace is already open.





<ul><li>IsMinus</li><li>IsPlus</li><li>PrepareRandomMessage</li><li>SetToMinus</li><li>SetToPlus</li></ul>



Apply the quantum teleportation


```python
// generate the program
operation TeleportRandomMessage () : Unit {

    using (qubits = Qubit[2]) {

        //Identify the msg and Alice qubit
        let msg = qubits[0];
        let Bob = qubits[1];

        PrepareRandomMessage(msg); // generate a random value for msg qubit

        //Apply the quntum teleportation
        Teleport(msg, Bob);

        // Report the message received from Alice to Bob:
        if (IsPlus(Bob))  { Message("Received |+>"); }
        if (IsMinus(Bob)) { Message("Received |->"); }

        // Reset all of the qubits 
        ResetAll(qubits);
    }
}
```




<ul><li>TeleportRandomMessage</li></ul>



Run the quantum teleportation program in Q#


```python
%simulate TeleportRandomMessage
```

    Sending |->
    Received |->





    ()



# Silq Program

The silq program is generated to pass the information from one qubit to another.

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

# Generate  Teleportation Function
Apply the same structure for the image in the description,it is conditioned that the program is performed 100 times to verify that it is the same value of the message qubit


```python
def transport(){
  count := 0; // intege variable
  for i in [0..100){ // iteration from 0 to 99
     
      msg := 0:B;   // boolean variable to state in zero and reprsentate the message 
      Alice := 0:B; 
      Bob := 0:B;
      
      zero_state = 75;
      theta:=2·asin(1/sqrt(zero_state)); //prepare the  state
      msg := rotY(theta,msg);
      
      Alice := H(Alice); // generate the Bel state from the tutorial 1
      Bob := cx(Alice,Bob);
      Alice := cx(msg,Alice);
      msg := H(msg);
      
      msg := measure(msg); // measure the msg qubit
      Alice := measure(Alice); // measure Alice qubit
      
      if msg==1{ 
          Bob := Z(Bob); // if msg is 1 apply Z gate in  Bob gate
      }
      if Alice==1{
          Bob := X(Bob); // if msg is 1 apply Z gate in  Bob gate
      }

      Bob := measure(Bob);
      if Bob==1{ 
          count+= 1; // if Bob==1 add 1 to the variable count
      }

   }
    print(count); // print the value of the integer vaariable count
}
```

## Define main function

initialize the main function to the program, it calls the function transprot() and return a default value of return in 1


```python
def main(){ // main function
    transport();
    return  measure(1);
}
```

## Expected outputs

The program print the value of the count in the Bob qubit, this one is approximately  equal to the value of the variable zero_state, and below of this print the default reaturn that  we indicate as 1.


```python
75  // the value is the same from  the msg
(1)
```

The previous silq code is in the file called transform.sql

# Strawberry Fields


The strawberry fields  program is generated to pass the information from one qubit to another.

import the strawberryields libraries for generare the circuit and run it.


```python
import strawberryfields as sf
from strawberryfields.ops import *

# initialize engine and program objects
eng = sf.Engine(backend="gaussian")
prog = sf.Program(4)
```


```python
with prog.context as q:
    # create initial states
    Squeezed(0.1) | q[0]
    Squeezed(-2)  | q[1]
    Squeezed(-2)  | q[2]

    # apply the gate to be teleported
    Pgate(0.5) | q[1]

    # conditional phase entanglement
    CZgate(1) | (q[0], q[1])
    CZgate(1) | (q[1], q[2])

    # projective measurement onto
    # the position quadrature
    Fourier.H | q[0]
    MeasureX | q[0]
    Fourier.H | q[1]
    MeasureX | q[1]
    # compare against the expected output
    # X(q1/sqrt(2)).F.P(0.5).X(q0/sqrt(0.5)).F.|z>
    # not including the corrections
    Squeezed(0.1) | q[3]
    Fourier       | q[3]
    #Xgate(q[0])   | q[3]
    Pgate(0.5)    | q[3]
    Fourier       | q[3]
    ##Xgate(q[1])   | q[3]
    # end circuit
prog.print()
```

    Squeezed(0.1, 0) | (q[0])
    Squeezed(-2, 0) | (q[1])
    Squeezed(-2, 0) | (q[2])
    Pgate(0.5) | (q[1])
    CZgate(1) | (q[0], q[1])
    CZgate(1) | (q[1], q[2])
    Fourier.H | (q[0])
    MeasureX | (q[0])
    Fourier.H | (q[1])
    MeasureX | (q[1])
    Squeezed(0.1, 0) | (q[3])
    Fourier | (q[3])
    Pgate(0.5) | (q[3])
    Fourier | (q[3])


Print the solution for the circuit


```python
results = eng.run(prog)
print(results.state.reduced_gaussian([2]))
print(results.state.reduced_gaussian([3]))
```

    (array([ 3.44420453, -3.83066208]), array([[ 1.11257261, -0.5851662 ],
           [-0.5851662 ,  1.20659044]]))
    (array([0., 0.]), array([[ 1.12408144, -0.61070138],
           [-0.61070138,  1.22140276]]))

