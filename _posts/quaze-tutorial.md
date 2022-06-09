---
title: "Tutorial to build a Quantum inspired puzzle game in JS"
categories:
  - Blog
tags:
  - tutorials
  - JS
  - HTML
  - CSS
  - games
  - Quaze
  - Quantum game
author:
 - Vardaan Sahgal
---

*Two physics geeks entered a Quantum Games hackathon with very minimal knowledge of Quantum Computing, met a CS Wiz, and the three embarked on a journey to create their first puzzle game inspired by quantum computing. This is exactly how 'Quaze' was developed during the [QAIF Quantum Games Hackathon 2021](https://www.qaif.org/contests/quantum-games-hackathon).* 

The source code of the game can be found at [Qorsairs - GitHub Repo](https://github.com/Qorsairs/Quaze) and the ready-to-play version of the game can be easily accessed over any browser at https://qorsairs.github.io/Quaze/. 

Quaze was developed by the 'Qorsairs Team':
1. Diego A. Quinones
2. Vardaan Sahgal
3. Vatsal Kanoria 

## Introduction:  
### Quaze
Quaze - the quantum maze! This is a puzzle game inspired by quantum computing, following rules like those used for the transformation of qubits, the basic units of information for a quantum computer. Our motivation while developing this game was to create a simple browser-based learning game which was easily accessible to all. The game acts as an educational resource to teach the basics of qubit rotations and transformations to early-stage Quantum Computing learners. 

### Gameplay
At a first glance, the game looks like just another maze puzzle, where the goal is to reach the end of a Maze by finding the correct path. However, on a closer look, reaching the end of the maze is not the only goal of the game. There is a quantum twist. The qubit at the start must also be rotated while moving through the maze to obtain a qubit target state, as indicated at the end of the maze. 

### Controls
Use the arrow keys ↑, ↓, ← & → to move the qubit around the maze. 
When the qubit moves into a quantum gate (a coloured tile within the maze), it changes its state. 
Different colours represent different quantum gates: red is the X gate, blue is the Z gate & green is the H (Hadamard) gate. 
Each gate transforms the qubit differently:
* X flips the qubit vertically. 
* Z flips the qubit horizontally.
* H rotates the qubit back and forth between horizontal and vertical.
Note: A rotation of a state around a symmetrical axis will leave the state the same.

If you reach the end of the maze and the state is not the target, keep going. You can move backwards and try a different route.

A more visual explanation of the game controls can be found in the [Quaze Tutorial](https://qorsairs.github.io/Quaze/tutorial.html).

## Getting started:
The game is developed using JS, HTML and CSS and hence, some basic knowledge in these languages is a prerequisite for the following tutorial. Although it is a quantum computing inspired game, quantum computing is not directly used in game development and so, knowledge is quantum computing is encouraged but not at all necessary for the tutorial!
[Figma](https://www.figma.com/) is used in this tutorial for designing the various graphic elements used in the game, but any other graphic designing software may work as well. This tutorial will avoid instructions to create the graphic art required for the game, but for simplicity and convenience, all the graphics used in this tutorial can be directly downloaded from [here](https://github.com/Qorsairs/Quaze/tree/main/assets). All the code files in this tutorial can be executed on any of the commonly used Code editors such as [VS Code](https://code.visualstudio.com/).

### Step 1 : Implementing the game logic in JS
The first and the most important step in this tutorial is to implement the gameplay logic in JS. To do this, create a `quaze.js` file and run the following code in it. To make the game development UI easy to code in JS, the help of external libraries such as [Phaser library](https://phaser.io/) is taken. It should be noted that all calculations of the position of various game objects must be done using pixels while using Phaser, and this might be comfortable in the long run since Figma (used for graphic designing) also has pixel counts.
Physics APIs are imported from Phaser to allow the easy movement of qubits across the maze. The layout of the maze is designed by constructing a basic grid of gate images with phaser. Using a similar implementation of the physics function from Phaser, the walls of the maze have been set to be "solid", which restricts the movement of the qubit only within the specified boundaries. If the graphics are being designed from scratch, care should be taken that the dimensions of the qubit asset should be sufficiently smaller than the dimension of the gap between the maze walls. This is done to ensure easy movement of the qubit across the maze.
Now, each gate image must be associated with its corresponding function of rotating the qubit image. This is done by writing specific functions to rotate the qubit image when it overlaps any gate image. Since the initial state of the qubit image can be variable, it is essential to account for each possible initial qubit state and associate the gate rotations accordingly. Since Quaze is a 2D game, the 4 possible orientations of the qubit are initialised as `0 = up, 1 = right, 2 = down, 3 = left` and the various rotations of the gates are trivially reduced to angular rotations of the qubit image as `0: 0 degree, 1: 90 degree, 2: 180 degree, 3: -90 degree `
Finally, conditional statements are added to the code to identify if the final state of the qubit obtained by the player at the end of the maze is the same as the one specified in the puzzle. If the desired state is obtained, the game ends and the player is declared a winner.

```javascript
let config = {
  type: Phaser.AUTO,
  width: 800,
  height: 650,
  backgroundColor: '#FFFFFF',
  scene: {
      preload: preload,
      create: create,
      update: update
  },
  physics: {
    default: 'arcade',
    arcade: {
        debug: false
    }
},
};

let game = new Phaser.Game(config);
let qubit;
let walls;
let hgates;
let xgates;
let zgates;
let gameOver = false;

function preload ()
{
  this.load.image('xgate', 'assets/xgate.png');
  this.load.image('zgate', 'assets/zgate.png');
  this.load.image('hgate', 'assets/hgate.png');
  this.load.image('wallh', 'assets/wallh.png');
  this.load.image('wallv', 'assets/wallv.png');
  this.load.image('qbitup', 'assets/qbitup.png');
  this.load.image('solutionleft', 'assets/solutionleft.png');
  this.load.image('goal', 'assets/goal.png');
}

let baseXCoordinate = 180;
let xSpacing = 100; //will be image width of a gate (i.e. grid column)
let baseYCoordinate = 110; 
let ySpacing = 100; //will be image height of a gate (i.e. grid row)
function xCoordinateGrid(columnNumber){ 
  return baseXCoordinate + xSpacing * columnNumber
}
function yCoordianteGrid(rowNumber){ 
  return baseYCoordinate + ySpacing * rowNumber
}

const h = 'hgate'
const x = 'xgate'
const z = 'zgate'
const T = true
const F = false
const gameData = {
  gridSize: {
    rows: 5,
    columns: 5
  }, //the grid is 5x5
  gatesGrid: [[h, z, h, z, x], [x, h, z, x, h], [z, x, h, z, x], [h, x, x, h, z], [x, h, z, h, h]], //each subarray represents a row starting from the top of the grid
  horizontalWalls: [[T, T, T, T, T], [F, T, F, T, F], [F, F, T, T, F], [F, F, F, F, F], [F, F, T, T, T], [T, T, T, T, T]], //each subarray represents a row starting from the top of the grid
  verticalWalls: [[F, T, T, T, T], [F, T, T, T, T], [F, F, F, T, F], [F, F, F, F, F], [F, F, T, T, F], [T, T, T, T, F]], //each subarray represents a column starting from the left of the grid
  qubitInitialState: 0, //facing up
  qubitFinalState: 3, //facing left
}
let qubitState = gameData.qubitInitialState; //initial state of qubit is facing up. (0 = up, 1 = right, 2 = down, 3 = left)

function create ()
{
  hgates = this.physics.add.staticGroup();
  xgates = this.physics.add.staticGroup();
  zgates = this.physics.add.staticGroup();
  for(let row=0; row<gameData.gridSize.rows; row++){
    for(let column=0; column<gameData.gridSize.columns; column++){
      let gate = gameData.gatesGrid[row][column];
      if(gate==='hgate'){
        hgates.create(xCoordinateGrid(row), yCoordianteGrid(column), gate)
      }
      if(gate==='xgate'){
        xgates.create(xCoordinateGrid(row), yCoordianteGrid(column), gate)
      }
      if(gate==='zgate'){
        zgates.create(xCoordinateGrid(row), yCoordianteGrid(column), gate)
      }
    }
  }

  walls = this.physics.add.staticGroup(); //group of static objects

  for(let row=0; row<gameData.gridSize.rows+1; row++){
    for(let column=0; column<gameData.gridSize.columns; column++){
      if(gameData.horizontalWalls[row][column]){
        walls.create(xCoordinateGrid(column), yCoordianteGrid(row)-50, 'wallh'); //TODO: remove magic value '50' by changing asset?
      }
      if(gameData.verticalWalls[row][column]){
        walls.create(xCoordinateGrid(row)-50, yCoordianteGrid(column), 'wallv'); //TODO: remove magic value '50' by changing asset?
      }
    }
  }

  let goal = this.physics.add.image(xCoordinateGrid(4.5), yCoordianteGrid(4), 'goal');
  this.add.image(xCoordinateGrid(5)+10, yCoordianteGrid(4), 'solutionleft').setScale(0.7);
  
  qubit = this.physics.add.image(xCoordinateGrid(-1), yCoordianteGrid(0), 'qbitup').setScale(0.7);
  qubit.setCollideWorldBounds(true); //qubit cannot run off the edge of the game screen
  
  let startText = this.add.text(xCoordinateGrid(-1)-25, yCoordianteGrid(-1)+30, 'Start', { fontSize: '16px', fill: '#000' }); 

  this.physics.add.collider(qubit, walls); 

  let qubitAngles = {
    0: 0, //up
    1: 90, //right
    2: 180, //down
    3: -90 //left
  }
  function hTransform(qubit, gate){
    gate.disableBody(true, true); //TODO: figure out way to enable re-enable the body when the qubit is no longer overlapping a specific gate!
    if (qubitState===0) {
      qubitState = 1
      qubit.angle = qubitAngles[qubitState];
    }else if (qubitState===1) {
      qubitState = 0
      qubit.angle = qubitAngles[qubitState];
    }else if (qubitState===2) {
      qubitState = 3
      qubit.angle = qubitAngles[qubitState];
    }else if (qubitState===3) {
      qubitState = 2
      qubit.angle = qubitAngles[qubitState];
    }

  }
  function xTransform(qubit, gate){
    gate.disableBody(true, true);
    if(qubitState===0){
      qubitState = 2
      qubit.angle = qubitAngles[qubitState];
	  }else if(qubitState===2){
      qubitState = 0
      qubit.angle = qubitAngles[qubitState];
    }
  }
  function zTransform(qubit, gate){
    gate.disableBody(true, true);
    if(qubitState===1){
      qubitState = 3
      qubit.angle = qubitAngles[qubitState];
    }else if(qubitState===3){
      qubitState = 1
      qubit.angle = qubitAngles[qubitState];
    }
  }
  function winOrLose(qubit, goal){
    let gameEndText = this.add.text(xCoordinateGrid(5)-45, yCoordianteGrid(5)-30, '', { fontSize: '32px', fill: '#000' }); 
    if(qubitState===gameData.qubitFinalState){
      gameEndText.setText('You Win'); 
    }else{
      gameEndText.setText('You Lose'); 
    }
    setTimeout(()=>{
      gameOver = true
    }, 250)
  }

  this.physics.add.overlap(qubit, hgates, hTransform, null, this); 
  this.physics.add.overlap(qubit, xgates, xTransform, null, this); 
  this.physics.add.overlap(qubit, zgates, zTransform, null, this); 
  this.physics.add.overlap(qubit, goal, winOrLose, null, this); 

  cursors = this.input.keyboard.createCursorKeys(); 
}

function update ()
{
  if(gameOver) return;

  if(cursors.left.isDown){
    qubit.setVelocityX(-100);
  }else if(cursors.right.isDown){
    qubit.setVelocityX(100);
  }else if(cursors.down.isDown){
    qubit.setVelocityY(100);
  }else if(cursors.up.isDown){
    qubit.setVelocityY(-100);
  }else{
    qubit.setVelocityX(0);
    qubit.setVelocityY(0);
  }
}
```
### Step 2 : Designing the CSS framework for the webpage
Now that the main part of the gameplay implementation in JS is completed, the next steps only cover some cosmetic code to embed the game in a user-friendly webpage.
The CSS file is used to define the various style elements of the webpage. The various HTML tags for which the style properties have been defined below might not be clear right now, but all the HTML tags have been defined in the next step (Step 3) of this tutorial. For simplicity the entire CSS is divided into 2 parts:

`style.css` file is created to design the basic layout of all the webpages. All the variables can be played around with to design the most aesthetically pleasing webpage.

```css
body {
    font-family: sans-serif;
    background-color: white;
}

.content{
    margin: 1rem 0 1rem 1rem ;
    display: grid;
    gap: 1rem;
    z-index: 1;
}

.hero {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: white;
    background-image: linear-gradient(rgba(0, 0, 0, 0.5),rgba(0, 0, 0, 0.5)), url('https://cdn.pixabay.com/photo/2017/01/31/15/35/ball-2025141_1280.png');
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

.hero h1 {
    font-size: 5em;
    margin-top: 0;
    margin-bottom: 0.5em;
    color:rgba(10, 247, 10, 0.76)
}

.hero .btn {
    display: block;
    width: 200px;
    padding: 1em;
    margin-top: 50px;
    margin-left: auto;
    margin-right: auto;
    color: white;
    text-decoration: none;
    font-size: 1.5em;
    border: 3px solid white;
    border-radius: 20px;
    background-color: rgba(10, 247, 10, 0.76);
}

.tutorial_image {
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
    max-width: 90vw;
    width: 50vw;
    border: 5px solid rgba(10, 247, 10, 0.76);
}
```

`nav.css` file is created to design the navbar of the webpage. Again, all the variables can be played around with to design the most aesthetically pleasing navbar for the webpages.

```css
body {
  margin: 4rem 0 0 0rem;
}

nav {
  overflow: hidden;
  background-color: black;
  position: fixed; 
  top: 0; 
  width: 100%; 
  z-index: 2;
}

nav a {
  float: left;
  display: block;
  color: white;
  text-align: center;
  padding: 1rem 1rem;
  text-decoration: none;
}

nav a:hover {
  background: rgba(10, 247, 10, 0.76);
  color: black;
}

nav .current {
  background: rgba(10, 247, 10, 0.76);
  color: black;
}
```

### Step 3 : Combining the CSS & JS files into a common HTML webpage

`quaze.html` file is created to embed and display the Quaze game. It is important that all the required CSS & JS code files prepared before are correctly attached within the HTML webpage to ensure proper formatting and embedding of the game onto the webpage.
The navbar element is also included in the webpage to allow easy navigation between the various webpages.

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Quaze</title>
    <script src="https://cdn.jsdelivr.net/npm/phaser@3.11.0/dist/phaser.js"></script>
    <script src="quaze.js" type="text/javascript"></script>
    <link rel="stylesheet" href="globals.css">
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="nav.css">
</head>
<body>
    <nav>
        <a href="index.html">Home</a>
        <a href="tutorial.html">Tutorial</a>
        <a href="quaze.html" class="current">Play</a> 
    </nav>
    <div class="content">
        <p>
            Use the arrow keys to move the qubit around and cross
            the finish line with its head on the right way round!
        </p>
    </div>
</body>
</html>
```

`tutorial.html` file is created to document the tutorial required for playing the game. All the required CSS code files prepared before must be correctly attached to the HTML webpage to ensure proper formatting. Along with all the controls of the game, a basic introduction to the quantum computing principles such as rotation and translation of qubits is also included in the tutorial. In this tutorial, simply pre-designed images have been inserted onto the tutorial page for defining the instructions. To elaborate the instructions in a more detailed manner, the same can be expanded in a text format as well.
Again, the navbar element is also included in the webpage to allow easy navigation between the various web pages.

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Quaze</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="globals.css">
    <link rel="stylesheet" href="nav.css">
</head>
<body>
    <nav>
        <a href="index.html">Home</a>
        <a href="tutorial.html" class="current">Tutorial</a>
        <a href="quaze.html">Play</a> 
    </nav> 
    <div class="content">
        <div class="tutorial">
            <img class="tutorial_image" src="assets\tutorial1.png" alt="tutorial1"/>
            <br>
            <img class="tutorial_image" src="assets\tutorial2.png" alt="tutorial2"/>
            <br>
            <img class="tutorial_image" src="assets\tutorial3.png" alt="tutorial3"/>
            <br>
            <img class="tutorial_image" src="assets\tutorial4.png" alt="tutorial4"/>
            <br>
            <img class="tutorial_image" src="assets\tutorial5.png" alt="tutorial5"/>
            <br>
            <img class="tutorial_image" src="assets\tutorial6.png" alt="tutorial6"/>
        </div>
    </div>
</body>
</html>
```

`index.html` file functions as the homepage which links the tutorial (`tutorial.html`) and the game (`quaze.html`) together in a user-friendly format.

```html
<!DOCTYPE html>
<html>
    <head>
        <title>Quaze</title>
        <link rel="stylesheet" href="globals.css">
        <link rel="stylesheet" href="style.css">
    </head>

    <body>
        <section class="hero">
            <div class="hero-inner">
                <h1>Quaze</h1>
                <h2>A quantum maze phase game</h2>
                <a href="tutorial.html" class="btn">Tutorial</a>
                <a href="quaze.html" class="btn">Play!</a>
            </div>
        </section>
    </body>
</html>
```

## Challenges faced and Ideas for Future work
* Since the HTML canvas forming the maze grid is formatted in specific pixels, the game is not screen responsive. Currently, the user needs to zoom in/out the browser window to view the game correctly. For anyone interested in diving deep into the intricacies of HTML, making the game screen responsive might be a good place to start.
* In the JS game logic, we had a hard time getting the Phaser to fire the overlap event only once when the qubit begins the overlap with a gate. Although a solution for this has been already implemented, there is still some scope for improvement in the working of the game logic.
* There are points in the maze where the qubit may overlap with multiple gates at once, so both the overlapping events fire at the same time, which we don't want! To resolve this, we have implemented the concept of vanishing the gates as soon as the qubit touches them. Although there is no fault here, it would be interesting to see a game where the gates are present even after the qubit overlaps it. This could potentially trigger new level ideas to the game where gates could be multiple times to attain the desired qubit state.
* Finally, it would be really awesome to see more Quaze puzzle ideas for new levels in the game :)

## Conclusions  
Only the important parts of the code are explained here, but the entire Source code can be viewed at [Qorsairs - GitHub Repo](https://github.com/Qorsairs/Quaze). As you've seen, making a quantum game is quite simple and in fact, can be developed even with absolutely no knowledge of quantum computing. All you need is a good game idea, some basic programming skills, and the will to make your idea come to life. 
