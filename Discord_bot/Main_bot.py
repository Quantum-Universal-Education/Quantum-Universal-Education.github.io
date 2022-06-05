import discord
import random

TOKEN = "insert token here"

client = discord.Client()


# Provides a confirmation of the activation of the bot.
@client.event
async def on_ready(message):
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} - {channel}")  # This will log the messages in the server.


    if message.author == client.user:  # Stops the bot from endlessly replying to itself.
        return

    if message.channel.name == 'chatbot-test':
        if user_message.lower() == 'hello':
            await message.channel.send(f"Hello {username}")
            return
        elif user_message.lower() == 'bye':
            await message.channel.send(f"See you later, {username}")
            return
        elif user_message.lower() == '!random':
            response = f'This is your random number: {random.random()}'
            await message.channel.send(response)

    if user_message.lower() == "anywhere":
        await message.channel.send("This message can be seen anywhere.")
        return


# Activates the bot.
client.run(TOKEN)
