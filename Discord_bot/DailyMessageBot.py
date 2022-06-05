import discord
from discord.ext import commands
import yaml
import random
from datetime import datetime as dt
from discord.ext import tasks as discordTasks

with open('config.yaml', 'r') as file:
    configFile = yaml.safe_load(file)
TOKEN = configFile['token']
tasks = configFile['tasks']
#connect to discord 
client = discord.Client()
#set command prefix
client = commands.Bot(command_prefix='dmb ')
#users that will receive messages
users = []
numTasks = 2
hour = configFile['messageTime']['hour']
minutes = configFile['messageTime']['minutes']
blacklistedDays = [item.lower() for item in configFile['blacklistedDays']]
#--------Handles Events---------
@client.event
async def on_ready():
    print("Bot is ready.")    


#---------Handles Commands---------
@client.command()
async def ping(ctx):
    embed = discord.Embed(description = "pong")
    await ctx.send(embed = embed)

@client.command()
async def echo(ctx, *args):
    output = ''
    for word in args:
        output += word + ' '
    embed = discord.Embed(description = output)
    await ctx.send(embed = embed)

@client.command()
async def addUser(ctx, *newUsers):
    if len(newUsers) == 0:
        embed = discord.Embed(description = " -- Error: no users selects.")
        await ctx.send(embed = embed)
        return
    for user in newUsers:
        #remove extra parts of id, comes as <@!555>
        user = user.replace("<@!","")
        user = user.replace(">","")
        #get the user from the server and add to users array
        user = ctx.message.guild.get_member(int(user))
        users.append(user)
    reply = " -- User added." if len(newUsers) == 1 else " -- Users added."
    embed = discord.Embed(description = reply)
    await ctx.send(embed = embed)

@client.command()
async def testTasks(ctx):
    #if there are no users you cannot send tasks
    if len(users) == 0:
        embed = discord.Embed(description = " -- There are no users added.")
        await ctx.send(embed = embed)
        return
    await dmTasks()
    embed = discord.Embed(description = " -- DM's sent.")
    await ctx.send(embed = embed)


#sends each task in a list
@client.command()
async def viewTasks(ctx):
    embed = discord.Embed(title = "All tasks")
    #each list of items (each 'items' is an int from config)
    for items in tasks:
        allTasks = ''
        #access each item in the array associated with that int if there are any there
        if len(tasks[items]) > 0:
            for eachOptions in tasks[items]:
                # add each option to string if they exist
                allTasks += '\t' + eachOptions + '\n'
            embed.add_field(name=str(items), value=allTasks, inline=False)
    await ctx.send(embed = embed)
    
    
@client.command()
async def setNumTasks(ctx, num):
    global numTasks
    numTasks = int(num)
    embed = discord.Embed(description = " -- " +str(num) + " tasks will be send instead now.")
    await ctx.send(embed = embed)

@client.command()
async def getUsers(ctx):
    allUsers = ''
    if len(users) == 0:
        embed = discord.Embed(description = " -- There are currently no users.")
        await ctx.send(embed = embed)
        return
    for user in users:
        #remove extra parts of id, comes as <@!555>
        allUsers += str(user) + "\n"
    embed = discord.Embed(description = allUsers)
    await ctx.send(embed = embed)

@client.command()
async def removeUser(ctx, *removeUsers):
    if len(removeUsers) == 0:
        embed = discord.Embed(description = " -- Error: no users selects.")
        await ctx.send(embed = embed)
        return
    for user in removeUsers:
        #remove extra parts of id, comes as <@!555>
        user = user.replace("<@!","")
        user = user.replace(">","")
        #get the user from the server and remove from users array
        user = ctx.message.guild.get_member(int(user))
        users.remove(user)
    reply = " -- User removed." if len(removeUsers) == 1 else " -- Users removed."
    embed = discord.Embed(description = reply)
    await ctx.send(embed = embed)

@client.command()
async def addTask(ctx, weight, newTask):
    #validate input
    if not weight.isnumeric:
        embed = discord.Embed(description = "Error: first value must be an integer (qutations are not allowed)")
        await ctx.send(embed = embed)
        return
    #see if the weight exists then add accordingly
    global tasks
    if int(weight) in tasks:
        tasks[int(weight)].append(newTask)
    else:
        tasks[int(weight)] = [newTask]
    embed = discord.Embed(description = "-- Task added.")
    await ctx.send(embed = embed)

@client.command()
async def removeTask(ctx, removeTask):
    #validate input
    if (type(removeTask) != str):
        embed = discord.Embed(description = 'Error: second value must be an string (ex. "Read book").')
        await ctx.send(embed = embed)
        return
    global tasks
    for weight in tasks:
        if removeTask in tasks[weight]:
            tasks[weight].remove(removeTask)
            embed = discord.Embed(description = '-- Removed item from ' + str(weight) + ' weight class.')
            await ctx.send(embed = embed)
            return
    embed = discord.Embed(description = 'Error: task does not exists')
    await ctx.send(embed = embed)

@client.command()
async def setMessageTime(ctx, newTime):
    if not ":" in newTime:
        embed = discord.Embed(description = 'Error: time must be in hour:minutes and 24 hour format (ex. 20:35).')
        await ctx.send(embed = embed)
        return
    newHour = int(newTime.split(':')[0])
    newMinutes = int(newTime.split(':')[1])
    if newHour > 23 or newHour < 0:
        embed = discord.Embed(description = 'Error: invalid hour. Must be from 0 to 23')
        await ctx.send(embed = embed)
        return
    if newMinutes > 59 or newMinutes < 0:
        embed = discord.Embed(description = 'Error: invalid minutes. Must be from 0 to 59')
        await ctx.send(embed = embed)
        return
    global hour, minutes
    hour = newHour
    minutes = newMinutes
    embed = discord.Embed(description = ' -- Time set')
    await ctx.send(embed = embed)


@client.command()
async def viewMessageTime(ctx):
    embed = discord.Embed(description = 'Time set is ' + str(hour) + ":" + str(minutes))
    await ctx.send(embed = embed)

@client.command()
async def blockDays(ctx, *days):
    global blacklistedDays
    days = list(days)
    if len(days) < 1:
        embed = discord.Embed(description = "Error: no days were provided")
        await ctx.send(embed = embed)
        return
    possibleDays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for day in days:
        if not day.lower() in possibleDays:
            embed = discord.Embed(description = "Error: " + str(day) + " is not a valid day. Nothing added.")
            await ctx.send(embed = embed)
            return
        if day.lower() in blacklistedDays:
            embed = discord.Embed(description = str(day) + " is already black listed. It will be ignored")
            await ctx.send(embed = embed)
            days.remove(day.lower())
            
    if len(days) < 1:
        embed = discord.Embed(description = "Nothing else to do.")
        await ctx.send(embed = embed)

    for item in days:
        blacklistedDays.append(item)
    message = " -- Days added to blacklist" if len(days) > 1 else " -- Day added to blacklist."
    embed = discord.Embed(description = message)
    await ctx.send(embed = embed)

@client.command()
async def unblockDays(ctx, *days):
    global blacklistedDays
    days = list(days)
    if len(days) < 1:
        embed = discord.Embed(description = "Error: no days were provided")
        await ctx.send(embed = embed)
        return
    possibleDays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for day in days:
        if not day.lower() in possibleDays:
            embed = discord.Embed(description = "Error: " + str(day) + " is not a valid day. Nothing added.")
            await ctx.send(embed = embed)
            return
        if not day.lower() in blacklistedDays:
            embed = discord.Embed(description = str(day) + " is not black listed. It will be ignored")
            await ctx.send(embed = embed)
            days.remove(day.lower())
            
    if len(days) < 1:
        embed = discord.Embed(description = "Nothing else to do.")
        await ctx.send(embed = embed)

    for item in days:
        blacklistedDays.remove(item.lower())
    message = " -- Days removed from blacklist" if len(days) > 1 else " -- Day removed from blacklist."
    embed = discord.Embed(description = message)
    await ctx.send(embed = embed)

@client.command()
async def viewBlockedDays(ctx):
    global blacklistedDays
    message = "Days blocked:"
    i = len(blacklistedDays)
    for day in blacklistedDays:
        message += " " + day.capitalize()
        message += "," if i > 1 else "."
        i -= 1
    embed = discord.Embed(description = message)
    await ctx.send(embed = embed)


#---------General Functions---------
#randomly selects 'numTasks' number of tasks from yaml file, weighted
async def getRandomTasks():
    hat = []
    #each list of items (each 'items' is an int from config)
    for items in tasks:
        #access each item in the array associated with that int
        for eachOptions in tasks[items]:
            # add it to hat[] x = that int times
            for _ in range(items):
                hat.append(eachOptions)
    #randomly get distinct values from hat, numTasks is how many
    picks = []
    while (len(picks) < numTasks):
        ranChoice = random.choice(hat)
        if ranChoice not in picks:
            picks.append(ranChoice)
    return picks

async def dmTasks():
    todaysTasks = await getRandomTasks()
    todaysDate = await custom_strftime('%A, %B {S}.', dt.now())
    todaysMessage = "\n\nGoodmorning! Today is " + todaysDate + "\n" + "Here are your tasks for today!\n"
    itemCount = 1
    embed = discord.Embed(
        title = 'Tasks for ' + todaysDate,
        description = todaysMessage,
        color = 1752220
    )
    # add feild for each task
    for items in todaysTasks:
        embed.add_field(name="Task " + str(itemCount) + " ", value=items, inline=False)
        itemCount += 1
    #send message to each user  
    for user in users:
        await user.create_dm()
        await user.dm_channel.send(embed=embed)
   
#methods for getting suffix in date, ex "May 10th"
#decides what suffix to use
async def suffix(d):
        return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

#gets date and formats the string
async def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + await suffix(t.day))

#loop for sending message
@discordTasks.loop(minutes=1.0)
async def messageDaily():
    global blacklistedDays
    if dt.now().strftime('%A'). lower() in blacklistedDays:
        return
    if (dt.now().hour == hour) and (dt.now().strftime('%M') == str(minutes)):
        await dmTasks()

#TODO: save to config file
#TODO: better help function

messageDaily.start()
#run bot using token    
client.run(TOKEN)