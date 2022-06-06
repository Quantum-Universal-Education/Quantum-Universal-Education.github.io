---
title: "Qubits vs Bits"
categories:
  - Blog
tags:
  - programming project
  - numpy
  - jupyter notebook
  - quantum bit
author: Maria Gragera Garces
---


<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

# 
This tutorial will explain the fundamental differences between quantum and classical data storage units, and how they affect computer performance. This notebook has been designed for non-technical readers, who want to understand how qubits differ from bits and how do these differences make quantum computers different from classical computers.

### Binary bits
How do computers store data? What allows us to communicate with modern machines?
Regardless of academic background, anyone who has seen the Matrix films will intuitively think of a series of 0's & 1's. Something like this comes to mind (run the code below to see a randomly generated binary string):


```python
import random

def binary_numbers(size):
   
    n = ""
    for i in range(size):
        choice = str(random.randint(0, 1))
        n += choice
    return(n)
 
binary_string = binary_numbers(100)
print(binary_string)
```

    0100101110000001110001000111010010111010100111000100000100010111010010011101001001110010101100100001


In essence, modern computers are massive calculators that know how to store an interpret ridiculous amounts of data. Each file, video, document and image in our laptops, phones, smartwatches, etc. can be and is represented by a (very long) series of numbers. Therefore, computational power boils down to having an efficient and fast system of storing and processing this data. Our current devices use the bit system.

X bits are capable of representing a number between 0 and 2^x. That might not seem like a lot at first, but the above creates a series of 100 bits, and therefore can represent any number between 0 & 1267650600228229401496703205376​... For reference as of the 3/6/22 Elon Musk's net worth is estimated at 2181000000 (218.1 billion) US $. Quite impressive for a sequence of 1's and 0's.

The word "bit" stands for binary digit. The binary number system is the most basic unit of information, and allows us to store any number as a combination of 0's and 1's. 
The way value is associated with each 1 or 0 is based on their position in the string. For example, in binary, 10 represents the number 2 but 100 represent number 4. From right to left each bit multiplies 2^n, with n being it's position. The idea looks something like this:

                                 64   |  32   |  16   |   8   |   4   |   2   |   1  
                                 ____________________________________________________   
                                  1   |   0   |   0   |   0   |   0   |   1   |   1     = 67
                                 ____________________________________________________   
                                  0   |   0   |   1   |   0   |   1   |   0   |   0     = 20
                                 ____________________________________________________   
                                  0   |   0   |   0   |   0   |   0   |   0   |   0     = 0

The following piece of code is a fun way for you to become more familiar with the idea of binary. It will output the binary equivalent of any number you feed it (the default is set to 100). Have fun testing it!


```python
f'{6:100b}'
```




    '                                                                                                 110'



### Qubits & the Bloch sphere

Now that we have built and intuition on the mathematical representation of data in modern computers, let's look at why Quantum computers will run on a different system.

Unlike modern classical computers, quantum computers base their storage on quantum particle superposition. Quantum theory argues that particles have states that dictate their behaviour. These states are very similar to our binary system, they are often also represented by 0's & 1's. But unlike bits, they represent a much more complex data storage system. 

Scientists often like to represent qubits through  Bloch's sphere. Run the code below to see how a Bloch sphere looks like:


```python
import numpy as np
from pylab import *
from qutip import *

b = Bloch()
b.show()
```


    
![png](/assets/images/Maria_QvsB/output_10_0.png)
    



    
![png](/assets/images/Maria_QvsB/output_10_1.png)
    


The idea behind this representation is that a Qubit has a state 0 or |0> if it's amplitude* lies at the top of the sphere, & a state |1> if it lies at the bottom.

### Amplitudes and vectors

With these ideas in place, let's start decoding some of the very intimidating math behind qubits.
A qubit is often represented by the following formula:

                                                     |ψ⟩=a|0⟩+b|1⟩


This mathematical representation allows us to position our qubit |ψ⟩ in the Bloch sphere. The variables a & b give us the qubit's coordinates with respect to it's allowed states |0> & |1>.
Run the code below, to get a better idea of what type of information a & b provide:


```python
b = qutip.Bloch()
pnt = [1./np.sqrt(3), 1./np.sqrt(3), 1./np.sqrt(3)]
b.add_points(pnt)
vec = [0, 1, 0]
b.add_vectors(vec)
up = qutip.basis(2, 0)
b.add_states(up)
b.render()
```


    
![png](/assets/images/Maria_QvsB/output_16_0.png)
    


In this case variables a & b allow us to find the coordinates of our blue qubit along the x & y axis.

### How is this different to the binary system?

In the previous example, we can see that our qubit (represented by a blue dot) is closer to the Bloch sphere's |0> pole than to it's |1> pole. Wouldn't that imply that it represents the equivalents of a 0 bit, and that the Bloch sphere is just a confusing 3D way of explaining how particles make a choice between being in a state |0> & |1>?

Fortunately, no, if that was the case Quantum computers wouldn't be very interesting. 

A qubit does not represent a "state", but rather a superposition of states. Our example is partly in state |0> and partly in state |1>, it holds both states simultaneously even if it might be closer to one.

That is a difficult concept to grasp, but the following comparison to bits might make it simpler:
With two bits we can create 2^2 = 4 number combinations: 11,10,01, & 00 . Given that qubits hold two states at once, two qubits can hold all those combinations at once. 

     X qubits can represent All values between 0 & 2^x at a time, Y bits can represent ONE value between 0 & 2^y at a time

The computational power between a quantum computer and a classical computer is astronomical. For scale, this table shows the number of qubits needed to hold a certain amount of RAM against the number of bits. 


                    Number of qubits	Number of bits / Number of loops	    RAM	            Time'*'

                         13	                      8192	                   1 kB		      2.73x10-6 s
                         20	                      1048576	                128 kB		    3.5x10-4s
                         23	                      8388608	                1 MB		      2.8x10-3s
                         33	                      8589934592	             1 GB		      2.9 s
                         43	                      8.8x1012	               1 TB		      49 mins
                         53	                      9.0x1015	               1 PB		      35 hours
                         63	                      9.2x1018	               1 EB		      97.5 years
                         1000		               1.1x10301	               1.3x10282 EB  	1.1x10284 years

'*' The time that it takes to run these operations is estimated through the following assumptions: We have a Classical Computer with a clock speed of 3 GHz. This is an average base clock speed for most professional work laptops 3.0 GHz. Let’s also assume one operation in a classical state can be done in one clock cycle.  The computer could therefore perform 3 billion operations per second.

Qubits can undoubtedly revolutionize humanities computing power. If we are able to fully develop efficient and functional quantum computers we will be able to run simulations and models that we can now only dream of. Qubits can (and hopefully will) revolutionize weather predictions, cryptography and online security, artificial intelligence, our mathematical models, stock prediction, etc. 

### Let's build a qubit

Great! We might be at the door of an unstoppable technology that will revolutionize many industries. What can we do now? 
Unfortunately most of us do not have direct access to qubits, and probably won't do so for the next couple of years. So for now, we have to prepare ourselves with simulations.

Many quantum simulators are currently available to the public (I will append a list at the end of this notebook). One of my personal favourites is SeQUeNCe, which we will be using to build our qubit.
SeQUeNCe is an open source, discrete-event simulator for quantum networks. In order for the code below to run, you will need to install the SeQUeNCe package.
You can download the source code from github:

                                             https://github.com/sequence-toolbox/SeQUeNCe

Then navigate to its directory, and install with:


```python
$ pip install .
```


      File "<ipython-input-5-9101172ce427>", line 1
        $ pip install .
        ^
    SyntaxError: invalid syntax



Hopefully, now that the toolbox is installed, we can start importing the libraries we need.


```python
import sequence 

import math
import numpy
from matplotlib import pyplot as plt

from sequence.utils.encoding import *
from sequence.utils.encoding import polarization
from sequence.utils.quantum_state import QuantumState
```

Qubits are mathematical interpretations that can be used to explain and build quantum circuits over different types of quantum computers. They can take different shapes and physical formats. Depending on the technology a qubit may be a photon, a trapped ion, a superconductor, a semiconductor quantum dot, etc. If you want to become more familiar with different types of qubits, I would recommend starting with this QuTech video: https://youtu.be/oZacBmOwvz0

Sequence is a photonic based simulator, which means that it considers photons as it's qubit "format". In order to build a qubit, we will import it's photon class.


```python
class Photon():
        def __init__(self, name, wavelength=0, location=None, encoding_type=polarization,
                quantum_state=(complex(1), complex(0))):

                self.name = name
                self.wavelength = wavelength
                self.location = location
                self.encoding_type = encoding_type
                if self.encoding_type["name"] == "single_atom":
                    self.memory = None
                self.quantum_state = QuantumState()
                self.quantum_state.state = quantum_state
                self.qstate_key = None
                self.is_null = False

          def entangle(self, photon):

                self.quantum_state.entangle(photon.quantum_state)

          def random_noise(self):

                self.quantum_state.random_noise()

          def set_state(self, state):
                self.quantum_state.set_state(state)

          @staticmethod
          def measure(basis, photon):

                return photon.quantum_state.measure(basis)

```

That's a lot of code at once! So let's analyze it bit by bit!


```python
        def __init__(self, name, wavelength=0, location=None, encoding_type=polarization,
                quantum_state=(complex(1), complex(0))):

                #photon values
                self.name = name
                self.wavelength = wavelength
                self.location = location
                self.encoding_type = encoding_type
                if self.encoding_type["name"] == "single_atom":
                    self.memory = None
                self.quantum_state = QuantumState()
                self.quantum_state.state = quantum_state
                
                #administrative lines
                self.qstate_key = None
                self.is_null = False
```

Our first function _init_ gives our photon its values: a name, a wavelength, a location, an encoding type, & a quantum state.
What do these values mean?
* Name: The photon's name serves as a way of identifying it in bigger simulations, it won't be of much use to us now, but can be quite useful later on.
* Wavelength: A photon is the fundamental particle of light. Light behaves as a particle and a wave. This effect causes photons to behave as such, and thus to have a wavelength.
* Location: As I previously mentioned sequence is a Quantum network simulator. Therefore, its purpose is to simulate how qubits behave in a quantum network. For this to be possible, we need to know where qubits 'land' at the end of an experiment. Thus why photons need to have a defined location with respect to the simulated network.
* Encoding type: We have set this value to single_atom. The simulator allows us to consider qubits as interpretations of one or various photons. For simplification, we have chosen to use one photon as a qubit.
* Quantum state: This variable will hold our quantum state data.

The bottom two lines are less relevant to our objective. They simply ensure our code doesn't "break" whilst defining the variables of a photon, and allow for more advanced adjustments.


```python
          def entangle(self, photon):

                self.quantum_state.entangle(photon.quantum_state)
```

Our first function, points towards a very interesting qubit effect. As we already know, qubits are far more complex than bits. They are based on quantum particle theory, and therefore behave according to quantum physics. This means, that they are affected by quantum effects. One of which is entanglement. 
If we entangle two qubits, regardless of how far apart they might be, measure the state of one of them allows us to know the state of the other without needing to measure it. This effect is extremely valuable and useful to quantum computation, as it allows us to create connections between fundamental particles of information. I will point at further reading material at the end of this notebook.


```python
          def random_noise(self):

                self.quantum_state.random_noise()
```

Our second function creates a randomly assigned noise. Quantum noise is currently one of the biggest hurdles the industry, most overcome in order to create efficient quantum machines. Quantum noise is a direct consequence of the quantum nature of qubits. Scientist don't yet fully understand its origin, thus why it is often assigned randomly in simulations, but various quantum error correction codes exist and are being developed to combat it. These error correction codes, make use of quantum entanglement, as a tool to "check" if qubits hold their predicted state. 
Given that we are only building a qubit, this effect won't cause any issues.


```python
          def set_state(self, state):
                self.quantum_state.set_state(state)
```

Our penultimate function, allows us to set the qubits state by using default values within the simulator. These values allow us to "find" our qubit's position in the Bloch sphere. This state is what the final code will output, and it will resemble a set of coordinates.


```python
          @staticmethod
          def measure(basis, photon):

                return photon.quantum_state.measure(basis)
```

Our final function measures and returns the qubit's state.

Now, let's take another look at our code:


```python
import sequence 

import math
import numpy
from matplotlib import pyplot as plt

from sequence.utils.encoding import *
from sequence.utils.encoding import polarization
from sequence.utils.quantum_state import QuantumState
        
class Photon():
    def __init__(self, name, wavelength=0, location=None, encoding_type=polarization,
        quantum_state=(complex(1), complex(0))):

        self.name = name
        self.wavelength = wavelength
        self.location = location
        self.encoding_type = encoding_type
        if self.encoding_type["name"] == "single_atom":
            self.memory = None
        self.quantum_state = QuantumState()
        self.quantum_state.state = quantum_state
        self.qstate_key = None
        self.is_null = False

    def entangle(self, photon):

        self.quantum_state.entangle(photon.quantum_state)

    def random_noise(self):

        self.quantum_state.random_noise()

    def set_state(self, state):
        self.quantum_state.set_state(state)

```

We have now built a basic photon structure that we can now use for scalable simulations! 🎉🎉
As a fundamental unit of information, our qubit is not very interesting by itself (as you might see when you run the code above, there are no returns). But it is the building block of Quantum computation, and a such a crucial part of all simulations.

## Thank you & congratulations for coming this far!

### Here are some further resources on mentioned topics and used tools:

#### Further reading material on bits: 
    - Microsoft quantum resources: https://azure.microsoft.com/en-gb/overview/what-is-a-qubit/#superposition-interference-entanglement 
    - How to build a qubit (video) : https://youtu.be/oZacBmOwvz0
#### Qutip, the tool used to plot our Bloch sphere:
    - https://qutip.org/docs/latest/guide/guide-bloch.html
#### Source for our qubit/bit performance table comparison:
    - https://vincentlauzon.com/2018/03/21/quantum-computing-how-does-it-scale/#:~:text=Classical%20Bits%20vs%20qubits,on%20both%20values%20at%20once.
#### SeQUenCe: 
    - https://github.com/sequence-toolbox/SeQUeNCe
#### Quantum entanglement:
    - https://scienceexchange.caltech.edu/topics/quantum-science-explained/entanglement  
#### Quantum noise:
    - https://en.wikipedia.org/wiki/Quantum_noise#:~:text=Quantum%20noise%20is%20observed%20in,and%20Zero%2Dpoint%20energy%20fluctuations.

## My journey in Quantum

Hi 👋 ! Thank you for completing my short tutorial on Qubits. I'm Maria, a university undergraduate working in the Quantum Networking field. 
As part of my degree I joined Cisco, where I have been contributing to their internal R&D Quantum incubation team for the past year. My work focuses on quantum networking protocol design and simulations, and I am now actively trying to use my newly learned skills to contribute in the Quantum open source software community! In an effort to do this I am creating simple tutorials such as this one that help non-technical individuals start their quantum journey.
If you want to see what I'm up to, feel free to follow my career on Linkedin: https://www.linkedin.com/in/maria-gragera-garces/
