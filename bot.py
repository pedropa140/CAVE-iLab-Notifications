import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import schedule
import datetime

import response

load_dotenv()

def run_discord_bot():
    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.all()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    room_dictionary = {248: [
        "cd.cs.rutgers.edu",
        "cd.cs.rutgers.edu",
        "grep.cs.rutgers.edu",
        "kill.cs.rutgers.edu",
        "less.cs.rutgers.edu",
        "ls.cs.rutgers.edu",
        "man.cs.rutgers.edu",
        "pwd.cs.rutgers.edu",
        "rm.cs.rutgers.edu",
        "top.cs.rutgers.edu",
        "vi.cs.rutgers.edu"
    ], 252: [
        "assembly.cs.rutgers.edu",
        "basic.cs.rutgers.edu",
        "batch.cs.rutgers.edu",
        "cpp.cs.rutgers.edu",
        "java.cs.rutgers.edu",
        "lisp.cs.rutgers.edu",
        "pascal.cs.rutgers.edu",
        "perl.cs.rutgers.edu",
        "prolog.cs.rutgers.edu",
        "python.cs.rutgers.edu"
    ], 254: [
        "ice.cs.rutgers.edu",
        "snow.cs.rutgers.edu",
        "butter.cs.rutgers.edu",
        "cheese.cs.rutgers.edu",
        "candle.cs.rutgers.edu",
        "frost.cs.rutgers.edu",
        "popsicle.cs.rutgers.edu",
        "plastic.cs.rutgers.edu",
        "crayon.cs.rutgers.edu",
        "wax.cs.rutgers.edu"
    ]}
    
    @bot.event
    async def on_ready():
        try:
            synced = await bot.tree.sync()
            print(f'Synced {synced} command(s)')
            print(f'Synced {len(synced)} command(s)')            
            print(f'{bot.user} is now running!')
            bot.loop.create_task(roomchecks(bot))
            bot.loop.create_task(checkmachine(bot))
        except Exception as e:
            print(e)
        
    # on ready to do room checks every day from monday - thursday 1pm to 11pm and sunday 3pm to 11pm
    async def roomchecks(bot : commands.Bot):
        while True:
            if str(datetime.datetime.now().strftime('%H:%M')) == '13:24':
                print("ROOMCHECKS")

            await asyncio.sleep(60)

    # checks every 5 mins to see if a machine is down
    async def checkmachine(bot : commands.Bot):
        while True:
            print("STATUS")

            await asyncio.sleep(300)

    # status [ilab machine]
    @bot.tree.command(name = "status", description = "Get a Status of an iLab Machine.")
    @app_commands.describe(machine = "Enter iLab Machine Name (e.g. If you want to check batch.cs.rutgers.edu ... Enter batch)")
    async def status(interaction : discord.Interaction, machine : str):
        username = str(interaction.user)
        mention = str(interaction.user.mention)
        user_message = str(interaction.command.name)
        channel = str(interaction.channel)
        print(f'{username} ({mention}) said: "{user_message}" ({channel})')

        await response.status(interaction, machine, room_dictionary)

    bot.run(TOKEN)
    
