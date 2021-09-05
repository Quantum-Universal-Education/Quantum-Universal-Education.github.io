---
permalink: /anniversary/
layout: archive
---

<link href="/assets/css/areas.css" rel="stylesheet" type="text/css">
<link rel="shortcut icon" type="image/png"  href="/assets/images/FSQC-small.png" />
<link rel="stylesheet" href="styles.css">

<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
<link href="http://www.jqueryscript.net/css/jquerysctipttop.css" rel="stylesheet" type="text/css">
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>
<style>
.button {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 16px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  transition-duration: 0.4s;
  cursor: pointer;
}

.qontributor {
  background-color: white;
  color: black;
  border: 2px solid #6d2f15;
  width: 100%;
}
.qontributor:hover {
  background-color: #6d2f15;
  color: white;
  width: 100%;
}


.qurator {
  background-color: white;
  color: black;
  border: 2px solid #005853;
  width: 100%;
}
.qurator:hover {
  background-color: #005853;
  color: white;
  width: 100%;
}

* {
  box-sizing: border-box;
}

.column {
  float: left;
  width: 50%;
  padding: 5px;
}

/* Clearfix (clear floats) */
.row::after {
  content: "";
  clear: both;
  display: table;
}

.page__footer {color: #FFFFFF;font-size: 16px;}
.site-logo img {
  max-height: 4rem;
}

.page__footer-copyright {
  font-size: 20px;
}


div p{
text-align: justify;”
}
	
.archive{
display: flex;
align-items: center;
flex-direction: column;
}	
* {
  box-sizing: border-box;
}

/* Create two equal columns that floats next to each other */
.column {
  float: left;
  width: 45%;
  padding: 10px;
  height: 700px /* Should be removed. Only for demonstration */
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}	
	
* {
  box-sizing: border-box;
}

body {
  font-family: Helvetica, sans-serif;
}

/* The actual timeline (the vertical ruler) */
.timeline {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
}

/* The actual timeline (the vertical ruler) */
.timeline::after {
  content: '';
  position: absolute;
  width: 6px;
  background-color: #00833C;
  top: 0;
  bottom: 0;
  left: 50%;
  margin-left: -3px;
}

/* Container around content */
.container {
  padding: 10px 40px;
  position: relative;
  background-color: inherit;
  width: 50%;
}

/* The circles on the timeline */
.container::after {
  content: '';
  position: absolute;
  width: 25px;
  height: 25px;
  right: -17px;
  background-color: white;
  border: 4px solid #280A7D;
  top: 15px;
  border-radius: 50%;
  z-index: 1;
}

/* Place the container to the left */
.left {
  left: 0;
}

/* Place the container to the right */
.right {
  left: 50%;
}

/* Add arrows to the left container (pointing right) */
.left::before {
  content: " ";
  height: 0;
  position: absolute;
  top: 22px;
  width: 0;
  z-index: 1;
  right: 30px;
  border: medium solid grey;
  border-width: 10px 0 10px 10px;
  border-color: transparent transparent transparent white;
}

/* Add arrows to the right container (pointing left) */
.right::before {
  content: " ";
  height: 0;
  position: absolute;
  top: 22px;
  width: 0;
  z-index: 1;
  left: 30px;
  border: medium solid grey;
  border-width: 10px 10px 10px 0;
  border-color: transparent white transparent transparent;
}

/* Fix the circle for containers on the right side */
.right::after {
  left: -16px;
}

/* The actual content */
.content {
  padding: 20px 30px;
  background-color: #A70024;
  position: relative;
  color: white;
  border-radius: 6px;
}

/* Media queries - Responsive timeline on screens less than 600px wide */
@media screen and (max-width: 600px) {
  /* Place the timelime to the left */
  .timeline::after {
  left: 31px;
  }
  
  /* Full-width containers */
  .container {
  width: 100%;
  padding-left: 70px;
  padding-right: 25px;
  }
  
  /* Make sure that all arrows are pointing leftwards */
  .container::before {
  left: 60px;
  border: medium solid white;
  border-width: 10px 10px 10px 0;
  border-color: transparent white transparent transparent;
  }

  /* Make sure all circles are at the same spot */
  .left::after, .right::after {
  left: 15px;
  }
  
  /* Make all right containers behave like the left ones */
  .right {
  left: 0%;
  }
}	



.view_item img{
	width: 75px;
}

.wrapper{
	width: 800px;
	margin: 20px auto;
}

.links{
	margin-bottom: 25px;
	background: #fff;
	padding: 15px;
	border-radius: 3px;
}

.links ul{
	display: flex;
	justify-content: center;
}

.links ul li{
	margin: 0 15px;
	font-weight: 600;
	text-transform: uppercase;
	letter-spacing: 3px;
	font-size: 20px;
	cursor: pointer;
}

.links ul li:hover,
.links ul li.active{
	color: #FE6A1A;
}

.view_main{
	background: #fff;
	border-radius: 3px;
	padding: 15px;
}

.list-view .view_item {
	background: #fff;
	border: 1px solid #e2efe1;
	margin: 10px;
	padding: 10px 20px;
	display: flex;
	align-items: center;
}

.list-view .view_item:last-child{
	margin-bottom: 0;
}

.list-view .view_item .vi_left{
	margin-right: 25px;
}

.view_item .title{
	font-weight: 600;
}

.view_item .content{
	margin: 5px 0;
	font-size: 14px;
	line-height: 22px;
	font-weight: 200;
}

.view_item .btn{
	width: 125px;
	background: #4abd3e;
	padding: 8px 5px;
	border-radius: 3px;
	color: #fff;
	text-align: center;
	font-weight: 200;
	cursor: pointer;
}

.view_item .btn:hover{
	background: #3bd62b;
}

.grid-view{
	width: 100%;
}

.grid-view .view_item {
	display: inline-block;
    border: 1px solid #e2efe1;
    width: 230px;
    padding: 25px;
    text-align: center;
    margin: 10px;
}

.grid-view .view_item .vi_left{
	margin-bottom: 10px;
}
</style>
<!-- Header -->

<header class="w3-container w3-padding-32" id="home" style="position:relative;text-align:center">

<div class="w3-container w3-padding-32" id="projects" style="width: 55vw;">
    <h2 class="w3-border-bottom w3-border-light-grey w3-padding-16">Anniversary</h2>
    <!--h4>This event is to celebrate our first anniversary in sharing the knowledge of quantum computing and for our community to share ideas, thoughts and their knowledge throughout this year.</h4-->
	<h4>This event is to celebrate our first anniversary in sharing the knowledge of quantum computing for our community. Time to celebrate and listen to everyone's quantum computing progress!</h4>
	</div>
<div style="width: 55vw">
	    <!--h4>Time to celebrate and listen to everyone's quantum computing progress.</h4-->
	<img src="/assets/images/anniversary-21_flyer.png" style="background-color: white;box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);display: block;  margin-left: auto;  margin-right: auto;  width: 50%;">
</div>
</header>
<div class="w3-container w3-padding-32" style="width: 40vw" >
<h2 style="color:#A70024;text-decoration: line-through;">Registration is now open!  Free to attend</h2>
<h2 style="color:#A70024;">If you missed registration, you can join via our <a href="https://discord.gg/NDm9e9W">Discord server</a> #pique-announcements channel</h2>
<!--button class="button qurator"  onclick="document.location='https://quantumuniversaled.typeform.com/to/hG70hI38'">Sign up to give a talk</button>
<button class="button qurator"  onclick="document.location='https://quantumuniversaled.typeform.com/to/OoTHmxDx'">Register for the event</button-->
</div>

<div class="w3-container w3-padding-32" style="width: 55vw;">	
	<h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">It is with great enthusiasm that we share with you the talks that have been accepted for the event on 24 and 25 July 2021.</h3>
	<h2 class="w3-border-bottom w3-border-light-grey w3-padding-16">Videos of the talks on 24 July</h2>
	<div class="wrapper">
		<div class="view_main"  style="width: 65vw;">
			<div id="video_anniversary_saturday" class="view_wrap list-view" style="display: block;">
				<!--div class="view_item" style="width: 65vw;">
					<p class="title">title</p>
						<div class="title">Autor</div>
					<div class="vi_left" style="width:40%;" >
						<iframe width="180" height="135" src="https://www.youtube.com/embed/YC88NyV5SuM"></iframe> 
					</div>
					<div class="vi_right" style="width:58%;" >
						<p class="content">Addressing data movement bottlenecks in HPC and other applications is important to improve storage and I/O performance. Data compression (lossy or lossless) helps in reducing the number of bytes that must be transmitted or stored. Caching is another method that helps in reducing data movement by keeping data required for computation in fast memory. Previously, it has been explored that hardware compression can be used to expand size of hardware caches and main memory or caching at the software level. Softwares caches further improve the I/O performance for distributed applications and cache the input data for parallel tasks. One of the main applications of compression and caching in quantum computing is in reducing the memory footprint for quantum circuit simulations. In quantum computing research, using classical HPC systems to simulate quantum computers is integral for understanding behavior of quantum computing systems. These simulations allow developers to evaluate complexity of new quantum algorithms and validate the design of quantum devices. Therefore, through this research we aim to build a cache simulator which can be used to assess the performance of different compressors as they cache for compressed blocks of various HPC applications or quantum simulations. This simulator can then be used to run different benchmarks (quantum approximate optimization algorithm (QAOA), Quantum Fourier Transform (QFT), Grover’s Search Algorithm) and then choose the compressor based on its cache performance.</p>
					</div>
				</div-->
			</div>
		</div>
	</div>
	
	<h2 class="w3-border-bottom w3-border-light-grey w3-padding-16">Videos of the talks on 25 July</h2>
	<div class="wrapper">
		<div class="view_main"  style="width: 65vw;">
			<div id="video_anniversary_sunday" class="view_wrap list-view" style="display: block;">

			</div>
		</div>
	</div>
</div>


<br> <br>	


<div class="w3-container w3-padding-32" style="width: 55vw;">	
	<h2 class="w3-border-bottom w3-border-light-grey w3-padding-16">Frequently Asked Questions (FAQ)</h2>	
	<div class="w3-container w3-padding-32" style="width: 55vw;">	
	<h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">When are the talks and meetups?</h3>	
	<p>The talks will be live on Zoom, on July 24th, and if need be the 25th.  The scheduling will begin after the talks are accepted.  Taking into account the speakers' availability, we will do our best to have most talks be when most people can attend, which is morning in western time zones and night in eastern time zones.  If the speaker has given permission, their talk will be publicly viewable afterwards on the FSQC Youtube channel.
The meetups will be spread out throughout July 24th and 25th.  The regional area and language meetups will be at most suitable times, while other topics and demographic meetups will be when most people can attend.</p>
	</div>
	<div class="w3-container w3-padding-32" style="width: 55vw;">	
	<h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">How do I join the meetups?</h3>	
	<p>To make it interactive and fun, most of the meetups will be on AltspaceVR, which is Microsoft's free/quick/easy to install computer virtual reality meetup.  As it is not supported for all platforms, we will also hold several meetups on Discord.
Although RSVP is not needed to join, we highly encourage you to RSVP as we will first email the event join links to those who RSVP'd for those meetup sessions, and then based on capacity open up meetup rooms through our Discord server [https://discord.gg/NDm9e9W].  RSVP'ing will enable you to sign up for the meetups you would like to join, which we then schedule based on your time zone and availability.  RSVP'ing will even allow you to suggest topics for a meetup room you'd like to see --- for each topic, so you can stay in contact after the meetup, we will make and moderate a text channel for that topic in the Discord server.</p>
	</div>
	<div class="w3-container w3-padding-32" style="width: 55vw;">	
	<h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">Are we going to hand out speaker certificates?</h3>	
	<p>Yes, only for accepted abstracts</p>
	</div>


</div>

<script>

var author_saturday = [
"Kevin Jofroit Joven Noriega",
"Wen-Sen Lu",
"Md. Sakibul Islam",
"Leonardo Calderón",
"Elliot Evans",
"Dante Bencivenga",
"Jitesh Lalwani",
"Kathrin Koenig",
"Rodrigo Pires Ferreira",
"Sagnik Banerjee",
"Sansriti Ranjan",
"Kushagra Sharma",
"Dayeong Kang"];



var affiliation_staturday = [
"Student at Universidad del Valle and intern at Purdue University",
"Qiskit advocate",
"B.Sc (Engg.) in Electrical and Electronic Engineering",
"Software Engineer and Quantum Enthusiast",
"elliot.website",
"qcsimplify.com",
"Founder of a Quantum Computing Startup",
"PhD Student at Fraunhofer IAF and University Freiburg",
"Co-founder at Brazil Quantum | BSc/MSc student at the Aeronautics Institute of Technology",
"Jadavpur University",
"Research student at Future Technologies in High Performance Computing at Clemson University",
"Student at Sacred Heart School",
""]
  
var title_saturday = [
"Simulating Quantum Circuits on Classical Hardware using FPGA",
"QArcade: A table-top arcade machine for quantum game developers",
"Introduction to Ion Trap Hardware, scaling and its future",
"Q-Dino: A Quantum version of the classical game of Chrome Dinosaur",
"What If You Could See Qubits!?",
"QC Simplify: An online tool to simplify and commute quantum gates on the fly",
"quantumcat - Cross-Platform Open-Source Quantum Computing Library",
"Error Extrapolation: an Introduction to Richardson Extrapolation",
"Solving Linear Differential Equations via Quantum Algorithms",
"Engineering the quantum dynamics in 2-D honeycomb systems",
"Research student at Future Technologies in High Performance Computing at Clemson University",
"Superposition and Quantum Coins",
"My projects with Qiskit"];
	
 var video_saturday = [
"https://www.youtube.com/embed/7anlxNPBdi0",
"https://www.youtube.com/embed/rXZ7xgbtXB0",
"https://www.youtube.com/embed/9JY9xUXSRj0",
"https://www.youtube.com/embed/xHOGpSY61XA",
"https://www.youtube.com/embed/BtHHz8h5Ygc",
"https://www.youtube.com/embed/dxqsNfeA-3M",
"https://www.youtube.com/embed/KqLos-j4dP8",
"https://www.youtube.com/embed/WC2Au-zHIS8",
"https://www.youtube.com/embed/TJrcWp2uBoQ",
"https://www.youtube.com/embed/4INMaL5ywwU",
"https://www.youtube.com/embed/YC88NyV5SuM",
"https://www.youtube.com/embed/rxTvHT6z6kA",
"https://www.youtube.com/embed/be5jlFmPaio"];

	
  var abstract_saturday = [
"One of the main actual problems in quantum computing is related to the number of qubits that can have the hardware implementation, also that can difficult the limitation of the algorithms and also that the algorithms can have errors due to the environment. We present a hardware implementation on FPGA that can emulate quantum circuits with a certain architecture that gives all the probabilities distribution of the quantum circuit outcomes.",
"It is our privilege to explore the cutting-edge quantum computational space during the NISQ era with qiskit. Looking back into the history especially in the 1970’s, arcade game developers already started the machine-level programming and prepared themselves as the future coders even if the hardware was still limited. In the meanwhile, game-driven breakthrough for the classical hardware, such as the first 3D acceleration chip Super FX in Nintendo super-NES home console, also demonstrated the possibilities where new hardware could be inspired by the game developers.In this project, we hope to contribute to quantum education by leveraging the experience of classical arcades in the 70’s. The motivation of this project is to help quantum enthusiastic building a classical machine hosting quantum development environment. It could be game development platform such as PICO-8 with micro-qiskit or full-fledged Python3 environment with Thonny which allows developers to access the full power of qiskit.Indeed, for mature users such as graduate student with physics or computer science background it is perhaps more straightforward for them to use qiskit on their laptops for some serious quantum simulations, while this project is aiming at K-12 students and educators who has rather limited experience regarding quantum physics and/or programming. For these audiences PICO-8 and micro-qiskit offer a simple yet concise platform for the to concentrate on their creativity to navigate the quantum ideas such as superposition and entanglement. Read more about this project here: https://github.com/wslu42/QArcade",
"Several physical implementations of qubits exist to employ quantum computational advantages, some of them are superconducting qubits, ion-trap, quantum dots. Out of all of this trapped ion technology has a good amount of potential, although superconducting qubits are the most common one. Basically ion is trapped in an energy function saddle point to harness the qubit property from the ion. An introduction of this promising technology will be discussed and shared its advantages over superconducting properties. Some meticulous procedures are followed to make quantum gates and at the end of the talk, we will discuss its scaling techniques and future potentials.",
"The world of videogames is mainly based on reaching a goal using to your advantage the effects that were determined by games designers for each of the actions that the player can perform through an interface. Let's give an example, the game of the chrome’s dinosaur has as its main goal to avoid the obstacles and get all the possible points, the actions of the player are to press the spacebar and the effect on the dinosaur of that action is jump. On the other hand, quantum computing has different applications, including the use of quantum properties in video games, one of the main characteristics that we can find is the use of qubits, information units and the analog of bits in classical computing. Qubits can be manipulated using quantum gates, which in turn can be arranged into quantum circuits. Putting these two ideas together, we decided to create a new video game in which the effects do not depend totally on the player actions or video game designer. Taking up the example of the classical chrome’s dinosaur, we developed a game in which the user has control over a set of quantum gates and their position in a quantum circuit, then based on a framework that can simulate quantum circuits such as Qiskit of IBM, we get the results which determine whether the dinosaur jumps or ducks. We hope you enjoy and learn a lot with this game.",
"Understanding qubits through math only goes so far...sometimes you just need to look at them with your eyeballs. In this session I'll talk about some inspiring approaches to making qubits visual and interactive, my decisions and lessons learned while creating a gamified quantum circuit editor for beginners (elliot.website/qubit), and some of my ideas for how qubits could be visualized in the future.",
"Quantum circuits feel less intuitive than classical circuits. I'm developing QC Simplify (qcsimplify.com) with the goal of helping people new to quantum computing gain a better intuition for how the order of quantum gates changes the behaviour of a quantum circuit. It uses a simple drag-and-drop interface, where you can drag gates across each other to automatically apply a commutation rule that keeps the circuit’s behaviour the same. When you place a new gate by letting go of it on the circuit, it will cancel with adjacent gates (when possible) to simplify the circuit. I will give a demo of the current capabilities of the website and propose some possible future directions, and will gladly listen to any ideas you bring for improvements!",
"Quantumcat is a cross-platform library and is built on the principle of write once and execute on any quantum provider. Developers just have to follow one syntax and could execute their circuit in one of the supported platforms such as Google Cirq, IBM Qiskit, IonQ, and Rigetti (Few others are in progress) without the need to write code in multiple syntaxes. More info on: https://quantumcat.io/",
"In NISQ era, quantum computers are not perfect and errors prevent them from being useful. Among the sources of errors, gate errors are significant. To reduce these errors an active error mitigation can be used. By amplifying the errors and then extrapolating, those to zero errors will increase the performance of NISQ devices. In my talk, I would like to give an introduction to what are sources of errors and to the method of error mitigation with Richardson extrapolation.",
"Several natural phenomena are described by differential equations - which are also used to model quantum systems. Simulating those systems in a quantum computer implies solving a particular set of linear differential equations (LDEs) using quantum algorithms. We use the same techniques to solve a broader set of LDEs, by representing their solutions via Taylor Series and decoding them into qubits. We use Yao Quantum (an efficient open-source framework for quantum algorithm design), written in Julia, to perform simulations with a 10 relative error.",
"An exciting playground for exploring quantum dynamics in the nano-scale is a 2D honeycomb system. With the evolution of nano-electronics and continued miniaturization of devices, it became evident that 2D materials would not only empower us to engineer novel devices, but also aid understanding the rich physics involved. It is no myth that all major breakthroughs in condensed matter physics have some sort of motivation drawn from hexagonal lattices. Graphene, among many others, is one such awesome 2D material, which could be cleverly ‘quantum-engineered’ to design robust ‘topological quantum devices’ or maybe applications in spintronics or in the whole new field of ‘valleytronics’. From an enormous rise in computational power to significant decrease in power consumption, the possibilities are endless. In this talk, I share some of my ‘quantum thoughts’ to introduce the fascinating world of honeycomb systems.",
"Addressing data movement bottlenecks in HPC and other applications is important to improve storage and I/O performance. Data compression (lossy or lossless) helps in reducing the number of bytes that must be transmitted or stored. Caching is another method that helps in reducing data movement by keeping data required for computation in fast memory. Previously, it has been explored that hardware compression can be used to expand size of hardware caches and main memory or caching at the software level. Softwares caches further improve the I/O performance for distributed applications and cache the input data for parallel tasks. One of the main applications of compression and caching in quantum computing is in reducing the memory footprint for quantum circuit simulations. In quantum computing research, using classical HPC systems to simulate quantum computers is integral for understanding behavior of quantum computing systems. These simulations allow developers to evaluate complexity of new quantum algorithms and validate the design of quantum devices. Therefore, through this research we aim to build a cache simulator which can be used to assess the performance of different compressors as they cache for compressed blocks of various HPC applications or quantum simulations. This simulator can then be used to run different benchmarks (quantum approximate optimization algorithm (QAOA), Quantum Fourier Transform (QFT), Grover’s Search Algorithm) and then choose the compressor based on its cache performance.",
"Researchers and Scientists have always hunted for analogies to explain complex physical phenomenas. Games have always been a way to explain our understanding. Quantum Coins combines both, we implement a circuit which returns a which returns the initial quantum state. Quantum Coins is a coin game which is intended to show some of the most fundamental properties of Quantum Mechanics. The game exploits superposition and uncertainty to show that quantum systems have an edge over classical computers when we talk about usability. The game is inspired from a reference in a TED Talk here (https://www.youtube.com/watch?v=QuR96...). A coin is initially placed in Heads position, there are a total of 3 moves, classically the game is all about random events. The computer and the player have an equal probability of winning. On a quantum computer the circuit is fashioned in such a way that the output is the ket 0 state with measurement probability equal to 100%. Hence by using some simple gates we display some of the most fundamental properties of Quantum Computers.",
"I will talk three qiskit projects, and these have a same thing which are using cloud. (1) Quantum Ugly Duckling: making a discord bot with NQRNG. For this project, I used IBM Cloud server and database to sabe quantum dad jokes. (2) Qoupang: quantum blockchain service for logistics. Our team used a cloud server and QRNG for making a hash value of each block. (3) Qiskit Textbook Master: a quiz app for learning qiskit textbook. Using a web-hosting service in Github, give a bundle of quizzes to help learning. Main focus will be You can make these quantum projects easily!"]; 
	
	
var author_sunday = [
"Victor Onofre and F. Rojas",
"AJMAL IBN MOHAMMED ALTHAF",
"Claudia Zendejas-Morales",
"Emilio Peláez and Minh Pham",
"Joonho Kim",
"Pinaki Sen",
"Rana Prathap Simh Mukthavaram",
"Zeki Seskir",
"Lia Yeh",
"John van de Wetering"];
 
var affiliation_sunday = [
"Center of Nanoscience and Nanotechnology (CNyN)",
"MSc Physics student, Q Enthusiasts Kerala",
"Teacher Assistant at UNAM and Intern at Quantum Flytrap",
"Research Intern at Weizmann Institute of Science & Undergraduate mathematics student at the University of Chicago.",
"Institute for Advanced Study",
"Engineering Undergrad at NIT Agartala, INDIA and Research Intern at ISI Kolkata, INDIA",
"Qiskit Advocate, Mathematics and Computing at IIT Kharagpur, AI Architect at MapRecruit.ai",
"Board member at QWorld and Research Assistant at METU Physics Department",
"PhD student, Quantum Group, University of Oxford",
"Oxford University"]

	
var title_sunday = [
"Discord-type quantum correlations in the radical pair mechanism for magnetoreception in birds",
"Digital Divide in Quantum Education",
"Incorporating the advantages of ZX-calculus in the Tequila platform",
"On the recursive construction of relative phased multiple controlled Toffoli",
"Quantum Energy Landscape and Variational Quantum Algorithms",
"Hierarchical Extreme Quantum Machine Learning with Tensor and Neural Networks in the NISQ Era",
"Building Retro-Style Quantum Games for Arduino from scratch",
"The Landscape of Academic Literature in Quantum Technologies",
"Quantum gates: software vs hardware implementation",
"Doing quantum computing using pictures"];
	
 var video_sunday = [
"https://www.youtube.com/embed/-PWs6JbtfUQ",
"https://www.youtube.com/embed/LehWenCTnIw",
"https://www.youtube.com/embed/lN8TxkgrdVE",
"https://www.youtube.com/embed/aqxQykylCOs",
"https://www.youtube.com/embed/decfApZo-Cg",
"https://www.youtube.com/embed/tJyAaSw3wWc",
"https://www.youtube.com/embed/vgIO6jC3US0",
"https://www.youtube.com/embed/NrKJcR_XzOQ",
"https://www.youtube.com/embed/8NpVsJb4xbY",
"https://www.youtube.com/embed/poh6cbHhvek"];
  
var abstract_sunday = [
"The leading hypothesis to explain how migratory birds can detect the direction of the Earth's magnetic field is the Radical-Pair mechanism, which is by now a well-established theoretically and experimentally mechanism. The radical pairs oscillate between singlet and triplet states. The Earth's magnetic field direction influences the probability of finding them in one state or another. The yield of these states controls the neural signals of the bird's retina, providing the basis for magnetoreception. This research studies quantum correlations in the mechanism of radical pairs, working with discord-type quantifiers. In the first stage of the work, the dependence of the angle of the Earth's magnetic field and the singlet yield was investigated, consistent with the different studies on the mechanism of radical pairs. In the second stage, discord-type quantifiers were calculated as a function of the angle of the Earth's magnetic field, finding a dependence similar to that of the singlet yield.",
"We live in a society where all the classes have gone from offline mode to online mode all of a sudden in a year. The digital divide, as we know is the inaccessibility to technology and gadgets. Nowadays education is just a privilege only for those who have access to technology. The same issue is there in the domain of quantum education. Quantum computing is relatively a new field and because of this, not everyone has prior exposure to it. To bridge the issue there are a lot of quantum education initiatives and many of them are free. The question is does everyone have access to quantum education in online mode. In Kerala, which is my state there is smartphone access is there for 90% of the students, but for quantum education, the smartphone is not enough. We need computer access for using quantum computing platforms or for coding. There are only 10-20 % of students who use computers for their education and this makes a huge gap in accessing the quantum world. My talk focuses on representing the issues in the first part. The second part address some of the possible solution in reducing the digital divide and how to be more inclusive in the quantum world. The solution discussed is regarding how learning materials can be made available offline, how local science communities and volunteers from quantum universal education can help in teaching quantum computing.",
"Tequila's main goal is to simplify and accelerate the implementation of new ideas for quantum algorithms, allowing algorithms to be prototyped and subsequently transforming the resulting circuits and executing them in quantum simulators or interfaces. In order to execute optimized circuits, we sought to take advantage of the benefits of ZX-calculus, incorporating the functionality of converting Tequila circuits to PyZX circuits and vice versa, through OpenQASM code, an intermediate representation for quantum instructions. With this extension to the Tequila platform, the optimization of circuits is achieved by reducing the T-count, the number of non-Clifford quantum gates, by up to 28%.",
"We propose an efficient construction for multiple controlled-NOT gates that allows for relative phase difference in the output of the gate and uses no additional qubits other than n control qubits and one target qubit. We employ a recursive construction using three base cases: the phaseless CNOT, the phased Toffoli, and the phased triple controlled-NOT; the latter two are known constructions from previous literature on the subject. To prove its correctness, we use the method of exhaustion, checking all different gate and parameter combinations. Finally, we derive an upper bound on the complexity of our technique and compare it to the recently known construction of complexity 9n + O(1) CNOT gates.",
"Variational Quantum Algorithm (VQA) is a major application of the near-term hybrid computing model that jointly uses a classical computer to handle continuous variables and a quantum computer to generate variational wavefunctions controlled by those variables. Many computing problems are formulated as optimization problems in this framework to find out the global minimum in the quantum energy landscape. In this talk, I will explain two main design factors for efficient VQA optimization, i.e., the entangling capability and number of control parameters of the variational wavefunction, by analyzing how they influence the geometric shape of the quantum energy landscape.",
"Recently, the closeness between the techniques used in classical machine learning and quantum-many body physics has got significant attention among the academic and research communities. Especially, the deep learning frameworks and tensor networks hold similar properties such that they can be used for machine learning tasks. In noisy intermediate-scale quantum (NISQ) technology, the quantum circuits with a long circuit depth or a large number of qubits cannot be implemented on NISQ devices. It is highly demanding to develop applications with adequate resources which can exploit the quantum advantages. In this paper, we proposed the architecture of hierarchal extreme quantum machine learning consisting of quantum tensor variants of autoencoder (i.e. Tree tensor network (TTN), multi-scale entanglement renormalization ansatz (MERA)) and quantum neural network (QNN) for binary classification. The proposed hierarchical architecture has the ability to overcome the shortcomings of regular tensor networks and can be defined in complex geometries efficiently as long as the order can be represented appropriately. We apply the quantum variants of TTN and MERA for image compression and quantum neural networks to classifying the images and compare their performance, concluding that the combination of TTN performs better than MERA with QNN for image classification.",
"Building retro quantum games in general is a task that’s super fun and in my opinion one of the best ways to cement your basic quantum computing concepts. However, Quantum games today are usually built for relatively powerful microprocessors such as a Raspberry pi or for a computer. These chips tend to be relatively expensive and honestly just aren’t fun to build retro games on - as you already have libraries like Pygame to help you along the process. The aim of this project was to build a retro handheld using an Arduino and program a game based on quantum computing onto it.  During this talk I’ll be sharing the process of how I built the quantum game, provide the code and circuit schematics so you can play and build on it yourself!",
"In this study, we investigated the academic literature on quantum technologies (QT) using bibliometric tools. We used a set of 49,823 articles obtained from the Web of Science (WoS) database using a search query constructed through expert opinion. Analysis of this revealed that QT is deeply rooted in physics, and the majority of the articles are published in physics journals. Keyword analysis revealed that the literature could be clustered into three distinct sets, which are (i) quantum communication/cryptography, (ii) quantum computation, and (iii) physical realizations of quantum systems. We performed a burst analysis that showed the emergence and fading away of certain key concepts in the literature. This is followed by co-citation analysis on the “highly cited” articles provided by the WoS, using these we devised a set of core corpus of 34 publications. Comparing the most highly cited articles in this set with respect to the initial set we found that there is a clear difference in most cited subjects. Finally, we performed co-citation analyses on country and organization levels to find the central nodes in the literature. Overall, the analyses of the datasets allowed us to cluster the literature into three distinct sets, construct the core corpus of the academic literature in QT, and to identify the key players on country and organization levels, thus offering insight into the current state of the field.",
"Unlike for classical computers, for quantum computers, present-day quantum assembly languages do not correspond to physical hardware operations. Although gate-based quantum computers which implement a universal gateset can run any qubit operations, for the implementation to be efficient, the desired gate needs to be decomposed into gates the hardware can run. This talk is a primer on quantum computer architecture, specifically how quantum software is compiled to quantum assembly language and then to quantum hardware.",
"Quantum mechanics is famously counter-intuitive, so we should grasp at anything that allows us to understand it in a more intuitive manner. As we are visual creatures, why not let our visual cortex do some work and represent computations using pictures instead of formulae or matrices! The ZX-calculus is a graphical language for reasoning about quantum computation. The usefulness of ZX comes from our ability to transform and simplify ZX-diagrams completely graphically. In this talk I will briefly introduce ZX, and demonstrate using our software library PyZX how we can simplify quantum computations and how to verify a circuit is exactly doing what it says on the tin."]; 
  
//////////// saturday ///////////////////////////
	
var data = [];
var length = author_saturday.length; // user defined length

for(var i = 0; i < length; i++) {
    data.push(i);
}

data.sort(() => Math.random() - 0.5);
  
  
var first = Math.floor(Math.random() * author_saturday.length);
var html_str = "";
var i;
for (i = 0; i < title_saturday.length; i++) {
  var idx = (first + i) % title_saturday.length; 
  html_str += "<div class=\"view_item\" style=\"width: 65vw;\"> <div class=\"vi_left\" style=\"width:30%;\" > <iframe width=\"180\" height=\"135\" src="+ video_saturday[data[idx]] +"></iframe>  </div> <div class=\"vi_right\" style=\"width:68%;\" > <p class=\"title\"> "+title_saturday[data[idx]] + "</p> <div class=\"title\">"+ author_saturday[data[idx]] +" "+ affiliation_staturday[data[idx]] +"</div> <p class=\"content\">"+ abstract_saturday[data[idx]]+ "</p></div></div>\n";
                          
}
document.getElementById("video_anniversary_saturday").innerHTML = html_str;
	
//////////// sunday///////////////				      
				      
				      
var data = [];
var length = author_sunday.length; // user defined length

for(var i = 0; i < length; i++) {
    data.push(i);
}

data.sort(() => Math.random() - 0.5);
  
  
var first = Math.floor(Math.random() * 10);
var html_str_s = "";
var i;
for (i = 0; i < title_sunday.length; i++) {
  var idx = (first + i) % title_sunday.length; 
  html_str_s += "<div class=\"view_item\" style=\"width: 65vw;\"> <div class=\"vi_left\" style=\"width:30%;\" > <iframe width=\"180\" height=\"135\" src="+ video_sunday[data[idx]] +"></iframe>  </div> <div class=\"vi_right\" style=\"width:68%;\" > <p class=\"title\"> "+title_sunday[data[idx]] + "</p> <div class=\"title\">"+ author_sunday[data[idx]] +" "+ affiliation_sunday[data[idx]] +"</div> <p class=\"content\">"+ abstract_sunday[data[idx]]+ "</p></div></div>\n";		      
				  
}
document.getElementById("video_anniversary_sunday").innerHTML = html_str_s;

</script>


<!-- End page content

  html_str += "<div class=\"view_item\" style=\"width: 65vw;\"> <div class=\"vi_left\" style="width:40%;\" > <iframe width=\"180\" height=\"135\" src=\"https://www.youtube.com/embed/YC88NyV5SuM\"></iframe>  </div> <div class=\"vi_right\" style=\"width:58%;\" > <p class=\"title\"> "+title[data[idx]] + "</p> <div class=\"title\">"+ author[data[idx]] + "   "  + affiliation[data[idx]] +"</div> <p class=\"content\">"+ abstract[data[idx]]+ "</p></div></div>\n;"
                          -->


