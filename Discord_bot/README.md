# Discord Quantum Bot
## Instructions
1) Create an app at https://discord.com/developers/applications
2) Add a bot to the app through discord (see left side of the screen options)
3) Download this code
4) Copy the bot's token and replace the: YOUR_TOKEN_HERE in line 2 of config.yaml
5) This bot is designed to send messages every day at 9am. If you would like to reconfigure this to a different time change lines 12 & 13 of config.yaml.
6) Sundays the bot "sleeps", if you would like to blacklist any other day or to send a message every day add/delete desired blacklisted days in line 15 of config.yaml
7) Messages are weighted by desired frequency. To writte message reminders of frequency (4-1), with 4 being the most frequent messages, please insert your desired message in lines 6-9 of config.yaml. For example:
   Change 4: ["Common Example", "Another common example"] -> to 4:["Remember to work on your Quantum skills today!"]
8) Run the program and activate the bot
