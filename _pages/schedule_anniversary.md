---
permalink: /schedule_anniversary/
title: "Schedule Anniversary"
---

It is with great encouragement that we share with you the talks that have been accepted for the event on 14 and 25 July 2021.<br>

The schedule will be posted later, for the moment we share with you the accepted talks and their abstracts.<br>

<div id="schedule_anniversary"></div>
<script>
var author = [
"Lia Yeh",
"Alberto Maldonado Romo",
"Kevin Jofroit Joven Noriega",
"Victor Onofre and F. Rojas",
"Wen-Sen Lu",
"Md. Sakibul Islam",
"Leonardo Calderón",
"Elliot Evans",
"AJMAL IBN MOHAMMED ALTHAF",
"Claudia Zendejas-Morales",
"Dante Bencivenga",
"Emilio Peláez and Minh Pham",
"Jitesh Lalwani",
"Joonho Kim",
"Kathrin Koenig",
"Pinaki Sen",
"Dayeong Kang",
"Rana Prathap Simh Mukthavaram",
"Rodrigo Pires Ferreira",
"Rukhsan Ul Haq",
"Sagnik Banerjee",
"Sansriti Ranjan",
"Zeki Seskir",
"Adam Fattal",
"John van de Wetering"];
  
 
var affiliation = [
"PhD student, Quantum Group, University of Oxford"
"PhD student, Center for Computing Research - Instituto Politecnico Nacional",
"Student at Universidad del Valle and intern at Purdue University",
"Center of Nanoscience and Nanotechnology (CNyN)",
"Qiskit advocate",
"B.Sc (Engg.) in Electrical and Electronic Engineering",
"Software Engineer and Quantum Enthusiast",
"elliot.website",
"MSc Physics student, Q Enthusiasts Kerala",
"Teacher Assistant at UNAM and Intern at Quantum Flytrap",
"qcsimplify.com",
"Research Intern at Weizmann Institute of Science & Undergraduate mathematics student at the University of Chicago.",
"Founder of a Quantum Computing Startup",
"Institute for Advanced Study",
"PhD Student at Fraunhofer IAF and University Freiburg",
"Engineering Undergrad at NIT Agartala, INDIA and Research Intern at ISI Kolkata, INDIA",
"",
"Qiskit Advocate, Mathematics and Computing at IIT Kharagpur, AI Architect at MapRecruit.ai",
"Co-founder at Brazil Quantum | BSc/MSc student at the Aeronautics Institute of Technology",
"Quantum Scientist, IBM",
"Jadavpur University",
"Research student at Future Technologies in High Performance Computing at Clemson University",
"Board member at QWorld and Research Assistant at METU Physics Department",
"Undergraduate of Physics",
"Oxford University"]
  
  
var title = [
"Quantum gates: software vs hardware implementation",
"Classification of the MNIST dataset using quantum knn and quantum neural networks.",
"Simulating Quantum Circuits on Classical Hardware using FPGA",
"Discord-type quantum correlations in the radical pair mechanism for magnetoreception in birds",
"QArcade: A table-top arcade machine for quantum game developers",
"Introduction to Ion Trap Hardware, scaling and its future",
"Q-Dino: A Quantum version of the classical game of Chrome Dinosaur",
"What If You Could See Qubits!?",
"Digital Divide in Quantum Education",
"Incorporating the advantages of ZX-calculus in the Tequila platform",
"QC Simplify: An online tool to simplify and commute quantum gates on the fly",
"On the recursive construction of relative phased multiple controlled Toffoli",
"quantumcat - Cross-Platform Open-Source Quantum Computing Library",
"Quantum Energy Landscape and Variational Quantum Algorithms",
"Error Extrapolation: an Introduction to Richardson Extrapolation",
"Hierarchical Extreme Quantum Machine Learning with Tensor and Neural Networks in the NISQ Era",
"My projects with Qiskit",
"Building Retro-Style Quantum Games for Arduino from scratch",
"Solving Linear Differential Equations via Quantum Algorithms",
"Quantum Oracles",
"Engineering the quantum dynamics in 2-D honeycomb systems",
"Research student at Future Technologies in High Performance Computing at Clemson University",
"The Landscape of Academic Literature in Quantum Technologies",
"Hosting a Workshop: What I learned",
"Doing quantum computing using pictures"];
  
  
 var img = [
"q_architecture",
"qml",
"q_software",
"q_sensing",
"q_game",
"q_hardware",
"q_software",
"q_game",
"q_learning_resource",
"q_learning_resource",
"q_architecture",
"q_learning_resource"];
  
var abstract = [
"Unlike for classical computers, for quantum computers, present-day quantum assembly languages do not correspond to physical hardware operations.  Although gate-based quantum computers which implement a universal gateset can run any qubit operations, for the implementation to be efficient, the desired gate needs to be decomposed into gates the hardware can run.  This talk is a primer on quantum computer architecture, specifically how quantum software is compiled to quantum assembly language and then to quantum hardware.",
"Quantum computing has initiated a great popularity to be able to perform in different environments quantum algorithms that some claim to reach a quantum supremacy, one of the most popular areas is the Quantum Machine Learning (QML) as there are equivalents to the models, such as neural networks, support machines, nearest neighbor, and that these manage to perform a Supervised Learning to classify from a set that we know its result. Our proposal uses quantum circuits to represent a neural network following the format of parametric quantum circuits and using Grover's algorithm and a complex data storage structure known as quantum RAM (QRAM) that has a complexity O(log(n)) to read a state of information with the use of the SWAP Test for the quantum nearest neighbor. These examples developed in two popular environments which are Qiskit as in PennyLane we managed to obtain an accuracy greater than 80% considering that it is a two-class classifier.",
"One of the main actual problems in quantum computing is related to the number of qubits that can have the hardware implementation, also that can difficult the limitation of the algorithms and also that the algorithms can have errors due to the environment. We present a hardware implementation on FPGA that can emulate quantum circuits with a certain architecture that gives all the probabilities distribution of the quantum circuit outcomes.",
"The leading hypothesis to explain how migratory birds can detect the direction of the Earth's magnetic field is the Radical-Pair mechanism, which is by now a well-established theoretically and experimentally mechanism. The radical pairs oscillate between singlet and triplet states. The Earth's magnetic field direction influences the probability of finding them in one state or another. The yield of these states controls the neural signals of the bird's retina, providing the basis for magnetoreception. This research studies quantum correlations in the mechanism of radical pairs, working with discord-type quantifiers. In the first stage of the work, the dependence of the angle of the Earth's magnetic field and the singlet yield was investigated, consistent with the different studies on the mechanism of radical pairs. In the second stage, discord-type quantifiers were calculated as a function of the angle of the Earth's magnetic field, finding a dependence similar to that of the singlet yield.",
"It is our privilege to explore the cutting-edge quantum computational space during the NISQ era with qiskit. Looking back into the history especially in the 1970’s, arcade game developers already started the machine-level programming and prepared themselves as the future coders even if the hardware was still limited. In the meanwhile, game-driven breakthrough for the classical hardware, such as the first 3D acceleration chip Super FX in Nintendo super-NES home console, also demonstrated the possibilities where new hardware could be inspired by the game developers.In this project, we hope to contribute to quantum education by leveraging the experience of classical arcades in the 70’s. The motivation of this project is to help quantum enthusiastic building a classical machine hosting quantum development environment. It could be game development platform such as PICO-8 with micro-qiskit or full-fledged Python3 environment with Thonny which allows developers to access the full power of qiskit.Indeed, for mature users such as graduate student with physics or computer science background it is perhaps more straightforward for them to use qiskit on their laptops for some serious quantum simulations, while this project is aiming at K-12 students and educators who has rather limited experience regarding quantum physics and/or programming. For these audiences PICO-8 and micro-qiskit offer a simple yet concise platform for the to concentrate on their creativity to navigate the quantum ideas such as superposition and entanglement. Read more about this project here: https://github.com/wslu42/QArcade",
"Several physical implementations of qubits exist to employ quantum computational advantages, some of them are superconducting qubits, ion-trap, quantum dots. Out of all of this trapped ion technology has a good amount of potential, although superconducting qubits are the most common one. Basically ion is trapped in an energy function saddle point to harness the qubit property from the ion. An introduction of this promising technology will be discussed and shared its advantages over superconducting properties. Some meticulous procedures are followed to make quantum gates and at the end of the talk, we will discuss its scaling techniques and future potentials.",
"The world of videogames is mainly based on reaching a goal using to your advantage the effects that were determined by games designers for each of the actions that the player can perform through an interface. Let's give an example, the game of the chrome’s dinosaur has as its main goal to avoid the obstacles and get all the possible points, the actions of the player are to press the spacebar and the effect on the dinosaur of that action is jump. On the other hand, quantum computing has different applications, including the use of quantum properties in video games, one of the main characteristics that we can find is the use of qubits, information units and the analog of bits in classical computing. Qubits can be manipulated using quantum gates, which in turn can be arranged into quantum circuits. Putting these two ideas together, we decided to create a new video game in which the effects do not depend totally on the player actions or video game designer. Taking up the example of the classical chrome’s dinosaur, we developed a game in which the user has control over a set of quantum gates and their position in a quantum circuit, then based on a framework that can simulate quantum circuits such as Qiskit of IBM, we get the results which determine whether the dinosaur jumps or ducks. We hope you enjoy and learn a lot with this game.",
"Understanding qubits through math only goes so far...sometimes you just need to look at them with your eyeballs. In this session I'll talk about some inspiring approaches to making qubits visual and interactive, my decisions and lessons learned while creating a gamified quantum circuit editor for beginners (elliot.website/qubit), and some of my ideas for how qubits could be visualized in the future.",
"We live in a society where all the classes have gone from offline mode to online mode all of a sudden in a year. The digital divide, as we know is the inaccessibility to technology and gadgets. Nowadays education is just a privilege only for those who have access to technology. The same issue is there in the domain of quantum education. Quantum computing is relatively a new field and because of this, not everyone has prior exposure to it. To bridge the issue there are a lot of quantum education initiatives and many of them are free. The question is does everyone have access to quantum education in online mode. In Kerala, which is my state there is smartphone access is there for 90% of the students, but for quantum education, the smartphone is not enough. We need computer access for using quantum computing platforms or for coding. There are only 10-20 % of students who use computers for their education and this makes a huge gap in accessing the quantum world. My talk focuses on representing the issues in the first part. The second part address some of the possible solution in reducing the digital divide and how to be more inclusive in the quantum world. The solution discussed is regarding how learning materials can be made available offline, how local science communities and volunteers from quantum universal education can help in teaching quantum computing.",
"Tequila's main goal is to simplify and accelerate the implementation of new ideas for quantum algorithms, allowing algorithms to be prototyped and subsequently transforming the resulting circuits and executing them in quantum simulators or interfaces. In order to execute optimized circuits, we sought to take advantage of the benefits of ZX-calculus, incorporating the functionality of converting Tequila circuits to PyZX circuits and vice versa, through OpenQASM code, an intermediate representation for quantum instructions. With this extension to the Tequila platform, the optimization of circuits is achieved by reducing the T-count, the number of non-Clifford quantum gates, by up to 28%.",
"Quantum circuits feel less intuitive than classical circuits. I'm developing QC Simplify (qcsimplify.com) with the goal of helping people new to quantum computing gain a better intuition for how the order of quantum gates changes the behaviour of a quantum circuit. It uses a simple drag-and-drop interface, where you can drag gates across each other to automatically apply a commutation rule that keeps the circuit’s behaviour the same. When you place a new gate by letting go of it on the circuit, it will cancel with adjacent gates (when possible) to simplify the circuit. I will give a demo of the current capabilities of the website and propose some possible future directions, and will gladly listen to any ideas you bring for improvements!",
"We propose an efficient construction for multiple controlled-NOT gates that allows for relative phase difference in the output of the gate and uses no additional qubits other than n control qubits and one target qubit. We employ a recursive construction using three base cases: the phaseless CNOT, the phased Toffoli, and the phased triple controlled-NOT; the latter two are known constructions from previous literature on the subject. To prove its correctness, we use the method of exhaustion, checking all different gate and parameter combinations. Finally, we derive an upper bound on the complexity of our technique and compare it to the recently known construction of complexity 9n + O(1) CNOT gates.",
"Quantumcat is a cross-platform library and is built on the principle of write once and execute on any quantum provider. Developers just have to follow one syntax and could execute their circuit in one of the supported platforms such as Google Cirq, IBM Qiskit, IonQ, and Rigetti (Few others are in progress) without the need to write code in multiple syntaxes. More info on: https://quantumcat.io/",
"Variational Quantum Algorithm (VQA) is a major application of the near-term hybrid computing model that jointly uses a classical computer to handle continuous variables and a quantum computer to generate variational wavefunctions controlled by those variables. Many computing problems are formulated as optimization problems in this framework to find out the global minimum in the quantum energy landscape. In this talk, I will explain two main design factors for efficient VQA optimization, i.e., the entangling capability and number of control parameters of the variational wavefunction, by analyzing how they influence the geometric shape of the quantum energy landscape.",
"In NISQ era, quantum computers are not perfect and errors prevent them from being useful. Among the sources of errors, gate errors are significant. To reduce these errors an active error mitigation can be used. By amplifying the errors and then extrapolating, those to zero errors will increase the performance of NISQ devices. In my talk, I would like to give an introduction to what are sources of errors and to the method of error mitigation with Richardson extrapolation.",
"Recently, the closeness between the techniques used in classical machine learning and quantum-many body physics has got significant attention among the academic and research communities. Especially, the deep learning frameworks and tensor networks hold similar properties such that they can be used for machine learning tasks. In noisy intermediate-scale quantum (NISQ) technology, the quantum circuits with a long circuit depth or a large number of qubits cannot be implemented on NISQ devices. It is highly demanding to develop applications with adequate resources which can exploit the quantum advantages. In this paper, we proposed the architecture of hierarchal extreme quantum machine learning consisting of quantum tensor variants of autoencoder (i.e. Tree tensor network (TTN), multi-scale entanglement renormalization ansatz (MERA)) and quantum neural network (QNN) for binary classification. The proposed hierarchical architecture has the ability to overcome the shortcomings of regular tensor networks and can be defined in complex geometries efficiently as long as the order can be represented appropriately. We apply the quantum variants of TTN and MERA for image compression and quantum neural networks to classifying the images and compare their performance, concluding that the combination of TTN performs better than MERA with QNN for image classification.",
"I will talk three qiskit projects, and these have a same thing which are using cloud. (1) Quantum Ugly Duckling: making a discord bot with NQRNG. For this project, I used IBM Cloud server and database to sabe quantum dad jokes. (2) Qoupang: quantum blockchain service for logistics. Our team used a cloud server and QRNG for making a hash value of each block. (3) Qiskit Textbook Master: a quiz app for learning qiskit textbook. Using a web-hosting service in Github, give a bundle of quizzes to help learning. Main focus will be You can make these quantum projects easily!",
"Building retro quantum games in general is a task that’s super fun and in my opinion one of the best ways to cement your basic quantum computing concepts. However, Quantum games today are usually built for relatively powerful microprocessors such as a Raspberry pi or for a computer. These chips tend to be relatively expensive and honestly just aren’t fun to build retro games on - as you already have libraries like Pygame to help you along the process. The aim of this project was to build a retro handheld using an Arduino and program a game based on quantum computing onto it.  During this talk I’ll be sharing the process of how I built the quantum game, provide the code and circuit schematics so you can play and build on it yourself!",
"Several natural phenomena are described by differential equations - which are also used to model quantum systems. Simulating those systems in a quantum computer implies solving a particular set of linear differential equations (LDEs) using quantum algorithms. We use the same techniques to solve a broader set of LDEs, by representing their solutions via Taylor Series and decoding them into qubits. We use Yao Quantum (an efficient open-source framework for quantum algorithm design), written in Julia, to perform simulations with a 10 relative error.",
"Quantum oracles are the fundamental primitives of many quantum algorithms like Deutsch-Jozsa, Grover, Quantum amplitude estimation. So, understanding quantum oracles is crucial for understanding these quantum algorithms and other generalized versions of them as well. In my talk I will try to give a pedagogical introduction to quantum oracles and discuss some of their applications which have been recently explored.",
"An exciting playground for exploring quantum dynamics in the nano-scale is a 2D honeycomb system. With the evolution of nano-electronics and continued miniaturization of devices, it became evident that 2D materials would not only empower us to engineer novel devices, but also aid understanding the rich physics involved. It is no myth that all major breakthroughs in condensed matter physics have some sort of motivation drawn from hexagonal lattices. Graphene, among many others, is one such awesome 2D material, which could be cleverly ‘quantum-engineered’ to design robust ‘topological quantum devices’ or maybe applications in spintronics or in the whole new field of ‘valleytronics’. From an enormous rise in computational power to significant decrease in power consumption, the possibilities are endless. In this talk, I share some of my ‘quantum thoughts’ to introduce the fascinating world of honeycomb systems.",
"Addressing data movement bottlenecks in HPC and other applications is important to improve storage and I/O performance. Data compression (lossy or lossless) helps in reducing the number of bytes that must be transmitted or stored. Caching is another method that helps in reducing data movement by keeping data required for computation in fast memory. Previously, it has been explored that hardware compression can be used to expand size of hardware caches and main memory or caching at the software level. Softwares caches further improve the I/O performance for distributed applications and cache the input data for parallel tasks. One of the main applications of compression and caching in quantum computing is in reducing the memory footprint for quantum circuit simulations. In quantum computing research, using classical HPC systems to simulate quantum computers is integral for understanding behavior of quantum computing systems. These simulations allow developers to evaluate complexity of new quantum algorithms and validate the design of quantum devices. Therefore, through this research we aim to build a cache simulator which can be used to assess the performance of different compressors as they cache for compressed blocks of various HPC applications or quantum simulations. This simulator can then be used to run different benchmarks (quantum approximate optimization algorithm (QAOA), Quantum Fourier Transform (QFT), Grover’s Search Algorithm) and then choose the compressor based on its cache performance.",
"In this study, we investigated the academic literature on quantum technologies (QT) using bibliometric tools. We used a set of 49,823 articles obtained from the Web of Science (WoS) database using a search query constructed through expert opinion. Analysis of this revealed that QT is deeply rooted in physics, and the majority of the articles are published in physics journals. Keyword analysis revealed that the literature could be clustered into three distinct sets, which are (i) quantum communication/cryptography, (ii) quantum computation, and (iii) physical realizations of quantum systems. We performed a burst analysis that showed the emergence and fading away of certain key concepts in the literature. This is followed by co-citation analysis on the “highly cited” articles provided by the WoS, using these we devised a set of core corpus of 34 publications. Comparing the most highly cited articles in this set with respect to the initial set we found that there is a clear difference in most cited subjects. Finally, we performed co-citation analyses on country and organization levels to find the central nodes in the literature. Overall, the analyses of the datasets allowed us to cluster the literature into three distinct sets, construct the core corpus of the academic literature in QT, and to identify the key players on country and organization levels, thus offering insight into the current state of the field.",
"Quantum Computing is a rapidly emerging field that is gaining a lot of interest not only within academia, but also within other areas  such as industry and the business world in general. For this reason,  a lot of interest in "adapting to quantum" is being displayed by a notable subset of the STEM (and in some cases, even  the non-STEM) community. As a consequence, many opportunities are available in the field of  quantum education that people, even beginners at the undergraduate level (such as myself), can exploit. Here, I will discuss The Eigensolvers,  a group of students who have an avid interest in quantum computing,  as well as our first global workshop. I will also give tips for  anyone who is interested in pursuing something similar and talk about future plans and how you can contribute to them.",
"In this talk I will give a brief introduction to the ZX-calculus, a graphical language for reasoning about quantum computation. I will give a demonstration of our software PyZX which allows you to do quantum circuit rewriting on a massive scale."]; 
  
var data = [];
var length = author.length; // user defined length

for(var i = 0; i < length; i++) {
    data.push(i);
}

data.sort(() => Math.random() - 0.5);
  
  
var first = Math.floor(Math.random() * img.length);
var html_str = "";
var i;
for (i = 0; i < title.length; i++) {
  var idx = (first + i) % title.length; 
  html_str += "<div style=\"border: 0px solid black; width: 65vw; padding: 0px; margin: 0px; text-align: center\"><p style=\"text-align:left; font-size:22px; font-weight: bolder; \">" + author[data[idx]] + "</p><p style=\"text-align:left; font-size:22px; font-weight: bolder; \">" + affiliation[data[idx]] + "</p><p style=\"text-align:left; font-size:20px; font-weight: bolder; \">" + title[data[idx]] + "</p><div  style=\"display: table;\"><p style=\"text-align:left; font-size:18px; display: inline-block;float: left;  width: 100%;\">"+ abstract[data[idx]]+"</p></div></div><br>\n";

                          
}
document.getElementById("schedule_anniversary").innerHTML = html_str;

</script>
