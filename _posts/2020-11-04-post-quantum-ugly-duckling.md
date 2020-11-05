---
title: "Quantum Random Number Generation at Qiskit Hackathon Global"
categories:
  - Blog
tags:
  - NQRNG
  - QRNG
  - NISQ
  - noise
  - random
  - Qiskit
  - Qasm
  - hackathon
  - Qiskit Hackathon Global
  - RNG
  - FFT
  - Fourier Transform
  - Discord bot
  - Qadjoke bot
  - Dad jokes
  - simulator
  - hardware
  - Qiskit Pulse
  - Rabi experiment
  - IBM Cloud
author:
  - Rochisha Agarwal
  - Dayeong Kang
  - Hyorin Kim 
  - Kathrin Koenig
  - Rana Prathap
  - Curate Section
  - Harshit Garg Q
  - Lia Yeh Q
---

|Have a look at these prerequisites to better understand the article:
|  - (Fast) Fourier Transform [https://en.wikipedia.org/wiki/Fast_Fourier_transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform)
|  - Qasm Simulator [https://www.youtube.com/watch?v=V4CwN4rEtVQ](https://www.youtube.com/watch?v=V4CwN4rEtVQ)
 

We are living in the [Noisy Intermediate Scale Quantum](https://arxiv.org/abs/1801.00862) (NISQ) computing era. Noise says, "I am inevitable," but we want to give noise the finger snap (like Thanos in Marvel's Avenger's). There have been several attempts to make the existing noise useful, but in this project, we want to maximize the current noise and explore use cases for this high noise.

Random numbers are an important commodity in multiple fields and businesses. The random numbers we are able to create on deterministic devices such as our computer are not truly random and are called [pseudo-random numbers](https://en.wikipedia.org/wiki/Pseudorandom_number_generator). For most purposes these pseudo random numbers should be sufficient, however, for applications involving security, true random numbers are imperative. But, creating such truly random numbers is not trivial. For example, the security company Cloudflare (which runs a network for increasing internet security and performance which over 25 million internet properties are on) uses a [video of a wall of lava lamps as a source of randomness](https://blog.cloudflare.com/randomness-101-lavarand-in-production/) in the creation of random numbers. Today, let's see how we can extract randomness inherent in a Quantum Computer to create random numbers. 

This project was part of the [Qiskit Hackathon Global](https://qiskithackathon.global.bemyapp.com/#/projects), from October 5th-9th 2020. The hackathon was a private event. The idea for our project came from [Soyoung Shin](https://www.linkedin.com/in/karysshin/), who also mentored our group.

## The aim of this project
- Find a use case of the noise
- Build a random number generator with a quantum computer using only noise
- Connect the project with IBM cloud
- Create a Discord bot with the help of Quantum Simulator

## **How to create a Noisy Quantum Random Number Generator?**

There are several ways to generate randomness. The easiest and oldest is to role a dice and see what number appears. But as this method is slow and not very modern, today computational methods are used. These methods are only pseudo random, because they are based on algorithms. A physical phenomenon which is random is noise. As noise is always present in the hardware of quantum computers, we can use this noise to our advantage to create a Random Number Generator. This is a use case of noise.

In the following sections, we want to describe why and for what a random number generator is useful. We show how we implemented a random number generator with the Qasm Simulator and a real backend from IBM. Besides it is demonstrated how to test the randomness of the numbers and a use case for these numbers as well as another way to acquire random numbers.

### **Why do we need a Random Number Generator?**

Random numbers are needed in many applications, such as: 

1. for Simulations
PCB (printed circuit boards) designs are often simulated with a [Monte-Carlo simulation](https://resources.pcb.cadence.com/blog/2019-monte-carlo-analysis-and-simulation-for-electronic-circuits) where a very large number of similar random experiments is performed to receive information about the manufacturing processes.
2. for electronic games
Random numbers are used in electronic games to simulate the shuffling of cards  or to generate realistic looking tree models (this is done with [procedural generation](https://medium.com/qiskit/introducing-a-quantum-procedure-for-map-generation-eb6663a3f13d)).
3. for Cryptography
To encrypt and decrypt data, keys are used which depend on random numbers.

In our project we decided to use random numbers to build a Discord bot which tells random quantum jokes.

### **Creating NQRNG on Qiskit Qasm Simulator**

We first build a basic bit flip error noise model and map it to the Qasm Simulator. This approach is similar to what is given in Qiskit Tutorials. It is a simple noise model which is often used in research.

The different probabilities for an error to occur are, from [Qiskit documentation](https://qiskit.org/documentation/tutorials/simulators/3_building_noise_models.html):

> When applying a single qubit gate, flip the state of the qubit with probability p_gate1.

> When applying a 2-qubit gate apply single-qubit errors to each qubit.

> When resetting a qubit reset to 1 instead of 0 with probability p_reset.

> When measuring a qubit, flip the state of the qubit with probability p_meas."

```python
# Error probabilities
p_reset = 0.03
p_meas = 0.1
p_gate1 = 0.05

# QuantumError objects
error_reset = pauli_error([('X', p_reset), ('I', 1 - p_reset)])
error_meas = pauli_error([('X',p_meas), ('I', 1 - p_meas)])
error_gate1 = pauli_error([('X',p_gate1), ('I', 1 - p_gate1)])
error_gate2 = error_gate1.tensor(error_gate1)

# Add errors to noise model
noise_bit_flip = NoiseModel()
noise_bit_flip.add_all_qubit_quantum_error(error_reset, "reset")
noise_bit_flip.add_all_qubit_quantum_error(error_meas, "measure")
noise_bit_flip.add_all_qubit_quantum_error(error_gate1, ["u1", "u2", "u3"])
noise_bit_flip.add_all_qubit_quantum_error(error_gate2, ["cx"])

print(noise_bit_flip)
```

We create a quantum circuit full of I and CX gates. I and CX essentially have no effect on the circuit. They are there to add ample of noise. The number of repetitions was chosen to be 200, to amplify the noise which appears after every repetition.

![/assets/images/NQRNG/3Q_circuit_2.png](/assets/images/NQRNG/3Q_circuit_2.png)

This circuit without noise should have no effect, i.e., output ‘000’ but with ample of noise results in random numbers.

![/assets/images/NQRNG_results_3q.png](/assets/images/NQRNG/NQRNG_results_3q.png)
 
### **Creating NQRNG using real hardware**

To verify the noisiness of the circuit on a real device, we created a quantum circuit with 3 qubits. The quantum circuit also contains I and CX gates.

![/assets/images/NQRNG/3Q_circuit_2%201.png](/assets/images/NQRNG/3Q_circuit_2%201.png)

```python
backend = provider.backends.ibmqx2
real_circ = QuantumCircuit(3, 3)
for i in range(200):
    real_circ.u3(0,0,0,0)
    real_circ.u3(0,0,0,1)
    real_circ.u3(0,0,0,2)
    real_circ.cx(0,1)
    real_circ.cx(1,2)
    real_circ.cx(2,0)
    real_circ.barrier()

real_circ.measure([0, 1, 2], [0, 1, 2])

job_exp = execute(real_circ, backend=backend, shots=8192)
print(job_exp.job_id())

job_monitor(job_exp)
exp_result = job_exp.result()

exp_measurement_result = exp_result.get_counts(real_circ)
print(exp_measurement_result)
plot_histogram(exp_measurement_result, color='midnightblue', title="NQRNG result on IBM Yorktown backend")
```

On the real device the number of repetitions of the code was restricted to 200, because of the decoherence time. The results are not as random as the ones on the simulator, but still are random.

The results are not as equally distributed as the results of the simulated circuit (with the bit flip error). The different distribution is due to the fact that the error which occur in the real device are not the same that are assumed in the bit flip error model.

![/assets/images/NQRNG/resultsonQasmAndYorktown.png](/assets/images/NQRNG/resultsonQasmAndYorktown.png)

### **Testing QRNG with FFT**

Sometimes a source for noise can be a specific frequency (aka energy) and thus is not random. To check this, we made a Fast Fourier Transform (FFT) and plotted the solution of this FFT into a graph were it can be seen if all the numbers are equally distributed over the frequency range.

```python
t = .1 #some time

n = 1000 #n-number of datapoints

for i in range(1000): 
    l.append(random_number()) 
    
fhat=np.fft.fft(l,n) #f-data ,n-number of datapoints per set

freq=(1/(dt*n))*np.arange(n)

PSD2=np.log(np.abs(np.fft.fftshift(fhat))**2)

plt.plot(freq.real,PSD2.real)
plt.xlabel('frequency')
plt.ylabel('number of occurence')
plt.show()
```

The FFT was realized with Pythons *Numpy* were the FFT is already implemented. To visualize the FFT we used *matplotlib*. Above, the program we used can be seen. Because we didn’t have a time dependent signal, we chose *dt* to be 0.1, but any other time step could have been used. *n* is the number of data points per data set, so let’s say we make 10 measurements and each measurement gives us 1000 data points; that’s the number which should be inserted for *n*. The last variable is the data point *l.* Then the FFT is calculated with the command *fft.fft(l,n),* the frequency is calculated and to get the amount of occurrences the power spectral density (PSD) is calculated, in the code above it is marked as *PSD2*.

As can be seen in the graph, the numbers are symmetrical distributed left and right from 5 Hz. This is because of how the FFT is calculated (with a series expansion of sin() and cos()), as well as the peak at 5 Hz. So we can say that at the first glance our numbers are random.

![/assets/images/NQRNG/fft.png](/assets/images/NQRNG/fft.png)

### Creating a QRNG from dephasing in a qubit, using Qiskit Pulse

Dephasing is the phenomenon when a qubit kept in a superposition state starts to disperse into a classical mixture of quantum states, i.e, a mixed state and eventually becomes a random mixture, losing all the information it held. This is a major problem in quantum computers today and one that quantum error correction protocols try to fix. However, in the experiment we are about to do, we will harness this randomness (noise) to create a Quantum random number generator.

|**The idea:** We will pulse a single qubit into an equal superposition of \|0> and \|1> and wait until it disperses into a mixed state before we measure it in the computational basis.

![/assets/images/NQRNG/hahn_echo-gif.gif](/assets/images/NQRNG/hahn_echo-gif.gif)

|The experiment described in Step 4 excluding the final pi/2 pulse. ([Source: Wikipedia - Spin Echo](https://en.wikipedia.org/wiki/Spin_echo))

The phenomenon (excluding the measurement step) can be viewed in the picture above.

**Experiment construction:**

- *Step 1:* **Calculate Qubit frequency** by Sweeping in the frequency domain and checking for an absorption
- *Step 2:* Conduct the Rabi Experiment to **calibrate a pi pulse** (pulse equivalent of an X gate)
- *Step 3:* **Measure T1** (time it takes for a qubit to decay from the excited state to the ground state) using inversion recovery
- *Step 4:* Use a pi/2 pulse and attach a delay to **let dephasing add randomness,** then apply another pi/2
- *Step 5:* **Measure the qubit** in the computational basis

Most of these steps have been explained in depth in the Qiskit textbook chapter, “[Calibrating qubits using qiskit pulse](https://qiskit.org/textbook/ch-quantum-hardware/calibrating-qubits-pulse.html#hahn)”. Step 4 is similar to the Ramsey experiment done in the chapter to find the exact frequency of the qubit. In the Ramsey experiment in the chapter an offset frequency and a maximum delay of 1.8 microseconds(μs) are applied; however, in Step 4 the delay we apply is about 100 microseconds(μs) for us to observe the dephasing phenomenon. 

The reason for calculating the value of T1 is to ascertain the amount of delay to give our pulse so that the errors will be due to effects of dephasing and not due to us crossing the relaxation time (time after which there is a significant chance that a qubit initially in the state \|1> comes down to the ground state \|0>). Once we found that the value of T1 is about 170 μs, we fixed our delay to about 100 μs and conducted the experiment (Step 4 + Step 5) 60 times. In each experiment run, 1024 shots were executed.

![/assets/images/NQRNG/222.png](/assets/images/NQRNG/222.png)

|Best Result, 1024 shots

You can find the final notebook here: [https://github.com/rochisha0/quantum-ugly-duckling/blob/main/quantum-ugly-duckling-main/notebooks/pulse_method.ipynb](https://github.com/rochisha0/quantum-ugly-duckling/blob/main/quantum-ugly-duckling-main/notebooks/pulse_method.ipynb)

## **How to connect a NQRNG with IBM Cloud?**

We chose Cloud Foundry and Cloudant in IBM Cloud. To get any funny Qadjokes (which means Quantum dadjokes), we built a website linked to a database for saving Qadjokes. Then we made a Qadjoke bot and connected it with the database.

For choosing a random Qadjoke, we connected our bot with the NQRNG that we made before. Get a random number from the NQRNG and read the database to choose a Qadjoke with the random number. Type "!Qadjoke" on Discord. Our Discord bot will say that Qadjoke!

![/assets/images/NQRNG/1111.gif](/assets/images/NQRNG/1111.gif)

|How the Qadjoke bot works

## **Conclusions**

The entire code can be found in the github repository shared: [https://github.com/rochisha0/quantum-ugly-duckling](https://github.com/rochisha0/quantum-ugly-duckling)

Also, you can invite our lovely duck to your Discord server!

- Official Qadjoke bot server: [https://discord.gg/3UdGBAC](https://discord.gg/3UdGBAC)
- If you want to invite our Qadjoke bot, [click it!](https://discord.com/api/oauth2/authorize?client_id=763802062370111498&permissions=67584&scope=bot)

**References and links**

- [https://en.wikipedia.org/wiki/Fast_Fourier_transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform)
- [https://www.youtube.com/watch?v=V4CwN4rEtVQ](https://www.youtube.com/watch?v=V4CwN4rEtVQ)
- [https://arxiv.org/abs/1801.00862](https://arxiv.org/abs/1801.00862)
- [https://en.wikipedia.org/wiki/Pseudorandom_number_generator](https://en.wikipedia.org/wiki/Pseudorandom_number_generator)
- [https://blog.cloudflare.com/randomness-101-lavarand-in-production/](https://blog.cloudflare.com/randomness-101-lavarand-in-production/)
- [https://qiskithackathon.global.bemyapp.com/#/projects](https://qiskithackathon.global.bemyapp.com/#/projects)
- [https://resources.pcb.cadence.com/blog/2019-monte-carlo-analysis-and-simulation-for-electronic-circuits](https://resources.pcb.cadence.com/blog/2019-monte-carlo-analysis-and-simulation-for-electronic-circuits)
- [https://medium.com/qiskit/introducing-a-quantum-procedure-for-map-generation-eb6663a3f13d](https://medium.com/qiskit/introducing-a-quantum-procedure-for-map-generation-eb6663a3f13d)
- [https://qiskit.org/documentation/tutorials/simulators/3_building_noise_models.html](https://qiskit.org/documentation/tutorials/simulators/3_building_noise_models.html)
- [https://qiskit.org/textbook/ch-quantum-hardware/calibrating-qubits-pulse.html#hahn](https://qiskit.org/textbook/ch-quantum-hardware/calibrating-qubits-pulse.html#hahn)
- [https://github.com/rochisha0/quantum-ugly-duckling/blob/main/quantum-ugly-duckling-main/notebooks/pulse_method.ipynb](https://github.com/rochisha0/quantum-ugly-duckling/blob/main/quantum-ugly-duckling-main/notebooks/pulse_method.ipynb)
