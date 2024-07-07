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
    
    @bot.event
    async def on_ready():
        try:
            synced = await bot.tree.sync()
            print(f'Synced {synced} command(s)')
            print(f'Synced {len(synced)} command(s)')            
            print(f'{bot.user} is now running!')
        except Exception as e:
            print(e)
        
    # on ready to do room checks every day from monday - thursday 1pm to 11pm and sunday 3pm to 11pm

    # checks every 5 mins to see if a machine is down

    # status [ilab machine]
    @bot.tree.command(name = "status", description = "Get a Status of an iLab Machine.")
    @app_commands.describe(machine = "Enter iLab Machine Name (e.g. If you want to check batch.cs.rutgers.edu ... Enter batch)")
    async def status(interaction : discord.Interaction, machine : str):
        username = str(interaction.user)
        mention = str(interaction.user.mention)
        user_message = str(interaction.command.name)
        channel = str(interaction.channel)
        print(f'{username} ({mention}) said: "{user_message}" ({channel})')

        await response.status(interaction, machine)

    bot.run(TOKEN)
    
