---
permalink: /anniversary/
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
<h2 style="color:#A70024;">if u missed registration, u can still join via our <a href="https://discord.gg/NDm9e9W">Discord server announcements </a> </h2>
<!--button class="button qurator"  onclick="document.location='https://quantumuniversaled.typeform.com/to/hG70hI38'">Sign up to give a talk</button>
<button class="button qurator"  onclick="document.location='https://quantumuniversaled.typeform.com/to/OoTHmxDx'">Register for the event</button-->
<button class="button qurator"  onclick="document.location='https://fullstackquantumcomputation.tech/schedule_anniversary/'">Accepted abstracts </button>

	
</div>	
<div class="w3-container w3-padding-32" style="width: 55vw" >		
<div class="w3-container w3-padding-32" style="width: 55vw" >		
<h4></h4>
</div>	
<div class="w3-container w3-padding-32" id="projects" style="width: 55vw;">
    <h2 class="w3-border-bottom w3-border-light-grey w3-padding-16">Timeline</h2>
	<h4 style="text-align:center">Deadlines below are Anytime-on-Earth (AoE)</h4>	
<div class="timeline">
  <div class="container left">
    <div class="content">
	<h3 style="color:#FFFFFF; text-align:left; margin-bottom:0px">How to Write an Abstract</h3>
    <h3 style="color:#FFFFFF; margin-top:0px"><a href="https://fullstackquantumcomputation.tech/blog/abstract-workshop" style="color:#FFFFFF">Workshop recording link</a></h3>
<p style="color:#FFFFFF;text-decoration: line-through;">4pm UTC, June 27th, 2021</p>
  </div>
  </div>
  <div class="container right">
    <div class="content">
    <h2 style="color:#FFFFFF; text-align:left; margin-bottom:0px">Talk abstract due</h2>
	<h3 style="color:#FFFFFF; margin-top:0px">if you'd like feedback</h3>
	  <p style="color:#FFFFFF;text-decoration: line-through;">July 9th, 2021</p>
  </div>
  </div>
  <div class="container left">
    <div class="content">  
    <h2 style="color:#FFFFFF; text-align:left; margin-bottom:0px">Talk abstract due</h2>
	<h3 style="color:#FFFFFFF; text-align:left; margin-top:0px; margin-bottom:0px">&</h3>
	<h2 style="color:#FFFFFF; text-align:left; margin-top:0px">Event registration due</h2>
	  <p style="color:#FFFFFF;text-decoration: line-through;">July 16th, 2021</p>
  </div>
  </div>
  <div class="container right">
    <div class="content">  
  <h2 style="color:#FFFFFF; text-align:left">Event Days</h2>
	<p style="color:#FFFFFF">July 24th and 25th, 2021</p>
    </div>
  </div>
</div>	

  </div>
<div class="w3-container w3-padding-32" style="width: 55vw;">	
	<h2 class="w3-border-bottom w3-border-light-grey w3-padding-16">Topics</h2>
	<div style="width:100%">
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Learning Resources</li></ul></div>
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Hardware</li></ul></div>
	</div>
	<div style="width:100%">
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Software</li></ul></div>
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Algorithms</li></ul></div>
	</div>
	<div style="width:100%">
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Computer Architecture</li></ul></div>
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Error Correction</li></ul></div>
	</div>
	<div style="width:100%">
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Chemistry</li></ul></div>
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Sensing</li></ul></div>
	</div>
	<div style="width:100%">
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Cryptography</li></ul></div>
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Communication</li></ul></div>
	</div>
	<div style="width:100%">
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Information Theory</li></ul></div>
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Machine Learning</li></ul></div>
	</div>
	<div style="width:100%">
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Quantum Games</li></ul></div>
	<div style="padding: 10px; display: inline-block;width:47%"><ul><li>Miscellaneous</li></ul></div>
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

</div>



<!-- End page content -->

