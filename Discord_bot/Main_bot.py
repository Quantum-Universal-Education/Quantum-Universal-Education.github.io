import discord
from discord.ext import commands

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

TOKEN = OTgzMDA3NDI4NDUyOTcwNTI4.Gg71E-.KqCHsn2RfptlgStlyLMAVYfQRAAEqAk5wWyz2k
client = discord.Client()

class Scheduler(commands.Cog):
    """Schedule commands."""
    def __init__(self, bot):
        self.bot = bot

        # Initialize session
        self.session = aiohttp.ClientSession()
    
    # Scheduled events
    async def schedule_func(self):

    def schedule(self):
        # Initialize scheduler
        schedule_log = logging.getLogger("apscheduler")
        schedule_log.setLevel(logging.WARNING)

        job_defaults = {
            "coalesce": True,
            "max_instances": 5,
            "misfire_grace_time": 15,
            "replace_existing": True,
        }

        scheduler = AsyncIOScheduler(job_defaults = job_defaults, 
                          logger = schedule_log)

        # Add jobs to scheduler
        scheduler.add_job(self.schedule_func, CronTrigger.from_crontab("0 * * * *")) 
        # Every hour

    
@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} - {channel}")  # This will log the messages in the server.

    scheduler = schedule_jobs.Scheduler(bot).schedule()
    scheduler.start()

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
