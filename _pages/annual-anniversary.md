---
permalink: /annual-anniversary/
layout: archive
---

<link href="/assets/css/areas.css" rel="stylesheet" type="text/css">
<link rel="shortcut icon" type="image/png"  href="/assets/images/FSQC-small.png" />
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
</style>
<!-- Header -->

<header class="w3-display-container w3-content w3-wide" id="home">

<div class="w3-container w3-padding-32" id="projects" style="width: 55vw;">
    <h2 class="w3-border-bottom w3-border-light-grey w3-padding-16">Annual Anniversary</h2>
    <h4>This event is to celebrate our first anniversary in sharing the knowledge of quantum computing and for our community to share ideas, thoughts and their knowledge throughout this year.</h4>	
	</div>
	
<div class="w3-container w3-padding-32" id="projects" style="width: 55vw;">
    <h2 class="w3-border-bottom w3-border-light-grey w3-padding-16">TimeLine</h2>	
<div class="timeline">
  <div class="container left">
    <div class="content">
    <h2 style="color:#FFFFFF">Open enrollment</h2>
<p style="color:#FFFFFF">June 14, 2021</p>
  </div>
  </div>
  <div class="container right">
    <div class="content">
    <h2 style="color:#FFFFFF">Close enrollment</h2>
	  <p style="color:#FFFFFF">July 9, 2021</p>
  </div>
  </div>
  <div class="container left">
    <div class="content">  
    <h2 style="color:#FFFFFF">Abstracts accepted from</h2>
	  <p style="color:#FFFFFF">July 16th, 2021</p>
  </div>
  </div>
  <div class="container right">
    <div class="content">  
  <h2 style="color:#FFFFFF">Event Days</h2>
	<p style="color:#FFFFFF">July 24th and 25th, 2021</p>
    </div>
  </div>
</div>	
	
	

	
  </div>

<div class="w3-container w3-padding-32" style="width: 55vw;">	
	<h2 class="w3-border-bottom w3-border-light-grey w3-padding-16">Topics</h2>
  <ul>
	  <li>Quantum Learning Resources</li>
	  <li>Quantum Hardware</li>
	  <li>Quantum Software</li>
	  <li>Quantum Algorithms</li>
	  <li>Quantum Computer Architecture</li>
	  <li>Quantum Error Correction</li>
	  <li>Quantum Chemistry</li>
	  <li>Quantum Sensing</li>
	  <li>Quantum Cryptography</li>
	  <li>Quantum Communication</li>
	  <li>Quantum Information Theory</li>
	  <li>Quantum Machine Learning</li>
	  <li>Quantum Games</li>
	  <li>Miscellaneous</li>
  </ul>
</div>
<br> <br>	
<div style="width: 55vw">
	    <h4>Time to celebrate and listen to everyone's quantum computing progress.</h4>
	<img src="/assets/images/event.png" style="background-color: white;box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);display: block;  margin-left: auto;  margin-right: auto;  width: 50%;">
</div>
<br> <br>

<div class="w3-container w3-padding-32" style="width: 55vw" >		
<h4></h4>
</div>

	
	


</header>


<div class="w3-container w3-padding-32" style="width: 40vw" >		

<button class="button qurator"  onclick="document.location='https://quantumuniversaled.typeform.com/to/TYDeLwCr'">Register</button>

	
</div>
<!-- End page content -->

