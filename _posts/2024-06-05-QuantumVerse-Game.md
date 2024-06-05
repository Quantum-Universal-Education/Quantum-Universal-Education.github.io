# QuantumVerse 🌌🎮- A Gamer's Bot!

## Introduction
Welcome to **QuantumVerse**, an innovative project combining education and entertainment in the realm of quantum computing! QuantumVerse consists of two main components: 
- **QuantBot** 🤖, a Discord bot designed to educate and engage users about quantum computing through reminders and interactive games
- **Quantum Quest** ✨, an interactive game that introduces players to fundamental quantum computing concepts like superposition and quantum gates.
- And well, a fusion of these, **QuestyBot**💎 where you can play from your discord bot!

This project aims to bridge the gap between theoretical knowledge and practical application, making quantum computing accessible and fun for high school and undergraduate students.

### Note: Do follow along to setup and create your own version of QuantumVerse! 🚀

## Part 1 : QuantBot for Discord (Quantum Universal Education Discord Server in this tutorial!) 🤖📅

### Objective 🎯

In this tutorial, we'll create QuantBot, a Discord bot for Quantum Universal Education. QuantBot will provide reminders about upcoming quantum computing events using Google Calendar API.

### Prerequisites 📝

- Basic understanding of Python programming.
- Familiarity with Discord and setting up bots.
- Interest in quantum computing concepts and applications.

### Tools Required 🛠️

- Python (3.7 or higher recommended)
- Discord.py library (for interacting with Discord API)
- Google Calendar API (for event reminders)

### Follow the below Guide for Setup 🚀

#### 1. Setting Up Your Development Environment ⚙️

Ensure Python is installed and install necessary libraries:

```bash
pip install discord.py google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

#### 2. Creating a Discord Bot 🤖

- Create a Discord Bot:
  - Go to the `Discord Developer Portal`.
  - Click on **"New Application"** and give your bot a name.
  - Navigate to the **"Bot"** tab and click **"Add Bot"**.
  - Copy the bot token. This will be used to authenticate your bot with Discord.

- Invite the Bot to Your Server:
  - Go to the **"OAuth2"** tab.
  - In the **"Scopes"** section, select "bot".
  - In the **"Bot Permissions"** section, choose permissions like "Send Messages" and "Read Message History".
  - Copy the generated OAuth2 URL and paste it into your browser. Select a server to **invite** your bot.

 #### 3. Setting Up Google Calendar API 📅

- Create a Google Cloud Project:

   - Go to the Google Cloud Console.
   - Create a new project or select an existing project.
   - Enable the Google Calendar API for your project:
   - Search for "Google Calendar API" in the library.
   - Click on "Enable".

- Generate Google Calendar API Credentials:

   - Go to the "Credentials" tab.
   - Click on "Create Credentials" and select "Service Account".
   - Fill in the necessary details and grant the required permissions (typically "Project" > "Editor").
   - Download the JSON file containing your credentials. Rename it to credentials.json and store it securely.

#### 4. Coding the Quantum Computing Reminder Bot 🖥️

Now, let's actually get on to the coding part~

We will be implement the bot using Python and Discord.py and integrate it with Google Calendar to fetch upcoming events and send reminders!

```python
import os
import datetime
import discord
from discord.ext import commands, tasks
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Discord bot setup
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
bot = commands.Bot(command_prefix='!')

# Google Calendar setup
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Initialize Google Calendar service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

# Function to fetch upcoming events from Google Calendar
def fetch_upcoming_events():
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=5, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

# Background task to check for upcoming events and send reminders
@tasks.loop(minutes=30)
async def check_upcoming_events():
    events = fetch_upcoming_events()
    if not events:
        return
    upcoming_events = "\n".join([f"📅 {event['summary']}: {event['start']['dateTime']}" for event in events])
    channel = bot.get_channel(YOUR_CHANNEL_ID)  # Put your Discord channel ID here
    await channel.send(f"🔔 Upcoming Quantum Computing Events:\n{upcoming_events}")

@bot.event
async def on_ready():
    print(f'🤖 Logged in as {bot.user}!')
    check_upcoming_events.start()

# Command to fetch upcoming events manually
@bot.command(name='events')
async def fetch_events(ctx):
    events = fetch_upcoming_events()
    if not events:
        await ctx.send("No upcoming events found.")
        return
    upcoming_events = "\n".join([f"📅 {event['summary']}: {event['start']['dateTime']}" for event in events])
    await ctx.send(f"🔔 Upcoming Quantum Computing Events:\n{upcoming_events}")

# Run the bot
bot.run(TOKEN)
```
In the code I provided, do not forget to replace YOUR_DISCORD_BOT_TOKEN with your actual Discord bot token and YOUR_CHANNEL_ID with the ID of the Discord channel where you want the bot to send reminders, as 
these parameters are unique, obviously.

#### Sooo, our part 1 ends here and our QuantBot is ready! Now let's move on to the next part, The QuantQuest!

## Part 2 : The "Quantum Quest" Game 🎮

### Objective
In this part of the tutorial, we'll design the "Quantum Quest" Game using Python and Quantum Development Kit (Q#). This game will simulate quantum computing concepts like superposition and quantum gates, providing an interactive learning experience.

### Prerequisites 📝
- Basic understanding of Python programming.
- Interest in learning about quantum computing concepts like superposition.

### Tools Required 🛠️
- Python (3.7 or higher recommended)
- Quantum Development Kit (Q# and Microsoft Quantum Libraries)
- Jupyter Notebook (for interactive coding and explanations)

### Step-by-Step Guide 🚀

#### 1. Setting Up Your Development Environment ⚙️
Install the Quantum Development Kit (Q#) and necessary Python libraries:

```bash
pip install qsharp matplotlib
```

#### 2. Creating the "Quantum Quest" Game 🎮
Develop a Python script or Jupyter Notebook that simulates a quantum computing game. Players interact with qubits, apply quantum gates, and observe outcomes based on quantum mechanics principles.

- Example game structure:

```python
import qsharp
from Quantum.QuantumGame import QuantumGame

# Initialize Quantum Game
game = QuantumGame.simulate()

# Game Loop
while not game.is_game_over():
    print("Current Qubit State:", game.get_qubit_state())

    # Player Interaction
    action = input("Enter 'H' to apply Hadamard gate, 'M' to measure, or 'Q' to quit: ").upper()

    if action == 'H':
        game.apply_hadamard()
    elif action == 'M':
        result = game.measure()
        print("Measurement Result:", result)
    elif action == 'Q':
        break
    else:
        print("Invalid action. Please try again.")

print("Game ended. Thanks for playing!")
```

#### 3. Explanation and Educational Points ℹ️

- **Quantum Game Setup:**

    - Qubits: Represent quantum bits, the basic unit of quantum information.
    - Quantum Gates (Hadamard, Measurement): Operations that manipulate qubits, such as the Hadamard gate for superposition and measurement to observe qubit state.
    - Superposition: Qubits can exist in multiple states simultaneously, unlike classical bits.
    - Measurement: Observes the state of a qubit, collapsing it to a classical state.

- **Game Mechanics:**

    - Players interact with qubits using quantum gates.
    - Explore quantum phenomena like superposition and measurement outcomes.

#### 4. Enhancements and Further Learning 🚀

**Since this is an example tutorial, we are limiting ourselves to a simple game structure, however you can explore additional features to your games**
**Few Ideas are given below:**

  - **Advanced Quantum Algorithms:**
        - Implement more complex quantum algorithms.
        - Introduce quantum error correction and entanglement concepts.

  - **Visualization:**
        - Use matplotlib or similar libraries to visualize quantum states and gate operations.

**Lastly, our final part, **The QuestyBot!** is here!**

## Part 3 : The "QuestyBot" - Integrating QuantQuest with QuantBot 🚀🤖

### Objective
Integrate the "Quantum Quest" Game with the Quantum Computing Reminder Bot on Discord. Allow players to start and interact with the game directly through bot commands, enhancing engagement and learning about quantum computing concepts.

### Step-by-Step Integration

#### 1. Update the Discord Bot to Include Game Commands 🤖

We are basically modify the Discord bot to accept commands for starting and playing the "Quantum Quest" Game!

```python
@bot.command(name='start_game')
async def start_game(ctx):
    global game
    game = QuantumGame.simulate()
    await ctx.send("🎮 Quantum Quest Game started! Use commands to interact with qubits.")

@bot.command(name='apply_gate')
async def apply_gate(ctx, gate: str):
    global game
    if not game:
        await ctx.send("Please start the game first using !start_game.")
        return

    if gate.lower() not in ['h', 'x', 'z', 'measure']:
        await ctx.send("Invalid gate. Use 'H', 'X', 'Z', or 'measure'.")
        return

    if gate.lower() == 'h':
        game.apply_hadamard()
        await ctx.send("Applied Hadamard gate.")
    elif gate.lower() == 'x':
        game.apply_x()
        await ctx.send("Applied X gate.")
    elif gate.lower() == 'z':
        game.apply_z()
        await ctx.send("Applied Z gate.")
    elif gate.lower() == 'measure':
        result = game.measure()
        await ctx.send(f"Measured qubit: {result}")

@bot.command(name='end_game')
async def end_game(ctx):
    global game
    game = None
    await ctx.send("🛑 Quantum Quest Game ended. Thanks for playing!")

# Error handling
@apply_gate.error
async def apply_gate_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing gate argument. Use 'H', 'X', 'Z', or 'measure'.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument type. Use 'H', 'X', 'Z', or 'measure'.")

@bot.event
async def on_ready():
    print(f'🤖 Logged in as {bot.user}!')
    check_upcoming_events.start()

# Run the bot
bot.run(TOKEN)
```
#### 2. Integrate Quantum Quest Game Logic 🎮

Integrate the existing **"Quantum Quest"** Game logic with Discord bot commands to handle player interactions. Ensure the game state persists throughout interactions.

```python
import qsharp
from Quantum.QuantumGame import QuantumGame

# Initialize Quantum Game
game = None

@bot.command(name='start_game')
async def start_game(ctx):
    global game
    game = QuantumGame.simulate()
    await ctx.send("🎮 Quantum Quest Game started! Use commands to interact with qubits.")

@bot.command(name='apply_gate')
async def apply_gate(ctx, gate: str):
    global game
    if not game:
        await ctx.send("Please start the game first using !start_game.")
        return

    if gate.lower() not in ['h', 'x', 'z', 'measure']:
        await ctx.send("Invalid gate. Use 'H', 'X', 'Z', or 'measure'.")
        return

    if gate.lower() == 'h':
        game.apply_hadamard()
        await ctx.send("Applied Hadamard gate.")
    elif gate.lower() == 'x':
        game.apply_x()
        await ctx.send("Applied X gate.")
    elif gate.lower() == 'z':
        game.apply_z()
        await ctx.send("Applied Z gate.")
    elif gate.lower() == 'measure':
        result = game.measure()
        await ctx.send(f"Measured qubit: {result}")

@bot.command(name='end_game')
async def end_game(ctx):
    global game
    game = None
    await ctx.send("🛑 Quantum Quest Game ended. Thanks for playing!")

# Error handling
@apply_gate.error
async def apply_gate_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing gate argument. Use 'H', 'X', 'Z', or 'measure'.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument type. Use 'H', 'X', 'Z', or 'measure'.")

@bot.event
async def on_ready():
    print(f'🤖 Logged in as {bot.user}!')

# Run the bot
bot.run(TOKEN)
```

#### 3. Testing and Deployment 🚀

Finally, test the integration to ensure players can start, interact, and end the game seamlessly within the Discord server. Deploy the updated bot to your Discord server and invite users to engage with the integrated "Quantum Quest" Game!

### Yayy you completed the tutorial!! 🎉

By completing this tutorial, you've created a Quantum Computing Reminder Bot for Discord, designed the "Quantum Quest" Game using Python and Q#, and integrated the game with the Discord bot for interactive gameplay. These projects provide practical hands-on experience in quantum computing concepts and software development, which is suitable for you high schoolers and undergraduate students who are interested in exploring quantum software and games.
Do remember that this is just an Inspiration, so do experiment and create those awesome Quantum Games! 
Good luck!
