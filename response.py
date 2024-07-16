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
        with open(f'ilab_machines/{machine}.cs.rutgers.edu.json', 'r') as file:
            data = json.load(file)
            print(data)
            result_title = f'****{machine}****'
            embed = discord.Embed(title=result_title, color=8311585)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
            embed.add_field(name="Machine Name", value=data['name'], inline=True)
            embed.add_field(name="Room Number", value=data['room_number'], inline=True)
            embed.add_field(name="Host Status", value=data['host_status'], inline=True)
            embed.add_field(name="Last Check Time", value=data['last_check_time'], inline=True)
            embed.add_field(name="Next Schedule Active Check", value=data['next_schedule_active_check'], inline=True)
            embed.add_field(name="Is Scheduled Downtime", value=data['is_scheduled_downtime'], inline=True)
            embed.add_field(name="GPU Current Temp", value=data['gpu_current_temp'], inline=True)
            embed.add_field(name="GPU Fans Speed", value=data['gpu_fan_speed'], inline=True)
            embed.add_field(name="Connections", value=data['connections'], inline=True)
            embed.add_field(name="Load", value=data['load'], inline=True)
            embed.add_field(name="Ping", value=data['ping'], inline=True)
            embed.add_field(name="Packet Loss", value=data['packet_loss'], inline=True)
            embed.add_field(name="RTA", value=data['rta'], inline=True)
            embed.add_field(name="Root Disk", value=data['root_disk'], inline=True)
            embed.add_field(name="Smart Failed", value=data['smart_failed'], inline=True)
            embed.add_field(name="Smart Predicted", value=data['smart_predicted'], inline=True)
            embed.add_field(name="SSH", value=data['ssh'], inline=True)
            embed.add_field(name="VarDisk", value=data['vardisk'], inline=True)
            embed.add_field(name="X2GO", value=data['x2go'], inline=True)
            embed.set_footer(text="/status")
            await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
    else:
        result_title = f'**ERROR**'
        result_description = f'Machine Not Found'
        embed = discord.Embed(title=result_title, description=result_description, color=13632027)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Birthday-Bot says:")
        embed.set_footer(text="/status")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)