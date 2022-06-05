import os, sys
try:
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass

import discord, asyncio, re, json, time
from itertools import cycle
from datetime import datetime
from datetime import timedelta as timedelta
from discord.ext import commands, tasks

status = cycle(['$help for help!', 'Ping me for prefix!'])

def get_uptime():
    return round(time.time() - startTime)

@tasks.loop(minutes=5)
async def change_status():
    current_status = next(status)
    await client.change_presence(activity=discord.Game(name=current_status))

def get_prefix(client, message):
    if isinstance(message.channel, discord.channel.DMChannel):
        return "$"
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')

class Timer:
    def __init__(self):
        self.current_time = datetime.now()
        with open('json/reminderlist.json') as r:
            self.reminder_list = json.load(r)
        with open('json/remindertemplate.json') as t:
            self.reminder_template = json.load(t)

    def create(self, ctx, reminder, seconds, channel):
        authorid = ctx.author.id
        time_start = ctx.message.created_at
        message_id = ctx.message.id
        time_end = time_start + timedelta(0, seconds)
        self.reminder_template.update({"reminder": reminder,
            "time_start":time_start, "time_end":time_end,
            "authorid":ctx.author.id, "messageid":ctx.message.id,"channelid":channel})
        self.reminder_list.append(self.reminder_template.copy())
        with open('json/reminderlist.json', 'w') as f:
            json.dump(self.reminder_list, f, sort_keys=True,
                indent=2, separators=(',', ': '), default=str)
        self.task = asyncio.create_task(self.send_reminder(seconds,
            authorid, reminder, message_id, channel))

    def read_reminders(self):
        for s in range(len(self.reminder_list)):
            authorid = self.reminder_list[s]["authorid"]
            reminder = self.reminder_list[s]["reminder"]
            message_id = self.reminder_list[s]["messageid"]
            channel_id = self.reminder_list[s]["channelid"]
            time_start = datetime.strptime(
                self.reminder_list[s]["time_start"], '%Y-%m-%d %H:%M:%S.%f')
            time_end = datetime.strptime(
                self.reminder_list[s]["time_end"], '%Y-%m-%d %H:%M:%S.%f')
            seconds = (time_end - self.current_time).total_seconds()
            if(seconds <= 0):
                seconds = 1 + s
            asyncio.create_task(self.send_reminder(seconds, authorid, reminder,
                message_id, channel_id))

    async def send_reminder(self, seconds, authorid, reminder, messageid, channel_id, t=0):
        await asyncio.sleep(seconds)
        user = await client.fetch_user(authorid)
        with open('json/reminderlist.json') as r:
            reminder_list = json.load(r)
        embed = discord.Embed(title="Reminder!",
        description="\"{}\"".format(reminder), color=0x34a1eb)
        embed.set_footer(text="This is a reminder that you set!")
        if(channel_id == None):
            await user.send(embed=embed)
        else:
            print(channel_id)
            channel = client.get_channel(channel_id)
            await channel.send(embed=embed)
        for s in range(len(reminder_list)):
            if reminder_list[s]["messageid"] == messageid:
                reminder_list.pop(s)
                with open("json/reminderlist.json", "w") as f:
                    json.dump(reminder_list, f, sort_keys=True,
                        indent=2, separators=(',', ': '), default=str)

async def embed_send(ctx, title, description, err=False):
    colors = 0xc000000 if err else 0x80f000
    if err:
        colors = 0xc00000
    else:
        colors = 0x80f000
    embed = discord.Embed(description="{}".format(description),
        title=title, color=colors)
    embed.set_footer(text="Command sent by {}".format(ctx.message.author),
        icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)


def unit_getter(unit):
    if unit in ["s", "sec", "secs", "second", "seconds"]:
        return 1, "second"
    if unit in ["m", "min", "mins", "minute", "minutes"]:
        return 60, "minute"
    if unit in ["h", "hr", "hrs", "hour", "hours"]:
        return 3600, "hour"
    if unit in ["d", "day", "days"]:
        return 86_000, "day"
    if unit in ["w", "wk", "wks", "week", "weeks"]:
        return 604_800, "week"
    if unit in ["mth", "mths", "mos", "month", "months"]:
        return 2_580_000, "month"
    if unit in ["y", "yr", "yrs", "year", "years"]:
        return 31_390_000, "month"
    else:
        return None, None

@client.event
async def on_command_error(ctx, error):
    print('{}: {}\n{}\n'.format(ctx.message.author, ctx.message.content, error))
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await embed_send(ctx, "Error!",'That command doesn\'t exist!', 0xFF3232)
    elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await embed_send(ctx,"Error!",'Missing arguments in command!', 0xFF3232)
    elif isinstance(error, discord.ext.commands.MissingPermissions):
        await embed_send(ctx, "Error!",
            'You don\'t have permission(s) "{}" to do that command!' \
            .format(','.join(error.missing_perms)), 0xFF3232)
    elif isinstance(error, discord.ext.commands.NoPrivateMessage):
        await embed_send(ctx, "Error!",
            'You can\'t run this command in a private message!', 0xFF3232)
    else:
        pass

@client.event
async def on_guild_join(guild):
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "$"
    with open("json/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=2)

@client.event
async def on_guild_remove(guild):
    try:
        with open("json/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open("json/prefixes.json", "w") as f:
            json.dump(prefixes, f, sort_keys=True, indent=2)
    except:
        pass

@client.event
async def on_ready():
    global startTime
    change_status.start()
    startTime = time.time()
    t = Timer()
    t.read_reminders()
    print('Ready!')

@client.event
async def on_message(message):
    if (message.author.bot == True):
        return
    if (message.mention_everyone == True):
        return
    if client.user.mentioned_in(message):
        try:
            get_prefix(client, message)
        except:
            with open("json/prefixes.json", "r") as f:
                prefixes = json.load(f)
            prefixes[str(message.guild.id)] = "$"
            with open("json/prefixes.json", "w") as f:
                json.dump(prefixes, f, indent=2)
        embed = discord.Embed(
            title="Pinged!",
            description="The set prefix is ``{}``".format(get_prefix(client,
            message)),
            color=0x00FF40,
        )
        embed.set_footer(
            text="Command sent by {}".format(message.author),
            icon_url=message.author.avatar_url,
        )
        await message.channel.send(embed=embed)

    try:
        await client.process_commands(message)
    except:
        with open("json/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(message.guild.id)] = "$"
        with open("json/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=2)
        await client.process_commands(message)

@client.command(pass_context=True, aliases=["remind", "r"])
async def remindme(ctx, *args):
    reversed_args = reversed(args)
    channel_id = None
    unit_name_list = []
    seconds_list = []
    name_list = []
    seconds = 0
    index = 0
    reminder = ""
    for x in reversed_args:
        if(reminder != ""):
            reminder = x + " " + reminder
            continue
        try:
            reg = re.compile("([0-9]+)([a-zA-Z]+)")
            time, unit = reg.match(x).groups()
            unit_time, unit_name = unit_getter(unit.lower())
        except Exception as e:
            if(index != 0):
                reminder = x + " " + reminder
                continue
            else:
                try:
                    temp = re.findall(r'\d+', x)
                    res = list(map(int, temp))
                    if (client.get_channel(res[0]) != None):
                        channel_id = res[0]
                        channel = client.get_channel(res[0])
                        client_member = ctx.guild.get_member(client.user.id)
                        check1 = channel.permissions_for(ctx.author)
                        check2 = channel.permissions_for(client_member)
                        if(check1.send_messages == False):
                            await embed_send(ctx, "Error!", "You don't have permissions to send messages to that channel!", True)
                            return
                        if(check2.send_messages == False):
                            await embed_send(ctx, "Error", "Bot doesn't have permissions to send messages to that channel!", True)
                            return
                        index += 1
                        continue
                    else:
                        await embed_send(ctx, "Error!", "Invalid channel!", True)
                        return

                except:
                    await embed_send(ctx, "Error!", "Invalid command format!", True)
                    return
            await embed_send(ctx, "Error!", "Invalid command format!", True)
            return
        if(unit_name == None):
            await embed_send(ctx, "Error", "Invalid unit(s)\n**Supported units: **Seconds, minutes, hours, days, weeks, months, years", True)
            return
        elif(int(time) <= 0):
            await embed_send(ctx, "Error!", "Invalid time!", True)
            return
        elif unit_name in unit_name_list:
            await embed_send(ctx, "Error!", "Duplicate unit!", True)
            return
        unit_name_list.append(unit_name)
        if(int(time) != 1):
            unit_name += "s"
        seconds_list.append(time)
        seconds += unit_time * int(time)
        x = time + " " + unit_name
        name_list.append(x)
        index += 1
    if(reminder == ""):
        await embed_send(ctx, "Error!", "Reminder missing!", True)
        return
    if(name_list == []):
        await embed_send(ctx, "Error!", "Duration missing!", True)
        return
    name_list.reverse()
    t = Timer()
    t.create(ctx, reminder.rstrip(), seconds, channel_id)
    if(channel_id == None):
        await embed_send(ctx, "Reminder set!",
            "Reminder added for \"{}\" for {}\n**Note:** Make sure your DM's are enabled!".format(reminder.rstrip(),
            ", ".join(name_list)))
    else:
        await embed_send(ctx, "Reminder set!",
            "Reminder added for \"{}\" for {}, in <#{}>".format(reminder.rstrip(),
            ", ".join(name_list), channel_id))

@client.command(aliases=["prefix"])
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def setprefix(ctx, prefix):
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    if (prefixes[str(ctx.guild.id)]) == prefix:
        await embed_send(
            ctx, "Error!", 'Prefix is already ``{}``'.format(prefix), 0xFF3232
        )
        return
    prefixes[str(ctx.guild.id)] = prefix
    with open("json/prefixes.json", "w") as f:
        json.dump(prefixes, f, sort_keys=True, indent=2)
    await embed_send(ctx, "Prefix set!", 'Prefix set to ``{}``'.format(prefix))

@client.command(aliases=["h", "command", "commands"])
async def help(ctx):
    embed = discord.Embed(title="Help:", color=0x00FF40)
    with open("json/commands.json", "r") as f:
        commands = json.load(f)
    for key, value in commands.items():
        embed.add_field(name=key, value=value, inline=False)
    embed.set_author(name="Reminder Friend!")
    embed.set_footer(
        text="Command sent by {}".format(ctx.author),
        icon_url=ctx.author.avatar_url,
    )
    await ctx.send(embed=embed)

@client.command(aliases=["ping"])
async def info(ctx):
    embed=discord.Embed(title='Info:', color=0x00FF40)
    embed.add_field(name="Invite this bot!", value=
"[**Invite**](https://discord.com/oauth2/authorize?client_id=812140712803827742&permissions=2048&scope=bot)", inline=False)
    embed.add_field(name="Join support server!", value="[**Support Server**](https://discord.gg/Uk6fg39cWn)", inline=False)
    embed.add_field(name='Bot Creator:',
        value=\
        '[DoggieLicc](https://github.com/DoggieLicc/ReminderFriend)#1641',
        inline=True)
    embed.add_field(name='Bot Uptime:',
        value='{} seconds'.format(get_uptime()), inline=False)
    embed.add_field(name='Ping:',
        value='{} ms'.format(round(1000*(client.latency)), inline=False))
    embed.set_footer(text=f"Command sent by {ctx.message.author}",
        icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def dev(ctx, *args):
    if(ctx.message.author.id != 203161760297910273):
        return
    if(args[0] == "prefix"):
        with open("json/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = args[1]
        with open("json/prefixes.json", "w") as f:
            json.dump(prefixes, f, sort_keys=True, indent=2)
        await embed_send(ctx, "Prefix set!", f'Prefix set to ``{args[1]}``')


client.run("OTgzMDA3NDI4NDUyOTcwNTI4.Gg71E-.KqCHsn2RfptlgStlyLMAVYfQRAAEqAk5wWyz2k")

TOKEN = OTgzMDA3NDI4NDUyOTcwNTI4.Gg71E-.KqCHsn2RfptlgStlyLMAVYfQRAAEqAk5wWyz2k
# Activates the bot.
client.run(TOKEN)
