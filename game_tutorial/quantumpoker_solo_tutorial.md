# QuantumPoker Solo Version

Hi quantum traveler! You are about to partake in the adventure of giving superpowers to the most mysterious properties of the universe. You know, _somebody_ once said that programming is the closest thing humans have to superpowers — now imagine giving superpowers to the most mysterious and overwhelming force in the universe: quantum mechanics. Yes, quantum computing! 

Once incomprehensible, we've devised a way for you to understand its basic principles — not through complex matrices and symbols — but using real-world analogies that are far more accessible than pure math. That's how I (or we, depending on the superposition!) understand these very complex principles of quantum mechanics.

So, Poker... but quantum poker. If you understand poker, you'll understand this. So let's begin!

By the way, you'll need some basic programming knowledge to run this Python script. If coding isn't your thing, I recommend trying the printed version of the game — it's also a lot of fun and can be played with friends.

So, what is QuantumPoker?

QuantumPoker (solo version) is a game where the goal is to get the highest score by summing the values of your qubits. You'll be given 4 virtual qubit cards. These cards can be flipped (0 ↔ 1), shown or hidden, and superpositioned or collapsed.

Okay, let's set this up first and explain more as we go.

```python
# Basic imports
import random

# Constants
SET_SIZE = 4  # how many cards are given to you

# Variables
user_cards = []
```

**Explanation:** In classical computing, a bit can only have two states — 0 or 1.

A qubit is more complex. It can be described using three numbers, or angles: X, Y, and Z — each theoretically with infinite possible values between 0 and 1. Although in practice, current quantum computers work with discrete steps like 0.1, 0.2, 0.3, etc.

So instead of just storing a boolean value, we'll use a dictionary with x, y, and z to represent the qubit.

In our game:
- `x` is the core value: 0, 1, or `None` if it's in superposition.
- `y` determines visibility: 1 means hidden.
- `z` indicates bet strength: 1 doubles the score.

```python
# Let's define the cards
def card(x, y=0, z=0):
    return {
        "x": x,  # standard value of the card, can be 0, 1, or None (superposition)
        "y": y,  # 1 means the card is hidden; conceptually an imaginary phase
        "z": z,  # 1 means the card doubles the bet
    }

# A function to assign you the cards randomly
def assign_user_cards():
    global user_cards
    user_cards = [card(random.randint(0, 1)) for _ in range(SET_SIZE)]

# A function to print the cards
def print_user_cards():
    print("---- Your Qbit Cards ----")
    for i, card in enumerate(user_cards):
        x, y, z = card['x'], card['y'], card['z']
        title = f"Qbit {i} ->"
        if x == None:
            print(f"{title} SUPERPOSITION! x:???  y:{y}   z:{z}")
        elif y == 1:
            print(f"{title} HIDDEN!")
        else:
            print(f"{title} x:{x}   y:{y}   z:{z}")
    print("-------------------------")

# Now let's preview how the qbit cards will be given to you
assign_user_cards()
print_user_cards()
```

Now that you have your qubit cards, you'll be given 5 community cards representing Pauli Gates. These will be revealed one by one, and you'll choose which of your qubits to apply them to. Choose wisely — the goal is to maximize your score.

```python
PAULI_CARDS = [
    "X",  # This Pauli card flips a qubit from 0 to 1 or 1 to 0 on the X axis.
          # If the card is in superposition (x is None), it has no effect.
          # (Note: In real quantum mechanics, it would still have an effect!)
    "Y",  # This flips the qubit like X, but also toggles visibility (y).
          # If it was visible, it becomes hidden, and vice versa.
    "Z",  # Toggles phase, which in our game means doubling or normalizing the bet (z).
    "H",  # Hadamard gate: sets the qubit into superposition (x=None).
          # If already in superposition, collapses it randomly to 0 or 1.
          # In real quantum systems, this results in probabilistic outcomes.
]

COMMUNITY_CARDS_COUNT = 5
community_cards = []
```

Now let's add the functions to apply the Pauli Cards to your qubits.

```python
# This function shuffles and grants 5 community Pauli cards
def assign_community_cards():
    global community_cards
    community_cards = [random.choice(PAULI_CARDS) for _ in range(COMMUNITY_CARDS_COUNT)]

def apply_x(qbit):
    if qbit['x'] == 0:
        qbit['x'] = 1
    elif qbit['x'] == 1:
        qbit['x'] = 0
    # if x is None (superposition), do nothing
    return qbit

def apply_y(qbit):
    qbit = apply_x(qbit)
    qbit['y'] = 1 - qbit['y']  # toggle visibility
    return qbit

def apply_z(qbit):
    qbit['z'] = 1 - qbit['z']  # toggle phase/double bet
    return qbit

def apply_h(qbit):
    if qbit['x'] == None:
        qbit['x'] = random.randint(0, 1)  # collapse to 0 or 1
    else:
        qbit['x'] = None  # go into superposition
    return qbit

# Map Pauli card names to functions
pauli_functions = {
    "X": apply_x,
    "Y": apply_y,
    "Z": apply_z,
    "H": apply_h,
}

def apply_card(card_number, pauli_card):
    global user_cards
    if card_number < 0 or card_number >= len(user_cards):
        return False
    user_cards[card_number] = pauli_functions[pauli_card](user_cards[card_number])
    return True
```

Now, after all Pauli Cards are used, we must "measure" the qubits.

In quantum computing, some properties like visibility (y) or phase (z) are not directly observable in the classical sense. So, we simplify: we just sum x + z for each qubit.

Y is ignored in scoring, as it only influenced what you could see, not the underlying value.

Final score is the total of all x and z values.

```python
def measure_qbit(i, q):
    if q["x"] == None:
        q["x"] = random.randint(0, 1)
        print(f"Qbit {i} was in superposition and collapsed into {q['x']}. Now let's measure it:")
    print(f"Measuring qbit {i} x:{q['x']} + z:{q['z']} = {q['x'] + q['z']}")
    return q["x"] + q["z"]

def measure():
    score = 0
    maximum = SET_SIZE * 2
    for i, q in enumerate(user_cards):
        score += measure_qbit(i, q)
    if score >= maximum:
        print(f"Congrats! You achieved the maximum score of {maximum}. You're a quantum master!")
    else:
        print(f"You scored {score} points. That's {maximum - score} below the max. Keep trying!")
```

Now comes the game loop.

The function below assigns you new qubit cards, reveals the 5 Pauli cards one at a time, and lets you apply each to the qubit of your choice.

To play again, just run the play() function again.

```python
def play():
    print('\n' * 50)
    assign_user_cards()
    print("\n\n---- █ █ █ █ █ QUANTUM*POKER (solo edition) █ █ █ █ █ ----")
    print("                NOW LET'S THE GAME START!                \n")
    assign_community_cards()
    input("Press Enter to Start Playing...")
    print('\n' * 50)
    applied_msg = None
    for i, card in enumerate(community_cards):
        print('\n' * 50)
        if applied_msg:
            print(applied_msg)
        print_user_cards()
        remaining = len(community_cards) - i
        print(f"Pauli Cards Remaining Unopened [{' █ ' * remaining}]\n")
        if i == 0:
            print(f"Let's open the first card!")
        else:
            print(f"Now let's open the next card")
        input("Press Enter to open it! ")
        print(f"\n---- You've got Pauli {card} !!!! ----")
        while True:
           try:
               choice = int(input(f"Choose qbit number to apply the {card} card (0-{len(user_cards)-1}): "))
               applied = apply_card(choice, card)
               if applied:
                   applied_msg = f"\n\nApplied Pauli Card {card} to Qbit Card {choice}--------"
                   break
               else:
                   print("Invalid card number, try again.")
           except ValueError:
               print("Please enter a valid number.")

    # Let's measure your qbits!
    print("\n\nNow that there are no community cards left, let's measure everything into the classic world!\n")
    input("Press Enter to Meaure Everthing...")
    print('\n' * 50)
    print_user_cards()
    measure()

play()
```

I've hope this game inspired you to know more about quantum mechanics and quantum computing, remember that no matter how counterintuitive are this world, there is always ways to visualize this!