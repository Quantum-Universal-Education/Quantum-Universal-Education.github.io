{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# QuantumPoker Solo Version\n",
    "\n",
    "Hi quantum traveler! You are about to partake in the adventure of giving superpowers to the most mysterious properties of the universe. You know, _somebody_ once said that programming is the closest thing humans have to superpowers — now imagine giving superpowers to the most mysterious and overwhelming force in the universe: quantum mechanics. Yes, quantum computing!\n",
    "\n",
    "Once incomprehensible, we've devised a way for you to understand its basic principles — not through complex matrices and symbols — but using real-world analogies that are far more accessible than pure math. That's how I (or we, depending on the superposition!) understand these very complex principles of quantum mechanics.\n",
    "\n",
    "So, Poker... but quantum poker. If you understand poker, you'll understand this. So let's begin!\n",
    "\n",
    "By the way, you'll need some basic programming knowledge to run this Python script. If coding isn't your thing, I recommend trying the printed version of the game — it's also a lot of fun and can be played with friends.\n",
    "\n",
    "So, what is QuantumPoker?\n",
    "\n",
    "QuantumPoker (solo version) is a game where the goal is to get the highest score by summing the values of your qubits. You'll be given 4 virtual qubit cards. These cards can be flipped (0 ↔ 1), shown or hidden, and superpositioned or collapsed.\n",
    "\n",
    "Okay, let's set this up first and explain more as we go."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Basic imports\n",
    "import random\n",
    "\n",
    "# Constants\n",
    "SET_SIZE = 4  # how many cards are given to you\n",
    "\n",
    "# Variables\n",
    "user_cards = []"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**Explanation:** In classical computing, a bit can only have two states — 0 or 1.\n",
    "\n",
    "A qubit is more complex. It can be described using three numbers, or angles: X, Y, and Z — each theoretically with infinite possible values between 0 and 1. Although in practice, current quantum computers work with discrete steps like 0.1, 0.2, 0.3, etc.\n",
    "\n",
    "So instead of just storing a boolean value, we'll use a dictionary with x, y, and z to represent the qubit.\n",
    "\n",
    "In our game:\n",
    "- `x` is the core value: 0, 1, or `None` if it's in superposition.\n",
    "- `y` determines visibility: 1 means hidden.\n",
    "- `z` indicates bet strength: 1 doubles the score."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Let's define the cards\n",
    "def card(x, y=0, z=0):\n",
    "    return {\n",
    "        \"x\": x,  # standard value of the card, can be 0, 1, or None (superposition)\n",
    "        \"y\": y,  # 1 means the card is hidden; conceptually an imaginary phase\n",
    "        \"z\": z,  # 1 means the card doubles the bet\n",
    "    }\n",
    "\n",
    "# A function to assign you the cards randomly\n",
    "def assign_user_cards():\n",
    "    global user_cards\n",
    "    user_cards = [card(random.randint(0, 1)) for _ in range(SET_SIZE)]\n",
    "\n",
    "# A function to print the cards\n",
    "def print_user_cards():\n",
    "    print(\"---- Your Qbit Cards ----\")\n",
    "    for i, card in enumerate(user_cards):\n",
    "        x, y, z = card['x'], card['y'], card['z']\n",
    "        title = f\"Qbit {i} ->\"\n",
    "        if x == None:\n",
    "            print(f\"{title} SUPERPOSITION! x:???  y:{y}   z:{z}\")\n",
    "        elif y == 1:\n",
    "            print(f\"{title} HIDDEN!\")\n",
    "        else:\n",
    "            print(f\"{title} x:{x}   y:{y}   z:{z}\")\n",
    "    print(\"-------------------------\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Now let's preview how the qbit cards will be given to you\n",
    "assign_user_cards()\n",
    "print_user_cards()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now that you have your qubit cards, you'll be given 5 community cards representing Pauli Gates. These will be revealed one by one, and you'll choose which of your qubits to apply them to. Choose wisely — the goal is to maximize your score."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "PAULI_CARDS = [\n",
    "    \"X\",  # This Pauli card flips a qubit from 0 to 1 or 1 to 0 on the X axis.\n",
    "          # If the card is in superposition (x is None), it has no effect.\n",
    "          # (Note: In real quantum mechanics, it would still have an effect!)\n",
    "    \"Y\",  # This flips the qubit like X, but also toggles visibility (y).\n",
    "          # If it was visible, it becomes hidden, and vice versa.\n",
    "    \"Z\",  # Toggles phase, which in our game means doubling or normalizing the bet (z).\n",
    "    \"H\",  # Hadamard gate: sets the qubit into superposition (x=None).\n",
    "          # If already in superposition, collapses it randomly to 0 or 1.\n",
    "          # In real quantum systems, this results in probabilistic outcomes.\n",
    "]\n",
    "\n",
    "COMMUNITY_CARDS_COUNT = 5\n",
    "community_cards = []"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now let's add the functions to apply the Pauli Cards to your qubits."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# This function shuffles and grants 5 community Pauli cards\n",
    "def assign_community_cards():\n",
    "    global community_cards\n",
    "    community_cards = [random.choice(PAULI_CARDS) for _ in range(COMMUNITY_CARDS_COUNT)]\n",
    "\n",
    "def apply_x(qbit):\n",
    "    if qbit['x'] == 0:\n",
    "        qbit['x'] = 1\n",
    "    elif qbit['x'] == 1:\n",
    "        qbit['x'] = 0\n",
    "    # if x is None (superposition), do nothing\n",
    "    return qbit\n",
    "\n",
    "def apply_y(qbit):\n",
    "    qbit = apply_x(qbit)\n",
    "    qbit['y'] = 1 - qbit['y']  # toggle visibility\n",
    "    return qbit\n",
    "\n",
    "def apply_z(qbit):\n",
    "    qbit['z'] = 1 - qbit['z']  # toggle phase/double bet\n",
    "    return qbit\n",
    "\n",
    "def apply_h(qbit):\n",
    "    if qbit['x'] == None:\n",
    "        qbit['x'] = random.randint(0, 1)  # collapse to 0 or 1\n",
    "    else:\n",
    "        qbit['x'] = None  # go into superposition\n",
    "    return qbit\n",
    "\n",
    "# Map Pauli card names to functions\n",
    "pauli_functions = {\n",
    "    \"X\": apply_x,\n",
    "    \"Y\": apply_y,\n",
    "    \"Z\": apply_z,\n",
    "    \"H\": apply_h,\n",
    "}\n",
    "\n",
    "def apply_card(card_number, pauli_card):\n",
    "    global user_cards\n",
    "    if card_number < 0 or card_number >= len(user_cards):\n",
    "        return False\n",
    "    user_cards[card_number] = pauli_functions[pauli_card](user_cards[card_number])\n",
    "    return True"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now, after all Pauli Cards are used, we must \"measure\" the qubits.\n",
    "\n",
    "In quantum computing, some properties like visibility (y) or phase (z) are not directly observable in the classical sense. So, we simplify: we just sum x + z for each qubit.\n",
    "\n",
    "Y is ignored in scoring, as it only influenced what you could see, not the underlying value.\n",
    "\n",
    "Final score is the total of all x and z values."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def measure_qbit(i, q):\n",
    "    if q[\"x\"] == None:\n",
    "        q[\"x\"] = random.randint(0, 1)\n",
    "        print(f\"Qbit {i} was in superposition and collapsed into {q['x']}. Now let's measure it:\")\n",
    "    print(f\"Measuring qbit {i} x:{q['x']} + z:{q['z']} = {q['x'] + q['z']}\")\n",
    "    return q[\"x\"] + q[\"z\"]\n",
    "\n",
    "def measure():\n",
    "    score = 0\n",
    "    maximum = SET_SIZE * 2\n",
    "    for i, q in enumerate(user_cards):\n",
    "        score += measure_qbit(i, q)\n",
    "    if score >= maximum:\n",
    "        print(f\"Congrats! You achieved the maximum score of {maximum}. You're a quantum master!\")\n",
    "    else:\n",
    "        print(f\"You scored {score} points. That's {maximum - score} below the max. Keep trying!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now comes the game loop.\n",
    "\n",
    "The function below assigns you new qubit cards, reveals the 5 Pauli cards one at a time, and lets you apply each to the qubit of your choice.\n",
    "\n",
    "To play again, just run the play() function again."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Notebook-friendly version without screen clearing\n",
    "def play_notebook():\n",
    "    assign_user_cards()\n",
    "    print(\"---- █ █ █ █ █ QUANTUM*POKER (solo edition) █ █ █ █ █ ----\")\n",
    "    print(\"                NOW LET'S THE GAME START!                \\n\")\n",
    "    assign_community_cards()\n",
    "    \n",
    "    print(\"Your starting cards:\")\n",
    "    print_user_cards()\n",
    "    print(f\"\\nYou have {len(community_cards)} Pauli cards to use: {community_cards}\\n\")\n",
    "    \n",
    "    for i, card in enumerate(community_cards):\n",
    "        print(f\"\\n=== Round {i+1} ===\")\n",
    "        print(f\"Pauli Card: {card}\")\n",
    "        print(\"Current state:\")\n",
    "        print_user_cards()\n",
    "        \n",
    "        while True:\n",
    "           try:\n",
    "               choice = int(input(f\"Choose qbit number to apply {card} card (0-{len(user_cards)-1}): \"))\n",
    "               applied = apply_card(choice, card)\n",
    "               if applied:\n",
    "                   print(f\"✓ Applied Pauli {card} to Qbit {choice}\")\n",
    "                   break\n",
    "               else:\n",
    "                   print(\"Invalid card number, try again.\")\n",
    "           except ValueError:\n",
    "               print(\"Please enter a valid number.\")\n",
    "\n",
    "    print(\"\\n\" + \"=\"*50)\n",
    "    print(\"FINAL MEASUREMENT\")\n",
    "    print(\"=\"*50)\n",
    "    print(\"Final card state:\")\n",
    "    print_user_cards()\n",
    "    print(\"\\nMeasuring...\")\n",
    "    measure()\n",
    "\n",
    "# Original version for those who want the full experience\n",
    "def play():\n",
    "    print('\\n' * 50)\n",
    "    assign_user_cards()\n",
    "    print(\"\\n\\n---- █ █ █ █ █ QUANTUM*POKER (solo edition) █ █ █ █ █ ----\")\n",
    "    print(\"                NOW LET'S THE GAME START!                \\n\")\n",
    "    assign_community_cards()\n",
    "    input(\"Press Enter to Start Playing...\")\n",
    "    print('\\n' * 50)\n",
    "    applied_msg = None\n",
    "    for i, card in enumerate(community_cards):\n",
    "        print('\\n' * 50)\n",
    "        if applied_msg:\n",
    "            print(applied_msg)\n",
    "        print_user_cards()\n",
    "        remaining = len(community_cards) - i\n",
    "        print(f\"Pauli Cards Remaining Unopened [{' █ ' * remaining}]\\n\")\n",
    "        if i == 0:\n",
    "            print(f\"Let's open the first card!\")\n",
    "        else:\n",
    "            print(f\"Now let's open the next card\")\n",
    "        input(\"Press Enter to open it! \")\n",
    "        print(f\"\\n---- You've got Pauli {card} !!!! ----\")\n",
    "        while True:\n",
    "           try:\n",
    "               choice = int(input(f\"Choose qbit number to apply the {card} card (0-{len(user_cards)-1}): \"))\n",
    "               applied = apply_card(choice, card)\n",
    "               if applied:\n",
    "                   applied_msg = f\"\\n\\nApplied Pauli Card {card} to Qbit Card {choice}--------\"\n",
    "                   break\n",
    "               else:\n",
    "                   print(\"Invalid card number, try again.\")\n",
    "           except ValueError:\n",
    "               print(\"Please enter a valid number.\")\n",
    "\n",
    "    # Let's measure your qbits!\n",
    "    print(\"\\n\\nNow that there are no community cards left, let's measure everything into the classic world!\\n\")\n",
    "    input(\"Press Enter to Meaure Everthing...\")\n",
    "    print('\\n' * 50)\n",
    "    print_user_cards()\n",
    "    measure()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Start Playing!\n",
    "\n",
    "Run the cell below to start playing QuantumPoker!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "play()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "I've hope this game inspired you to know more about quantum mechanics and quantum computing, remember that no matter how counterintuitive are this world, there is always ways to visualize this!"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}