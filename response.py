import discord
from discord import app_commands
from discord.ext import commands
import datetime
import json        
import requests
from bs4 import BeautifulSoup

async def status(interaction : discord.Interaction, machine : str, room_dictionary : dict):
    def found(string : str):
        for room_number in room_dictionary:
            for machine in room_dictionary[room_number]:
                if string + ".cs.rutgers.edu" == machine:
                    return True
        
        return False

    if found(machine):
        result_title = f'**SUCCESS**'
        result_description = f'Machine Found'
        embed = discord.Embed(title=result_title, description=result_description, color=8311585)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Birthday-Bot says:")
        embed.set_footer(text="/status")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=False)
    else:
        result_title = f'**ERROR**'
        result_description = f'Machine Not Found'
        embed = discord.Embed(title=result_title, description=result_description, color=13632027)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Birthday-Bot says:")
        embed.set_footer(text="/status")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)

async def changesession(interaction : discord.Interaction, user_input_session : str):
    return NotImplementedError