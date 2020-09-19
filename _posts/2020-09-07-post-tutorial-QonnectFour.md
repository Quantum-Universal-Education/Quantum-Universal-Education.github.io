---
title: "Qonnect four - Making a quantum game"
categories:
  - Blog
tags:
  - tutorials
  - qiskit
  - games
  - Qonnect Four
  - Quantum game
author:
 - Praveen J
 - Curate Section
 - Harshit Garg Q
---

This post will elaborate on my thought process/journey and resources used for creating the Quantum game Qonnect four with Qiskit, which also is the first ever game I’ve made. This post is written with an aim of giving a beginner perspective. By reading this, you:  
1) Get an idea of the issues faced and how I tackled them.  
2) Will know the nuances of making a quantum game in an interactive ipython notebook.  
3) Will know the code structuring, learn from my mistakes.  
4) Should be able to make your own first simple quantum game.  

The game can be found at [https://github.com/Praveen91299/QonnectFour](https://github.com/Praveen91299/QonnectFour)  

## Introduction:  
### Why make a quantum game?  
The idea to make a quantum game came to me when I saw the Quantum Dojo, Quantum pong and Quantum Intuition’s Turn the Qubit’s off. Introducing quantum principles and math into games brought much richness and randomness to the game that it made it both hard, challenging and at the same time interesting and on an academic perspective made it easy for beginners to understand Quantum Mechanics.  

Like any other paradigms, games play an important role in learning as it makes it fun.  

So with that in mind, I set to make my first Quantum Game.  


### Why Qonnect Four?
Since My first exposure to quantum games was the Quantum Dojo, I decided to make something similar with interactive ipython notebooks. My first thought was to make something like the classical mastermind, which I realised is quite the same as Quantum Dojo. So I thought about other classic board games that I’ve played and ended up with Connect four. It’s ideal since:  
1) Qubit requirements are less hence less resource intensive.  
2) Adding entangling gates could make the game very interesting and unexpected.  

Before I began, I took a look at [this amazing list](https://github.com/HuangJunye/Awesome-Quantum-Games) of some popular Quantum games made before to check if I wasn’t reinventing the wheel. Then I began.

### Gameplay  
Before starting with the code, lets look at the game flow for a game over LAN. Let `IP` denote the Player 1 IPv4 address.  

Player 1: Initiates Server by running `python3 Server.py` at a terminal instance.
Player 1: Connects to the Server script from the Jupyter notebook using the constructor  
    `game = QonnectFour(columns = 7, seed = 42, depth = 2, StartPlayer = 0, MultiPlayer = 1, host = 1, Server_IP = 'IP')`  
Player 2: Connects using  
    `game = QonnectFour(columns = 7, seed = 42, depth = 2, StartPlayer = 1, MultiPlayer = 1, host = 0, Server_IP = 'IP')`  

Now Player 1 starts by first making a move, either `game.measure()` or `game.<gate>()` and uses `game.send_move()` to send the move to the Server.  
Since the clients are not continuously asking for data from the Server, Player 2 now receives the move performed using `game.get_move()`.  
Player 2 continues similarly and the game continues still one of the person wins by obtaining four continuous coins in a row/column/diagonal.

## Getting started:  
Install the required packages using pip/conda  

Set up Qiskit by `pip install qiskit`  
Set up other required packages like matplotlib, numpy, Pillow (PIL) using `pip install <package name>`

Set up jupyter notebooks or any other interface to edit a .inpyb notebook  
`pip install notebook` for classical notebook (or)  
`pip install jupyterlab` for JupyterLab (A newer rendition of Jupyter notebooks)  

If you wish to set up a virtual environment wherein you wish to work follow instructions in [this website](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) and [this website](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/).  

I first defined my game as a class, so each time a game instance can be initiated and will retain the memory of the state of the game instead of relying on global variables. This also allows to create an independent copy of the game over which the person can try out moves, see it’s output, etc. I will explain the `__init__()` function towards the end after I’ve defined the methods.  

Along with this, I defined two classes coord() and rect() that are used to carry 2D coordinate values with a few useful methods and will be useful for rendering the output board state.  

```python
class coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def relocate(self, coords_new):
        self.x = coords_new
        self.y = coords_new
        
    def displace(self, coords_disp):
        self.x += coords_disp.x
        self.y += coords_disp.y
        
    def rescale(self, scale):
        self.x *= scale
        self.y *= scale
        
class rect(coord):
    def __init__(self, height, width, coords, colour = black, label = 'rectangle'):
        self.name = label
        self.height = height
        self.width = width
        self.x = coords.x
        self.y = coords.y
        
        #image data
        self.data = np.zeros((height, width, 3), dtype=np.uint8)
        if colour != black:
            self.recolour(self, rect(height, width, coords, black), colour)
    
    def recolour(self, location, colour):
        for a in range(location.width):
            for b in range(location.height):
                self.data[b + location.y][a + location.x] = colour
    
    def save_image(self):
        img = Image.fromarray(self.data, 'RGB')
        img.save(self.name + '.png')
        return self.name + '.png'
```
`coord()` objects contain only two values, x and y coordinates. Methods like `relocate()` to redefine the point, `displace()` to move the point and `rescale()` to rescale the point is defined.  

`rect()` objects are rectangles, with an array that defines the pixels value of the image of the rectangle. I added two additional methods, recolour() which takes input of location (a rect object itself) to recolour, and the colour to recolour that rectangle location to. This is achieved by just re-assigning the values in the pixel value array of the object over the range of the given dimensions.  
The other function saves the image as `“<name of object>.png”`. The method `Image.fromarray()` takes array input (Of size length x breadth x 3) and ‘RGB’ identifying the type of input and returns a Image object. `<object>.save()` method is used to save the file. The method returns the image name.  

### Game class definition and class variables  
The game is initialized using the constructor:  

```python
def __init__(self, cols, seed, depth = 2, StartPlayer = 0, MultiPlayer = 0, host = 1, Server_IP = '0'):
    self.columns = cols
    self.backend = Aer.get_backend('statevector_simulator')
    self.depth = depth
    self.seed = seed
    self.ready = 0
    self.turn = StartPlayer
    self.MultiPlayer = MultiPlayer

    #for multiplayer stuff
    self.host = "localhost"
    self.move_no = 0
    self.move_no_opp = 0
    self.move = "0:0:h:0"
    self.StartPlayer = StartPlayer # the person's role: 0 - Start first, else start second.
    self.host_bin = host # 1 if local system is host and host is Player 0.

    #board with initial flags of -1
    self.board = np.full((cols, cols), -1, dtype=int)
    self.coin_array = np.array([0]*cols)
    self.board_img = rect(cols*scale, cols*scale,  coord(0, 0), black, "board")

    #start server if multiplayer
    if MultiPlayer == 1:
        if self.host_bin == 0: # if not host, then take in the Server_IP
            self.host = Server_IP
        self.net = Network(self.host)
        if self.host_bin == 1: # if game host, send seed.
            self.net.send("seed:" + str(self.seed) + ":" + str(self.depth) + ":" + str(self.columns) + ":" + str(self.StartPlayer))
        else: # the player is player 1 as not host
            received = self.net.send("seed:want")
            received = received.split(":")
            self.seed = int(received[0])
            self.depth = int(received[1])
            self.column = int(received[2])
            if int(received[3]) == 0:
                self.StartPlayer = 1
                self.turn = 0
            else:
                self.StartPlayer = 0
                self.turn = 1

    #initialise pseudo-random circuit and corresponding statevector
    self.circuit = QuantumCircuit(cols, cols)
    self.state = Statevector(execute(self.circuit, self.backend).result().get_statevector())
    self.generate_random()
    self.ready = 1

    #display after starting game
    clear_output()
    print("Welcome to Qonnect four! \n Player " + str(self.turn) + " to begin. \n Initial state:")
    self.disp_game_state()
```  

First I initialize some variables of the object,  
`seed` - seed  
`depth` - depth of initial random circuit  
`column` - number of initial columns (and rows)  
`backend` - simulation backend  
`ready` - indicator if the game has begun (initalising, preprocessing, etc all done)  
`turn` - player who is going to start  
`board` - array for coin values 0/1/-1
`coin_array` - a counter for number of coins in each of the column  
`board_img` - `rect()` object for board image  
`circuit` - Quantum circuit of the game  
`state` - Statevector that is evolved and measured  

For Multiplayer over LAN, we have some additional variables required:  
`MultiPlayer` - whether LAN multiplayer game or not,  
`host` - host server IPv4,  
`move_no, move_no_opp` - count of moves done by the players so far so as to check if valid move,  
`StartPlayer` - local Player role  
`host_bin` - 0 if not host, 1 if host  
`move` - stores a string that can be parsed to indicate the latest valid move performed by the player

If it is a multiplayer game, the host first initializes an instance of `Network` class that initializes connection with the server script. Then sends the seed, depth, StartPlayer and column values to the server. The server stores this and sends to the client/non-host player upon connection. A simple socket system as used here allows to send and receive strings. So we send them separated by ":", which is parsed when received and used accordingly.  

After these steps, the game is initialized by using the seed to append a random circuit to the `circuit` object and obtain it's `state` object as `state`. It ends with outputting the circuit, etc and a message with who starts the game.  

Next I listed out what broadly made up my game. In Connect four, a person makes only one type of move - adding coins. Here, my board is represented by a circuit, where there is a one-one correspondence with the qubit and the column. The person is allowed to either add gates or make measurements on each. And when a measurement is made, single or multiple coins are added. So I needed to write methods/functions that:  

1) Initialize the circuit to a random state -  so no particular player had the advantage  
2) Make moves - measure/adding gates  
3) Check if there’s a match (four in a row/column/diagonal)  
4) Output the current state of the game  

For clarity, I’ll be explaining my code in the above order. When I thought about/wrote the code, I started with the outputting process, then checking the state, after which I wrote the functions for the moves and finally the random initialization, on the way adding whatever I felt required to the class constructor. In general it doesn't matter as long as you plan beforehand.  

### Random circuit initialization  

```python
def generate_random(self):
    seed_digits = [int(d) for d in str(bin((self.seed + 500)**3))[2:]]
    seed_digits = seed_digits[:(len(seed_digits) - (len(seed_digits)%3))]

    gate_sequence = []
    for a in range(int(len(seed_digits)/3)):
        gate_sequence.append(4*seed_digits[3*a] + 2*seed_digits[3*a + 1] + seed_digits[3*a + 2])

    number_temp = self.depth*self.columns*3
    gate_sequence_temp = gate_sequence

    if len(gate_sequence_temp) < number_temp:
        for a in range(int(number_temp/len(gate_sequence_temp))):
            gate_sequence += [int((d + self.seed*a)%8) for d in gate_sequence_temp]

    for d in range(self.depth):
        for a in range(self.columns):
            if gate_sequence[0] <= 5:
                self.add_gate(gates[gate_sequence[0]], [a])
                gate_sequence = gate_sequence[1:]
                continue

            if gate_sequence[0] == 6:
                b = gate_sequence[1]%self.columns - int(a == gate_sequence[1]%self.columns)
                self.add_gate('cx', [a, b])
                gate_sequence = gate_sequence[2:]
                continue

            if gate_sequence[0] == 7:
                b = gate_sequence[1]%self.columns - int(a == gate_sequence[1]%self.columns)
                c = gate_sequence[2]%self.columns
                c = c - int(c==a) - int(((c - int(c==a)) == b))
                self.add_gate('ccx', [a, b, c])
                gate_sequence = gate_sequence[3:]
                continue
    self.circuit.barrier()
    return
```  

To initialize a pseudo-random circuit, the method requires a random string as a seed, so the seed is passed when the game object is initiated. I first extend the seed to a larger number, then convert it to an array of “0” and ”1”. Extending the seed can be better done with a hash function, but I didn't wish to include any other external functions. Since I’ve restricted my gates to only 8 types, I make sure that the binary string length is a multiple of 3. At each iteration, the function will add gates to the circuit. I do this by parsing the array as three’s and converting into integer indices which will denote the gate type and if it is a multiqubit gate, the successive gates denote the required locations.  

In this game, since the game continues with the post measurement state of the circuit after a measurement is made and requires to wait for user input of moves, it cannot be continuously run on the quantum system and cannot be repeated with the same outcomes. So simulate the quantum state, I use a Statevector object over which I perform gates and measurements. So the game in it’s current state (V1.2) is a simulated system. I maintain a statevector object with all actions so far and a circuit object for illustration purposes only.  

Since the output of measurements are still statevectors, we can still form a circuit to evolve the state and perform the measurement on an actual quantum computer. While this is possible, it would introduce wait times into the game which is undesireable right now.  

### Adding gates  
```python
def h(self, args):
    if type(args) != type(2):
        clear_output()
        print("Invalid positional argument. Please pass a single position as argument.")
        self.disp_game_state()
        return 0
    self.add_gate('h', [args])
    return
```   

To add gates, I wrote separate class methods that have the same syntax as that of qiskit (like above), and also a common add_gate() method that does a check of the input parameters and performs the required gates. The reason I wrote add_gate() separately is that it would be easier to code to add random gates in the initial stage and also add gates on local copy of the game when played over LAN.  

```python
def add_gate(self, gate, args, flag = 1):
    
    if flag and self.ready:
        if self.MultiPlayer == 1:
            if self.StartPlayer == 0 and self.move_no != self.move_no_opp: # if player 0, then should play first
                print("Invalid move. Wait for other player to play move or try receiving move by game.get_move().")
                return
            if self.StartPlayer == 1 and self.move_no != (self.move_no_opp - 1):
                print("Invalid move. Wait for other player to play move or try receiving move by game.get_move().")
                return

    #check if column full
    for a in range(len(args)):
        if self.coin_array[args[a]] == self.columns:
            clear_output()
            print("Column full, try different move")
            self.disp_game_state()
            return 0

    #apply corresponding gates/operators
    qc_temp = QuantumCircuit(self.columns)

    if gate == "h" and len(args) == 1:
        self.circuit.h(args)
        qc_temp.h(args)
        self.state = self.state.evolve(Operator(qc_temp))

    #similarly for other single qubit gates

    if gate == "cx" and len(args) == 2:
        self.circuit.cx(args[0], args[1])
        qc_temp.cx(args[0], args[1])
        self.state = self.state.evolve(Operator(qc_temp))

    if gate == "ccx" and len(args) == 3:
        self.circuit.ccx(args[0], args[1], args[2])
        qc_temp.ccx(args[0], args[1], args[2])
        self.state = self.state.evolve(Operator(qc_temp))

    if self.ready:
        clear_output()
        print("Current state:")
        self.disp_game_state()

        if flag:
            self.pass_turn()
            self.move_no += 1
            self.make_move(gate, args)
    return
```  

First, the method checks if it is a multiplayer game and whether a player is adding the move (and not another internal code). `flag` is set to 1 by default and is 0 when we wish to not check if it's a valid move or update any move number/turn. This would help us when we play over LAN as we wish to update the opponent's move onto our local copy of the game instance.  

So once we checked if it's a valid move (the correct player's turn incase of LAN) and whether the column is not already full (since there is no point adding gates to columns that are already full with coins), we proceed to apply the gates. At each `if` clause, we check the gate type passed in `gate` and array length of args, then perform appropriate gates on the circuit `self.circuit` and evolve the statevector `self.state` according to the gate. This is done by initializing a `QuantumCircuit` instance, adding the gate and evolving by this circuit by `self.state.evolve()` method.  

`self.ready` checks if the game has begun. If `True`, clears output of cell using ipython method `clear_output()` and prints the current state using `self.disp_game_state()`. Then if `flag == True`, it passes the turn to the other player. `make_move()` method makes the message to be passed to the server if played over LAN.

### Server and Networking using sockets  
This section is almost entirely based on code that can be found [here](https://github.com/techwithtim/Network-Game-Tutorial) and a quick tutorial can be found [here](https://www.youtube.com/watch?v=-3B1v-K1oXE)  
The multiplayer over LAN in v1.2 uses two additional scripts, `Network()` class definition and `Server.py` to setup a server system on the host's computer.

```python
import socket

class Network:

    def __init__(self, IP):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = IP 
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            return str(e)

```

The constructor takes a parameter, the server IPv4 address passed on to it. To establish a connection, the method `connect()` of the socket class is used, to which the address, a tuple of the IP and port number is passed. This is executed in the `connect()` method of the Network class. This returns a message from the server on receiving the connection request.  

The `send()` method of the socket class (which is used in the above defined `Network.send()`) is used to send messages to the server and return any associated message. The `try: ... except:` is a python code used to handle errors instead of halting the complete program. If the try block throws any error, instead of halting the program, it returns the error message. We shall not delve further in this for now.  

```python
import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '' #replace with Server device IPv4
port = 5555

server_ip = socket.gethostbyname(server)
print("Server IP: " + server_ip)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
Data = ["0:0:h:0", "1:0:h:0"] #player:moveID:move:positions...
seed = 42
depth = 1
column = 7
StartPlayer = 0
def threaded_client(conn):
    global currentId, Data, seed, depth, column, StartPlayer
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                continue
            if reply == '2':
                conn.send(str.encode("Goodbye"))
                #break
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                
                if arr[0] == "seed":
                    if arr[1] == "want":
                        send = str(seed) + ":" + str(depth) + ":" + str(column) + ":" + str(StartPlayer) #sends initial states
                        print(send)
                    else:
                        seed = int(arr[1])
                        depth = int(arr[2])
                        column = int(arr[3])
                        StartPlayer = int(arr[4])
                        send = str(1)
                elif len(arr) == 1: #get move
                    iden = int(arr[0])
                    send = Data[1-iden]
                elif len(arr) >= 4:
                    iden = int(arr[0])
                    Data[iden] = reply
                    print("Added move: " + reply)
                    send = reply
                print("Sending: " + send)
                conn.sendall(str.encode(send))
        except:
            print("Nothing received")
    
    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    
    start_new_thread(threaded_client, (conn,))
```

First, the socket object is initiated, then the address and port number (it's identity) is 'binded' to the socket. Then the method `listen(x)` waits for x connect requests on the network. Once a connection is made, it  sets up a new thread using `start_new_thread()` with each connect requests received, and executes the `threaded_client` method. Each thread keeps looking for messages received. The received message is split and when "seed" is the first word, it checks if "want" is the second word, then sends the previously received seed, depth and other details of the game as sent by the host. Else it assumes that the following words were sent by the host and is assigned to the global variables of the server script, and sends a "1". If only one word is received, then it requires the last move sent by the other player, stored in `Data`. If 4 or more words are parsed from the sent message, it means that the player has sent in his move, then the code saves the message in `Data`.  

You can just prefix the messages with a tag indicating what the kind of message was (seed/seed-want/move/get-move).  

Further, in the main game class, I've defined `send_move()` and `get_move()` for the player to send their move to the server instance and receive the opponent's move. Please refer to the game files.

### Performing measurements  
So to perform measurements, we not only need to add them to the circuit, but also perform measurements on the statevector, and check if any other qubits collapsed to classical state as a result of this measurement. So we check the purity of the qubits before and after and see if there's a change to classical state. To check the purity, we use `probability(<qubit_position>)` method of statevector class which returns an 2 element list giving the amplitudes of 0/1 state of that qubit. `numpy.isclose()` checks if the two elements are approximately equal, upto a threshhold passed as the third parameter. The method then returns the array indicating where ever it is pure.  

```python
def check_pure(self):
    temp = [0]*self.columns
    for a in range(self.columns):
        if np.isclose(self.state.probabilities([a])[0], 0.0, 1e-3) or np.isclose(self.state.probabilities([a])[0], 1.0, 1e-3):
            temp[a] = 1
    return temp

def measure(self, qubit_pos, flag = 1):

    #when multiplayer, check if valid
    if flag: # if performing own move
        if self.MultiPlayer == 1:
            if self.StartPlayer == 0 and self.move_no != self.move_no_opp: # if player 0, then should play first
                print("Invalid move. Wait for other player to play move or try receiving move by game.get_move().")
                return
            if self.StartPlayer == 1 and self.move_no != (self.move_no_opp - 1):
                print("Invalid move. Wait for other player to play move or try receiving move by game.get_move().")
                return

        #check if the column is not full already
        if type(qubit_pos) != type(2):
            clear_output()
            print("Invalid input! Provide an integer for position number")
            self.disp_game_state()
            return 0
        if self.coin_array[qubit_pos] == self.columns:
            clear_output()
            print("Column full, try different move")
            self.disp_game_state()
            return 0
        if qubit_pos >= self.columns:
            clear_output()
            print("Column out of bounds! Enter value between 0 and " + str(self.column))
            self.disp_game_state()
            return 0
        else:
            self.coin_array[qubit_pos] +=1

        #get premeasurement pure states
        pure_before = self.check_pure()

        #perform measurement
        result, self.state = self.state.measure([qubit_pos])
        result = int(result)
        self.circuit.measure([qubit_pos], [qubit_pos])
        self.circuit.barrier()

        #check if any other qubits collapsed to pure due to measurement
        pure_after = self.check_pure()

        positions = [qubit_pos]
        results = [result]

        for a in range(self.columns):
            if pure_after[a] == 1 and pure_before[a] == 0 and a != qubit_pos:
                positions.append(a)
                res_extra, self.state = self.state.measure([a])
                res_extra = int(res_extra)
                results.append(res_extra)
                self.coin_array[a] += 1

        #for making move to send (for multiplayer)
        temp = [-1]*7
        for a in range(len(positions)):
            temp[positions[a]] = results[a]
        self.move_no += 1
        temp = [positions[0]] + temp # so we can mark where measurement was performed
        #temp = np.concatenate([temp, self.state.data])
        self.make_move("measure", temp)

    if not flag: # when updating opponent's move
        self.circuit.measure([qubit_pos[0]], [qubit_pos[0]])
        self.circuit.barrier()

        temp2 = qubit_pos[1:(self.columns+1)]

        meas = -2
        while meas != qubit_pos[qubit_pos[0] + 1]:
            res, state = self.state.measure([qubit_pos[0]])
            meas = int(res)
        self.state = state

        positions = []
        results = []
        for a in range(self.columns):
            if temp2[a] == 0:
                results.append(0)
                positions.append(a)
                self.coin_array[a] += 1
            elif temp2[a] == 1:
                results.append(1)
                positions.append(a)
                self.coin_array[a] += 1

    #update board and display
    for a in range(len(positions)):
        temp_coord = coord(positions[a], self.columns - self.coin_array[positions[a]])
        self.board[temp_coord.x][temp_coord.y] = results[a]
        temp_coord.rescale(scale)
        #add coin
        self.board_img.recolour(rect(scale, scale, temp_coord), coin_colours[results[a]])

    #check for matches
    end, player = self.check_board()
    if end:
        clear_output()
        print("Player "+ str(player) + " wins! \n ")
        print("Final state: ")
        self.disp_game_state()
        if self.MultiPlayer:
            self.send_move()
        wrap_up(self)
        return

    clear_output()
    print("Current state:")
    self.disp_game_state()

    if flag:
        self.pass_turn()
    return
```  

The method for measurement first checks `flag == 1` and then checks whether it is a valid input. If yes, then it proceeds to first check for pure states, then to add measurement to the circuit and also performs a measurement on the `self.state` using `measure()` method. Now it again checks for pure states, then marks the states where the measurement has collapsed due to measurement, and is added to `positions` array and the corresponding results in `results` array. Then the game board is updated, followed by a check for matches of four. If any found, it ends the game and outputs the result (winner).  

if `flag == 0` indicating a move that is being received from the server and not performed. In this case, a measurement is added to the circuit and the statevector `self.state` is measured till equal to the received measurement since we want the local copy to be equal to the other player's copy.  

### Checking the board  
The following method is used to check the board for any matches. If found, it returns `True` and the match coin (0/1) found.  

```python
def check_board(self):
    temp = np.array([0]*4)
    for x in range(self.columns):
        for y in range(self.columns):
            if self.board[x][y] !=-1:

                if x<= (self.columns - 4):
                    for a in range(4):
                        temp[a] = self.board[x + a][y]

                    if (temp == zeros).all() or (temp == ones).all():
                        return True, self.board[x][y]

                    #diagonal
                    if y<= (self.columns - 4):
                        #temp = np.array([0]*4)
                        for a in range(4):
                            temp[a] = self.board[x + a][y + a]

                        if (temp == zeros).all() or (temp == ones).all():
                            return True, self.board[x][y]

                if y<= (self.columns - 4):
                    #temp = np.array([0]*4)
                    for a in range(4):
                        temp[a] = self.board[x][y + a]

                    if (temp == zeros).all() or (temp == ones).all():
                        return True, self.board[x][y]

                    #antidiagonal
                    if x >= 4:
                        for a in range(4):
                            temp = self.board[x - a][y + a]

                        if (temp == zeros).all() or (temp == ones).all():
                            return True, self.board[x][y]
    return False, -1
```  
`self.board` is an array that contains values of the coins. -1 if no coin; 0/1 for either player respectively.  

In a double for loop, at every board position, I check the row, column, diagonal and antidiagonal positions for any matches. If any are found, it returns `True` with the coin value (0/1). If you notice in the above code, first I check if the location actual has four or more positions ahead or behind as required so as to have a valid array to reference, hence to compare.

### Output display  
I wrote separate functions to create and save the output images and also display the same, as Jupyter notebook does not in default allow display of multiple images at a time.  

```python
def disp_game_state(self):
    print("Board:")
    self.disp_board()
    print("Circuit:")
    self.disp_circuit()
    print("Qsphere:")
    self.disp_qsphere()
    print("Bloch spheres:")
    self.disp_bloch_multivector()
    return

def disp_circuit(self):
    self.circuit.draw('mpl').savefig('circuit.png')
    display(Im(filename='circuit.png', unconfined = True))
    return

def disp_board(self):
    self.board_img.save_image()
    display(Im(filename='board.png'))
    return

def disp_qsphere(self):
    plot_state_qsphere(self.state.data).savefig('qsphere.png')
    display(Im(filename='qsphere.png', unconfined = True))
    return

def disp_bloch_multivector(self):
    plot_bloch_multivector(self.state.data).savefig('bloch.png')
    display(Im(filename='bloch.png', unconfined = True))
    return
```  

The method `self.circuit.draw('mpl')` returns a matplotlib figure, which can be saved using the `savefig()` method. Then the method displays the full sized image (Normally it shrinks the image to fit) by importing the image file and passing `unconfined = True` option to create a Image object (IPython.display.Image has been imported as Im).  


## Conclusions  
The entire code can be found in the github repository shared. Only parts of the code are explained here. As you've seen, making a quantum game is quite simple. With a good idea and a plan of the structure and division of the code, you can easily write your own game. when you need help, Google and stack exchange are your best friends along with Qiskit documentation. Start by listing the possible classes and methods you will need and defining one by one, then proceed filling them up, modifying on the go.  

All the very best!

### References and links  
1) My code: [https://github.com/Praveen91299/QonnectFour](https://github.com/Praveen91299/QonnectFour)  
2) Quantum Dojo: [https://github.com/amirebrahimi/quantumdojo](https://github.com/amirebrahimi/quantumdojo)  
3) List of Quantum games: [https://github.com/HuangJunye/Awesome-Quantum-Games](https://github.com/HuangJunye/Awesome-Quantum-Games)  
4) Creating a Conda environment: [https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/)  
5) Conda documentation: [https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)  
6) Network game tutorials by Tech with Tim: [https://github.com/techwithtim/Network-Game-Tutorial](https://github.com/techwithtim/Network-Game-Tutorial)  
