# Programming Languages

There are different frameworks or  programming languages or tools to perform quantum algorithms, of these we will highlight four:

<ul>
    <li>Qiskit</li>
    <li>Cirq</li>
    <li>QDK</li>
    <li>Silq</li>
</ul>

# Installation Guide

For each of the frameworks or porgramming languages, the official links are mentioned so that they can be installed in different environments.

## [Qiskit](https://qiskit.org/)
Qiskit can be installed on Windows7 or higher, Ubuntu 16.04 or higher, macOS 10.12.6 or later operating systems. Its link is https://qiskit.org/documentation/install.html

## [Cirq](https://github.com/quantumlib/Cirq)

Cirq can be installed on Linux, Mac OS X and Windows operating systems, as well as on the Docker. Its link is https://cirq.readthedocs.io/en/stable/install.html


## [QDK](https://www.microsoft.com/en-us/quantum/development-kit)

QDK has fourth ways to work: develop with Q# command line applications, develop with Q# Jupyter Notebooks, develop with Q# and Python - Enables you to combine Python and Q# and develop with Q# and .NET. Their link is https://docs.microsoft.com/en-us/quantum/quickstarts/


## [Silq](https://silq.ethz.ch/)

Silq can be installed on Linux instructions, Mac instructions and Windows instructions. Its link is  https://silq.ethz.ch/install

## [Strawberry Fields](https://strawberryfields.ai/)

Strawberry Fields is a full-stack Python library for designing, optimizing, and utilizing photonic quantum computers. https://strawberryfields.readthedocs.io/en/stable/_static/install.html

# Note

If anyone needs help on installing or question about the code, we can try to help in our discord server https://discord.gg/NDm9e9W

# Hello World

To verify the installation of each of these programming languages, you can check their operation by generating the program "Hello, World!

## Qiskit
Use python to programming a qubit with respective its measurement (Considering as base the if the qiskit community).


```python
import qiskit # call  the qiskit's module 

qr = qiskit.QuantumRegister(1) # call a quantum bit (or qubit)
cr = qiskit.ClassicalRegister(1) # call a clasical bit
program = qiskit.QuantumCircuit(qr, cr) # The quantum circuit is generated from the previous qubit and bit
```

Having the circuit design, the qubit measurement is performed.


```python
program.measure(qr,cr) # The qubit is measured and stored in the classic bit.
```




    <qiskit.circuit.instructionset.InstructionSet at 0x7fa7c815cb20>



Exist different forms to display the circuit as shown below


```python
program.draw()
```




<pre style="word-wrap: normal;white-space: pre;background: #fff0;line-height: 1.1;font-family: &quot;Courier New&quot;,Courier,monospace">      ┌─┐
q0_0: ┤M├
      └╥┘
c0_0: ═╩═
         </pre>




```python
%matplotlib inline
program.draw(output="mpl")
```




![png](/assets/quantum_programs/0_hello_world/output_6_0.png)



The simulation does nothing but measure the qubit in its base state $|0>$, which is the value that is set as the standard for each qubit.

Circuit simulation is performed by selecting a backend as 'qasm_simulator


```python
job = qiskit.execute( program, qiskit.BasicAer.get_backend('qasm_simulator') )
```

When no modification is made to the qubit, its value will always be the default value which is 0.


```python
print( job.result().get_counts() )
```

    {'0': 1024}


Another way to identify the output values from a histogram that will display the total of measurements in the $|0>$ state


```python
qiskit.visualization.plot_histogram(job.result().get_counts(program))
```




![png](/assets/quantum_programs/0_hello_world/output_12_0.png)



Qiskit gives the opportunity to use quantum computers remotely, to access them you need to have an account at https://quantum-computing.ibm.com, where by checking the section "my account" you will get a token to use a eal quantum computer. In case that you save the count in your local computer is not neccesary do it again.


```python
qiskit.IBMQ.save_account('my_token') #Replace the text my_token for your own token
```

    configrc.store_credentials:WARNING:2020-08-23 00:46:18,646: Credentials already present. Set overwrite=True to overwrite.


After having the key saved, use the load method and select a computer (the list can be found at the link https://quantum-computing.ibm.com/), for this example the ibmq16_melbourne (has 15 qubits) is selected. 


```python
qiskit.IBMQ.load_account() # load the token
provider = qiskit.IBMQ.get_provider('ibm-q') # select the provider
backend = provider.get_backend('ibmq_16_melbourne') # select the name of the quatum computer to use
print("real device:",backend.name())
job = qiskit.execute( program, backend )

```

    real device: ibmq_16_melbourne



```python
print( job.result().get_counts() ) # show the result
```

    {'1': 6, '0': 1018}



```python
qiskit.visualization.plot_histogram(job.result().get_counts())
```




![png](/assets/quantum_programs/0_hello_world/output_18_0.png)



So ends the **Qiskit** Hello World! program in simulation and on a real computer.

## CIRQ

The Hello, World! from Cirq is using python to programming a qubit by applying a square root of X with its respective measurement (Considering as base the if the qiskit community).
The qubits in cirq are selected from a grid.


```python
import cirq # call  the cirq's module 
qubit = cirq.GridQubit(0, 0)# Select a qubit in the state |0>.
```

The Hello, World! circuit is generated


```python
# Create a circuit
circuit = cirq.Circuit()

circuit.append(cirq.X(qubit)**0.5)  # Apply Square root of NOT to the qubit.
circuit.append( cirq.measure(qubit, key='m'))  #Apply the measurement on the qubit.
print("Circuit:")
print(circuit) # the circuit is displayed
```

    Circuit:
    (0, 0): ───X^0.5───M('m')───


The simulation of the previous circuit is generated. The results is the output value of the measurement.


```python
simulator = cirq.Simulator() # Simulate the circuit.
repetitions= 20
result = simulator.run(circuit, repetitions=repetitions) # run the simulation fo the circuit in 20 times
print("Results:")
print(result)  # show the output values  of 'm'
```

    Results:
    m=01101011001100001011


Can be show in a histogram with the method  plot_state_histogram()


```python
counts = cirq.plot_state_histogram(result) # cal the method to generate a plot 
```


![png](/assets/quantum_programs/0_hello_world/output_26_0.png)


In case to the the probability per state is posible with the coutns divided by the repetitions value


```python
print("Probabiity =", counts/repetitions)  # cal the method to generate a plot 
```

    Probabiity = [0.5 0.5]


So ends the **Cirq** Hello World! program in simulation.

## QDK

This example is based on the programming language Q# , which has the same syntax as C#.  

As a first step you should consider that Q# has a great diversity of modules that are already based to perform gate operations like qubit measurement (like the data type *qubit*). 


```python
open Microsoft.Quantum.Intrinsic;     // for the H operation
open Microsoft.Quantum.Measurement;   // for MResetZ

operation MeasureSuperposition() : Result { // type Result return the measurement
    using (q = Qubit()) {  // using a variable of type qubit q 
        H(q);              // apply Hadamard gate on the variable q
        return MResetZ(q); // apply the measurement on q
      }
}
```

    /snippet:(1,90): warning QS6003: The namespace is already open.





<ul><li>MeasureSuperposition</li></ul>



After generating the function it is called from the command %simulate followed by the name of the function and showing the result of the simulation


```python
%simulate MeasureSuperposition
```




    Zero



So ends the **QDK** Hello World! program in simulation.


## Silq
It is a new high-level language that is based on any program following the quantum computing paradigm.Being a new programming language it is very limited so there is no kernel for jupyter. In other words, the following code must be used inside a file with the extension slq.

Silq is based on a mixture between c++ and python, where a main function must be defined and this must return the measurement of the qubits used in the program that was performed.

To represent the state $|0>$ is the value false and $|1>$ is true for this example so you can initialize the qubit in false, also, the basic gates of the quantum computation already come predefined as it is the case of Hadamard's gate (which generates the overlap between the states $|0>$ and $|1>$).


":= " is the symbol that is represented to assign a value to a variable.



```python
def main(){ // define the main function
    x:=H(false); // assign to the boolean variable x the superposition of the state false or 0
     return measure(x); // return the 
}
```

Generate a file with the previous code and save as hello_world.slq.

**The expect output**


```python
0
or 
1
```

For future programs made in silq, the link will be shared with the source code file.


# Strawberry Fields
The programs are based on photon-based quantum circuit design and the program can be simulated using the various Strawberry Fields backends.

The program is started by calling the strawberryfields modules that are in charge of generating the qubits, the circuit and the simulation.


```python
import strawberryfields as sf
from strawberryfields import ops
```

There are different gates in this library to make quantum circuits such as Sgate and BSgate:

<ul>
    <li>Sgate is $S(z)=\exp \left(\frac{1}{2}\left(z^{*} a^{2}-z a^{\dagger^{2}}\right)\right)$<li>
    <li>BSgate is $B(\theta, \phi)=\exp \left(\theta\left(e^{i \phi} a_{1} a_{2}^{\dagger}-e^{-i \phi} a_{1}^{\dagger} a_{2}\right)\right)$</li>
</ul>

For more information about the gates it uses you can find the following link https://strawberryfields.readthedocs.io/en/stable/introduction/ops.html


```python
# create a quantum program with 3 qubits
prog = sf.Program(3)

# describe the circuit 
with prog.context as q:
    ops.Sgate(0.54) | q[0] # call the Sgate 
    ops.Sgate(0.54) | q[1]
    ops.Sgate(0.54) | q[2]
    ops.BSgate(0.43, 0.1) | (q[0], q[2]) # call the BSGate
    ops.BSgate(0.43, 0.1) | (q[1], q[2])
    ops.MeasureFock() | q # perform the measurement on all qubits of the variable q 
```

It is possible to print the set of instructions that were made to build the circuit as the measurements that will be made at the end of it.


```python
prog.print()
```

    Sgate(0.54, 0) | (q[0])
    Sgate(0.54, 0) | (q[1])
    Sgate(0.54, 0) | (q[2])
    BSgate(0.43, 0.1) | (q[0], q[2])
    BSgate(0.43, 0.1) | (q[1], q[2])
    MeasureFock | (q[0], q[1], q[2])


The Engine method works with the name of the backend and the possible options for that backend. 

You can work with three backends.

<ul>
    <li>The 'fock' written in NumPy.</li>
    <li>The 'gaussian' written in NumPy.</li>
    <li>The 'tf' written in TensorFlow 2 (for this one require install tensorflow 2).</li>
</ul>

After indicating the backend, the run method is implemented on the variable that the circuit is


```python
eng = sf.Engine("fock", backend_options={"cutoff_dim": 5})
result = eng.run(prog)
```

It is possible to print the description of the output status


```python
print(result.state)
```

    <FockState: num_modes=3, cutoff=5, pure=True, hbar=2>


Is also possible identify trace of the quantum state


```python
state = result.state
state.trace()
```




    1.0



It has the property of identifying the density matrix of the output state.


```python
state.dm().shape # density matrix
```




    (5, 5, 5, 5, 5, 5)



Finally, is possible to measurement samples from any measurements performed.


```python
result.samples
```




    array([[0, 0, 0]])



With this fnish the Hello, World! of  strawberries fields.
