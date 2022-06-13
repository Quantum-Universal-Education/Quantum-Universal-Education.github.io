---
title: "Variational Quantum Eigensolver: Simulating the Electronic Structure of Molecules"
categories:
  - Blog
tags:
  - tutorial
  - TFQ
  - VQE
  - jupyter notebook
  - quantum computing
  - quantum chemistry
  - H2
author: 
  - Owen Lockwood
  - Curate Section
  - Lia Yeh Q
  - Alberto Maldonado Romo Q
---

<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

In this tutorial we will outline the theoretical background of the VQE and how it can be applied on a quantum computer, then show an implementation in TensorFlow-Quantum for the $$H_2$$ molecule. 

## Problem Definition

The problem we wish to solve is to find the energies associated with a given Hamiltonain $\hat{H}$. We begin with the Time Independent Schrodinger Equation (TISE):

$$
    \hat{H} |\Psi \rangle = E |\Psi \rangle
$$

This is fundamentally an eigenvalue problem, in which the energies are the eigenvalues of the hamiltonian. Focusing on the ground state energy (i.e. the minimum eigenvalue), yields 

$$
    E_0 \leq \langle \Psi | \hat{H} | \Psi \rangle
$$

Where the RHS represented the expectation value of the hamiltonian. We can therefore approximate $$E_0$$ by minimizing this RHS using a parameterized wavefunction (or in the case of quantum computers, a parameterized quantum circuit). I.e. by solving the optimization problem [1]:

$$
    \min_\theta \langle \Psi(\theta) | \hat{H} | \Psi(\theta) \rangle
$$

And that is the variational quantum eigensolver!

## Molecular Hamiltonian Derivation

Of course, now the real challenge begins. How do we map our molecular hamiltonains problem onto this setup? First, let us revisit the TISE and rewrite it in an expanded form. 

$$
    \frac{-\hbar^2}{2m} \nabla^2 \Psi (r)  + V(r) \Psi (r)  = E \Psi (r)
$$

where $\nabla^2$ is the Laplacian (divergence of the gradient). Note that $r$ can be in Cartesian or polar or any coordinate system. This separates the hamiltonian into kinetic (Laplacian) and potential (V) energies. 

Now let us expand this equation to be more specific for molecules. Zooming in on the kinetic energy, we have two sources of movement: the electrons and the movement of the nucleus. Thus we have:

$$
    K.E. = -\sum_i^{nuclei} \frac{\hbar^2}{2 m_i} \nabla^2_i - \sum_i^{electrons} \frac{\hbar^2}{2m_e} \nabla^2_i
$$

where $m$ corresponds to the mass. 

Now let us consider the potential energy. There are three sources of coulombic interactions, the nucleus electron attraction, the nucleus nucleus repulsion and the electron electron repulsion. We write this as:

$$
    P.E. = -\sum_i^{nuclei} \sum_j^{electrons} \frac{Z_i e^2}{4 \pi \epsilon_0 |r_i - r_j|} + \sum_i^{nuclei} \sum_{j \neq i}^{nuclei} \frac{Z_i Z_j e^2}{4 \pi \epsilon_0 |r_i - r_j|} + \sum_i^{electrons} \sum_{j \neq i}^{electrons} \frac{e^2}{4 \pi \epsilon_0 |r_i - r_j|}
$$

Where $Z_i$ is the atomic number.

Combining these yields the full molecular hamiltonain:

$$
    \hat{H} = -\sum_i^{nuclei} \frac{\hbar^2}{2 m_i} \nabla^2_n - \sum_i^{electrons} \frac{\hbar^2}{2m_e} \nabla^2_i -\sum_i^{nuclei} \sum_j^{electrons} \frac{Z_i e^2}{4 \pi \epsilon_0 |r_i - r_j|} + \sum_i^{nuclei} \sum_{j \neq i}^{nuclei} \frac{Z_i Z_j e^2}{4 \pi \epsilon_0 |r_i - r_j|} + \sum_i^{electrons} \sum_{j \neq i}^{electrons} \frac{e^2}{4 \pi \epsilon_0 |r_i - r_j|}
$$

Now we can reduce the scope of our problems with some assumptions. First, we assume that the nuclei are not moving. This is based on the fact that electrons move many thousands of times faster. This approximation is known as the Born-Oppenheimer Approximation. This enables us to remove two terms from our hamiltonian that become constant (constants in the hamiltonian apply a constant effect to the eigenvalues). The resulting hamiltonian is known as the electronic hamiltonian (we simplify some terms using atomic units): 


$$
\label{reduced_hamil}
    %\hat{H}_{BO} = - \sum_i^{electrons} \frac{\hbar^2}{2m_e} \nabla^2_i -\sum_i^{nuclei} \sum_j^{electrons} \frac{Z_i e^2}{4 \pi \epsilon_0 |r_i - r_j|}  + \sum_i^{electrons} \sum_{j \neq i}^{electrons} \frac{e^2}{4 \pi \epsilon_0 |r_i - r_j|}
    \hat{H}_{BO} = - \sum_i^{electrons} \frac{1}{2} \nabla^2_i -\sum_i^{nuclei} \sum_j^{electrons} \frac{Z_i}{|r_i - r_j|}  + \sum_i^{electrons} \sum_{j \neq i}^{electrons} \frac{1}{|r_i - r_j|}
$$

Now that we have reduced the problem to just include electronic components (hence why it is called the electronic structure problem), we need to get the into something operable on quantum computers. 

## Moving to an Amenable Formalism

To do this conversion, we move from the "first quantization" to the "second quantization". These are just different formalisms that convey the same information. In this SQ formalize, we move from Slater Determinants to occupation number representations where $\Psi = |n_1, n_2, n_3, ... \rangle$ and $n_i$ corresponds to the number of particles in state $i$ (note the exponential growth that comes with expanding this state representation). We can operate on this wavefunction using creation and annihilation operators $\hat{a}_i^\dagger, \hat{a}_i$. The challenge is to now map the original molecular hamiltonian into this formalism. 

Single particle operators can be mapped via 

$$
\sum_i \hat{h} (x_i) \rightarrow \sum_{p, q} \langle p | \hat{h} | q \rangle \hat{a}^\dagger_p \hat{a}_q
$$

So we can map our electronic kinetic energy and nuclear-electron potential (since the nuclei are frozen) via the following. Also note that in the following equations x is not a one dimensional Cartesian coordinate, but contains the 3 dimensional information (as used above). The mapping is called the core integral. 

$$
    - \sum_i^{electrons} \left ( \frac{1}{2} \nabla^2_i  + \sum_i^{nuclei}  \frac{Z_i}{|r_i - r_j|} \right )  \rightarrow \int^{\infty}_{-\infty}  \psi^*_p (x) \left ( -\frac{1}{2} \nabla^2 - \sum_i^{nuclei} \frac{Z_i}{|r_i - r_{x}|} \right )  \psi_q (x) dx = h_{pq} = \langle p | \hat{h} | q \rangle
$$


Multiparticle operators can be mapped via:

$$
    \frac{1}{2} \sum_i \sum_j \hat{h}(x_i, x_j) \rightarrow \frac{1}{2}\sum_{p, q, r, s} \langle pq | \hat{h} | rs \rangle \hat{a}^\dagger_p \hat{a}^\dagger_q \hat{a}_r \hat{a}_s
$$

So we can map our two particle term (the electron electron repulsion term) using the electron repulsion integral:

$$
    \sum_i^{electrons} \sum_{j \neq i}^{electrons} \frac{1}{|r_i - r_j|} \rightarrow \int^{\infty}_{-\infty}  \int^{\infty}_{-\infty}  \psi^*_p(x_i) \psi^*_q(x_i) \frac{1}{|r_i - r_j|} \psi_r(x_j) \psi_s(x_j) dx_i dx_j  = g_{pqrs} = \langle pq | \hat{h} | rs \rangle
$$

Combining these with the fermionic operators yields (where p, q, r, s can take on any of the N spin orbitals):

$$
    \hat{H}_{SQ} = h_{pq} \hat{a}^\dagger_p \hat{a}_q + \frac{1}{2}g_{pqrs} \hat{a}^\dagger_p \hat{a}^\dagger_q \hat{a}_r \hat{a}_s + C
$$

We have the C constant to account for the assumptions earlier (since even if the nuclei are static, the nucleus-nucleus repulsion term is still some constant). Note that these integrals can be solved and provide the constants for our hamiltonian terms in VQE. 


## Mapping to a Quantum Computer

Now we just have two final challenges. How do we map the the orbitals to our occupation numbers and how do we map the fermionic operators to the quantum computer operations? Let's address the first challenge now. There are many different choices of mapping we could use. To represent this problem, we use a linear combination of atomic orbitals (LCAO). A common choice for VQE is STO-3G (approximating the Slater type orbital with 3 gaussians). To represent STO-3G we separate the wavefunction into its radial and angular parts $\Psi = R(r)Y(\theta, \phi)$ where 


$$
\begin{split}
    \text{Slater Type Orbital}: R(r) = N r^l e^{-\zeta r} \\
    \text{Gaussian Type Orbital}: R(r) = N r^l e^{-\zeta r^2} \\
    \text{STO-3G}: R(r) = N \sum_i^3 c_i r^l e^{-\zeta_i r^2} 
\end{split}
$$

Where $r^l$ is the angular momentum, $\zeta$ controls charge/size of nucleus and $N, c_i$ are constants. These are minimal basis sets (i.e. one function per orbital) and uncommon in classical computational quantum chemistry, more accurate ones such as 6-31G* or cc-pVDZ are preferred. 


To tackle the second challenge, once again, there are several solutions such as Parity Mapping, Jordan-Wigner, Bravy-Kitaev, etc. All of these map fermionic operators onto pauli gates. These mappings are necessary since we the basic Pauli gates do not satisfy the commutation relations that fermionic operators must. For example, Jordan-Wigner maps 

$$
    \hat{a}_p \rightarrow \frac{1}{2}(X_p + i Y_p)Z_1 ... Z_{p-1}
$$

And now we have all the tools for VQE. We can map our hamiltonian onto our quantum operations using the fermionic operators and the conversions and we can map our orbital space to our quantum register using a basis function and the occupation formalism. Thankfully everthing that has been covered so far has been implemented in easy to use python packages. 

## Implementation

Now, let's get to the code. In this tutorial we will be using TensorFlow-Quantum (TFQ) [2] for our quantum optimization need and OpenFermion [3] to generate our electronic structure problems. First, get all the imports squared away. 


```python
import tensorflow as tf
import tensorflow_quantum as tfq
import cirq
import sympy
import openfermion as of
from openfermionpyscf import generate_molecular_hamiltonian
from scipy.sparse import linalg
import numpy as np
import matplotlib.pyplot as plt
```


```python
print("TF Version:", tf.__version__)
print("TFQ Version:", tfq.__version__)
print("OF Version:", of.__version__)
```

    TF Version: 2.7.0
    TFQ Version: 0.6.1
    OF Version: 1.3.0


Now we need to choose our circuit structure to represent the parameterized wavefunction. Although there are a number of choices, we will be going with a HEA [4] inspired ansatz. In this, multiple layers of single qubit rotations are paired with circularly entangling CNOT gates. 


```python
def layer(circuit, qubits, parameters):
    # Single qubit rotations
    for i in range(len(qubits)):
        circuit += cirq.ry(parameters[3 * i]).on(qubits[i])
        circuit += cirq.rz(parameters[3 * i + 1]).on(qubits[i])
        circuit += cirq.ry(parameters[3 * i + 2]).on(qubits[i])
    # Entangling
    for i in range(len(qubits)-1):
        circuit += cirq.CNOT(qubits[i], qubits[i + 1])
    circuit += cirq.CNOT(qubits[-1], qubits[0])
    return circuit

def ansatz(circuit, qubits, layers, parameters):
    for i in range(layers):
        params = parameters[3 * i * len(qubits):3 * (i + 1) * len(qubits)]
        circuit = layer(circuit, qubits, params)
    return circuit
```

Next, we must create the actual TF model that we will be optimizing. We will create a noiseless version and a noisy version (with shot and depolarizing noise). We will be using a gradient based optimizer so we need to be able to differentiate these ciruits. In the noiseless case we can use adjoint differentiation, an efficient method for simulations. In the noisy case we will use the more realistic parameter shift rule which tells us that the derivative of the quantum circuit is $$ \frac{\partial f(x)}{x} = \frac{f(x + s) - f(x - s)}{2 \sin (s) } $$


```python
def make_vqe(qubits, layers, hamiltonian):
    num_params = layers * 3 * len(qubits)
    params = sympy.symbols('vqe0:%d'%num_params) # The variational parameters
    c = ansatz(cirq.Circuit(), qubits, layers, params) # Create the circuit
    ins = tf.keras.layers.Input(shape=(), dtype=tf.dtypes.string) # Quantum circuits are serialized as strings in TFQ
    pqc = tfq.layers.PQC(c, hamiltonian, differentiator=tfq.differentiators.Adjoint())(ins)
    vqe = tf.keras.models.Model(inputs=ins, outputs=pqc)
    return vqe

def make_vqe_noisy(qubits, layers, hamiltonian):
    num_params = layers * 3 * len(qubits)
    params = sympy.symbols('vqe0:%d'%num_params) # The variational parameters
    c = ansatz(cirq.Circuit(), qubits, layers, params) #  Create the circuit
    c = c.with_noise(cirq.depolarize(p=0.01)) # Add noise 
    ins = tf.keras.layers.Input(shape=(), dtype=tf.dtypes.string) # Quantum circuits are serialized as strings in TFQ
    pqc = tfq.layers.NoisyPQC(c, hamiltonian, repetitions=1000, sample_based=True, differentiator=tfq.differentiators.ParameterShift())(ins)
    vqe = tf.keras.models.Model(inputs=ins, outputs=pqc)
    return vqe
```

Now we just need a function to minimize the expectation value of this circuit. We can do that using traditional TensorFlow techniques using the Adam optimizer (which has been shown to be empirically efficient) [5]. 


```python
def optimize_vqe_gradient(vqe, init):
    old = np.inf
    inputs = tfq.convert_to_tensor([cirq.Circuit()]) # Empty circuit input
    counter = 0 
    vqe.set_weights([init])
    opt = tf.keras.optimizers.Adam(learning_rate=0.1) # Optimizer
    energy = 0
    while counter < 200: # 200 iterations
        with tf.GradientTape() as tape:
            guess = vqe(inputs)
        # Get and apply the gradients
        grads = tape.gradient(guess, vqe.trainable_variables) 
        opt.apply_gradients(zip(grads, vqe.trainable_variables))
        guess = guess.numpy()[0][0]
        energy = guess
        # If it has reached the minimum, stop optimization
        if abs(guess - old) < 1e-5:
            break
        old = guess
        counter += 1

    return energy
```

Now specify some of the important problem parameters. 


```python
layers = 2 # Number of VQE layers
diatomic_bond_length = 0.2 # H_2 bond length
interval = 0.1 # Increment to evaluate bond lengths at
max_bond_length = 4.0 
basis = 'sto-3g'
multiplicity = 1
charge = 0
ground_energies_real = []
ground_energies_vqe = []
ground_energies_vqe_noisy = []
bond_lengths = []
```

Finally we can use OpenFermion to create our problems for each bond length. These functions solves the integrals from before and computes the necessary transforms to render the problem useable for a quantum computer. 


```python
while diatomic_bond_length <= max_bond_length: # Iterate through the bond 
    geometry = [('H', (0., 0., 0.)), ('H', (0., 0., diatomic_bond_length))] # Specify the geometry of the molecule
    # Solve the integrals above to generate the molecular hamiltonians
    molecular_hamiltonian = generate_molecular_hamiltonian(geometry, basis, multiplicity, charge) 
    n_qubits = of.count_qubits(molecular_hamiltonian) 
    qs = [cirq.GridQubit(0, i) for i in range(n_qubits)] # Create the qubits for the circuit
    jw_operator = of.transforms.jordan_wigner(molecular_hamiltonian) # Convert the fermionic operators to pauli operators
    hamiltonian_jw_sparse = of.get_sparse_operator(jw_operator)
    eigs, _ = linalg.eigsh(hamiltonian_jw_sparse, k=1, which='SA') # Compute the exact ground state
    hamiltonian = of.transforms.qubit_operator_to_pauli_sum(jw_operator, qubits=qs) # Convert to cirq object

    # Create VQE models
    vqe = make_vqe(qs, layers, hamiltonian) 
    vqe_noisy = make_vqe_noisy(qs, layers, hamiltonian)
    initial_value = tf.random.uniform(shape=[layers * 3 * n_qubits], minval=0, maxval=2 * np.pi)
    # Optimize both models using same random initialization
    ground_gradient = optimize_vqe_gradient(vqe, initial_value)
    ground_gradient_noisy = optimize_vqe_gradient(vqe_noisy, initial_value)
    # Save the results
    ground_energies_vqe.append(ground_gradient)
    ground_energies_vqe_noisy.append(ground_gradient_noisy)
    ground_energies_real.append(eigs[0])
    bond_lengths.append(diatomic_bond_length)

    diatomic_bond_length += interval
    if diatomic_bond_length > 1.5:
        diatomic_bond_length += interval
```

Finally, we can plot the results of the VQE calculations. We can see that for a small molecule such as $H_2$ our HEA circuit is capable of finding the ground state energy quite well. However, we can see that with the addition of shot and depolarizing noise, the performance decreases. 


```python
plt.scatter(bond_lengths, ground_energies_vqe, label='VQE Predicted Ground State', marker='o', facecolors="None", edgecolor='blue')
plt.scatter(bond_lengths, ground_energies_vqe_noisy, label='Noisy VQE Predicted Ground State', marker='s', facecolors="None", edgecolor='red')
plt.plot(bond_lengths, ground_energies_real, label='Ground State', color='blue')
plt.xlabel("Interatomic Distance (Angstroms)")
plt.ylabel("Energy (Hartree)")
plt.legend()
plt.show()
```


    
![png](/assets/images/vqe/output_18_0.png)

    


## References

[1] Peruzzo, A., McClean, J., Shadbolt, P., Yung, M. H., Zhou, X. Q., Love, P. J., ... & O’brien, J. L. (2014). A variational eigenvalue solver on a photonic quantum processor. Nature communications, 5(1), 1-7.

[2] Broughton, M., Verdon, G., McCourt, T., Martinez, A. J., Yoo, J. H., Isakov, S. V., ... & Mohseni, M. (2020). Tensorflow quantum: A software framework for quantum machine learning. arXiv preprint arXiv:2003.02989.

[3] McClean, J. R., Rubin, N. C., Sung, K. J., Kivlichan, I. D., Bonet-Monroig, X., Cao, Y., ... & Babbush, R. (2020). OpenFermion: the electronic structure package for quantum computers. Quantum Science and Technology, 5(3), 034014.

[4] Kandala, A., Mezzacapo, A., Temme, K., Takita, M., Brink, M., Chow, J. M., & Gambetta, J. M. (2017). Hardware-efficient variational quantum eigensolver for small molecules and quantum magnets. Nature, 549(7671), 242-246.

[5] Lockwood, O. (2022). An Empirical Review of Optimization Techniques for Quantum Variational Circuits. arXiv preprint arXiv:2202.01389.
