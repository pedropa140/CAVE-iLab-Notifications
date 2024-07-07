'''
    Items to show:
        name of ilab machine
        room number
        host status
        last check time
        next schedule active check
        is scheduled downtime

        GPU Current Temp
        GPU Fan Speed
        Connections
        Load
        Ping
        Root Disk
        Smart Failed
        Smart Predicted
        ssh
        stats
        vardisk
        x2go
'''

import discord
from discord import app_commands
from discord.ext import commands
import datetime
import json        
import requests
from bs4 import BeautifulSoup

async def status(interaction : discord.Interaction, machine : str):
    def found(string : str):
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
        for room_number in room_dictionary:
            for machine in room_dictionary[room_number]:
                if string + ".cs.rutgers.edu" == machine:
                    return True
        
        return False

    def fetch_page_content(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()
            return page_text

        except requests.exceptions.RequestException as e:
            return f"Error fetching page content: {e}"


    if found(machine):
        print(f'https://report.cs.rutgers.edu/nagios4/cgi-bin/status.cgi?style=details&host={machine}.cs.rutgers.edu')
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