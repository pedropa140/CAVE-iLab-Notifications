import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import schedule
import datetime
import json

import response
import webscraper
from ilabmachine import IlabMachine

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
    session_type = 0 # 0 - regular session | 1 - summer session | 2 - no session
    
    @bot.event
    async def on_ready():
        try:
            synced = await bot.tree.sync()
            print(f'Synced {synced} command(s)')
            print(f'Synced {len(synced)} command(s)')            
            print(f'{bot.user} is now running!')
            bot.loop.create_task(checkmachine(bot))
            bot.loop.create_task(roomchecks(bot))
        except Exception as e:
            print(e)
        
    async def roomchecks(bot : commands.Bot):
        while True:
            current_datetime = datetime.datetime.now()
            current_date = current_datetime.strftime('%A')
            current_time = current_datetime.strftime('%H:%M')
            downmachines = []
            if session_type == 0:
                if current_date == 'Monday' or current_date == 'Tuesday' or current_date == 'Wednesday' or current_date == 'Thursday':
                    if current_time == '13:00' or current_time == '23:00':
                        for room in room_dictionary:
                            for machine in room_dictionary[room]:
                                with open(f'ilab_machines/{machine}.txt', 'r') as file:
                                    data = json.load(file)
                                    if data['host_status'].lower() != 'up':
                                        downmachines.append((machine, data))
                        if len(downmachines) > 0:
                            for machine in downmachines:
                                result_title = f'**MACHINE MAY BE DOWN**'
                                result_description = f'**{machine[0]}**\'s status is currently down.'
                                embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                                file = discord.File('images/icon.png', filename='icon.png')
                                embed.set_thumbnail(url='attachment://icon.png')
                                embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                                embed.add_field(name="Machine Name", value=machine[1]['name'], inline=False)
                                embed.add_field(name="Room Number", value=machine[1]['room_number'], inline=False)
                                embed.add_field(name="Host Status", value=machine[1]['host_status'], inline=False)
                                embed.add_field(name="Last Check Time", value=machine[1]['last_check_time'], inline=False)
                                embed.add_field(name="Next Schedule Active Check", value=machine[1]['next_schedule_active_check'], inline=False)
                                embed.add_field(name="Is Scheduled Downtime", value=machine[1]['is_scheduled_downtime'], inline=False)
                                embed.add_field(name="GPU Current Temp", value=machine[1]['gpu_current_temp'], inline=False)
                                embed.add_field(name="GPU Fans Speed", value=machine[1]['gpu_fan_speed'], inline=False)
                                embed.add_field(name="Connections", value=machine[1]['connections'], inline=False)
                                embed.add_field(name="Load", value=machine[1]['load'], inline=False)
                                embed.add_field(name="Ping", value=machine[1]['ping'], inline=False)
                                embed.add_field(name="Packet Loss", value=machine[1]['packet_loss'], inline=False)
                                embed.add_field(name="RTA", value=machine[1]['rta'], inline=False)
                                embed.add_field(name="Root Disk", value=machine[1]['root_disk'], inline=False)
                                embed.add_field(name="Smart Failed", value=machine[1]['smart_failed'], inline=False)
                                embed.add_field(name="Smart Predicted", value=machine[1]['smart_predicted'], inline=False)
                                embed.add_field(name="SSH", value=machine[1]['ssh'], inline=False)
                                embed.add_field(name="VarDisk", value=machine[1]['vardisk'], inline=False)
                                embed.add_field(name="X2GO", value=machine[1]['x2go'], inline=False)

                                embed.set_footer(text="/roomchecks")
                                for guild in bot.guilds:
                                    for channel in guild.channels:
                                        if channel.name.lower() == 'cave-roomchecks-bot' and str(channel.type).lower() == 'text':
                                            send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                            await send_message.send(file=file, embed=embed)
                        else:
                            result_title = f'**ALL MACHINES ARE UP AND RUNNING**'
                            embed = discord.Embed(title=result_title, color=8311585)
                            file = discord.File('images/icon.png', filename='icon.png')
                            embed.set_thumbnail(url='attachment://icon.png')
                            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                            embed.set_footer(text="/roomchecks")
                            for guild in bot.guilds:
                                for channel in guild.channels:
                                    if channel.name.lower() == 'cave-roomchecks-bot' and str(channel.type).lower() == 'text':
                                        send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                        await send_message.send(file=file, embed=embed)
                elif current_date == 'Friday':
                    if current_time == '13:00' or current_time == '18:00':
                        for room in room_dictionary:
                            for machine in room_dictionary[room]:
                                with open(f'ilab_machines/{machine}.txt', 'r') as file:
                                    data = json.load(file)
                                    if data['host_status'].lower() != 'up':
                                        downmachines.append((machine, data))
                        if len(downmachines) > 0:
                            for machine in downmachines:
                                result_title = f'**MACHINE MAY BE DOWN**'
                                result_description = f'**{machine[0]}**\'s status is currently down.'
                                embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                                file = discord.File('images/icon.png', filename='icon.png')
                                embed.set_thumbnail(url='attachment://icon.png')
                                embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                                embed.add_field(name="Machine Name", value=machine[1]['name'], inline=False)
                                embed.add_field(name="Room Number", value=machine[1]['room_number'], inline=False)
                                embed.add_field(name="Host Status", value=machine[1]['host_status'], inline=False)
                                embed.add_field(name="Last Check Time", value=machine[1]['last_check_time'], inline=False)
                                embed.add_field(name="Next Schedule Active Check", value=machine[1]['next_schedule_active_check'], inline=False)
                                embed.add_field(name="Is Scheduled Downtime", value=machine[1]['is_scheduled_downtime'], inline=False)
                                embed.add_field(name="GPU Current Temp", value=machine[1]['gpu_current_temp'], inline=False)
                                embed.add_field(name="GPU Fans Speed", value=machine[1]['gpu_fan_speed'], inline=False)
                                embed.add_field(name="Connections", value=machine[1]['connections'], inline=False)
                                embed.add_field(name="Load", value=machine[1]['load'], inline=False)
                                embed.add_field(name="Ping", value=machine[1]['ping'], inline=False)
                                embed.add_field(name="Packet Loss", value=machine[1]['packet_loss'], inline=False)
                                embed.add_field(name="RTA", value=machine[1]['rta'], inline=False)
                                embed.add_field(name="Root Disk", value=machine[1]['root_disk'], inline=False)
                                embed.add_field(name="Smart Failed", value=machine[1]['smart_failed'], inline=False)
                                embed.add_field(name="Smart Predicted", value=machine[1]['smart_predicted'], inline=False)
                                embed.add_field(name="SSH", value=machine[1]['ssh'], inline=False)
                                embed.add_field(name="VarDisk", value=machine[1]['vardisk'], inline=False)
                                embed.add_field(name="X2GO", value=machine[1]['x2go'], inline=False)

                                embed.set_footer(text="/roomchecks")
                                for guild in bot.guilds:
                                    for channel in guild.channels:
                                        if channel.name.lower() == 'cave-roomchecks-bot' and str(channel.type).lower() == 'text':
                                            send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                            await send_message.send(file=file, embed=embed)
                        else:
                            result_title = f'**ALL MACHINES ARE UP AND RUNNING**'
                            embed = discord.Embed(title=result_title, color=8311585)
                            file = discord.File('images/icon.png', filename='icon.png')
                            embed.set_thumbnail(url='attachment://icon.png')
                            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                            embed.set_footer(text="/roomchecks")
                            for guild in bot.guilds:
                                for channel in guild.channels:
                                    if channel.name.lower() == 'cave-roomchecks-bot' and str(channel.type).lower() == 'text':
                                        send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                        await send_message.send(file=file, embed=embed)
                elif current_date == 'Sunday':
                    if current_time == '15:00' or current_time == '23:00':
                        for room in room_dictionary:
                            for machine in room_dictionary[room]:
                                with open(f'ilab_machines/{machine}.txt', 'r') as file:
                                    data = json.load(file)
                                    if data['host_status'].lower() != 'up':
                                        downmachines.append((machine, data))
                        if len(downmachines) > 0:
                            for machine in downmachines:
                                result_title = f'**MACHINE MAY BE DOWN**'
                                result_description = f'**{machine[0]}**\'s status is currently down.'
                                embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                                file = discord.File('images/icon.png', filename='icon.png')
                                embed.set_thumbnail(url='attachment://icon.png')
                                embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                                embed.add_field(name="Machine Name", value=machine[1]['name'], inline=False)
                                embed.add_field(name="Room Number", value=machine[1]['room_number'], inline=False)
                                embed.add_field(name="Host Status", value=machine[1]['host_status'], inline=False)
                                embed.add_field(name="Last Check Time", value=machine[1]['last_check_time'], inline=False)
                                embed.add_field(name="Next Schedule Active Check", value=machine[1]['next_schedule_active_check'], inline=False)
                                embed.add_field(name="Is Scheduled Downtime", value=machine[1]['is_scheduled_downtime'], inline=False)
                                embed.add_field(name="GPU Current Temp", value=machine[1]['gpu_current_temp'], inline=False)
                                embed.add_field(name="GPU Fans Speed", value=machine[1]['gpu_fan_speed'], inline=False)
                                embed.add_field(name="Connections", value=machine[1]['connections'], inline=False)
                                embed.add_field(name="Load", value=machine[1]['load'], inline=False)
                                embed.add_field(name="Ping", value=machine[1]['ping'], inline=False)
                                embed.add_field(name="Packet Loss", value=machine[1]['packet_loss'], inline=False)
                                embed.add_field(name="RTA", value=machine[1]['rta'], inline=False)
                                embed.add_field(name="Root Disk", value=machine[1]['root_disk'], inline=False)
                                embed.add_field(name="Smart Failed", value=machine[1]['smart_failed'], inline=False)
                                embed.add_field(name="Smart Predicted", value=machine[1]['smart_predicted'], inline=False)
                                embed.add_field(name="SSH", value=machine[1]['ssh'], inline=False)
                                embed.add_field(name="VarDisk", value=machine[1]['vardisk'], inline=False)
                                embed.add_field(name="X2GO", value=machine[1]['x2go'], inline=False)

                                embed.set_footer(text="/roomchecks")
                                for guild in bot.guilds:
                                    for channel in guild.channels:
                                        if channel.name.lower() == 'cave-roomchecks-bot' and str(channel.type).lower() == 'text':
                                            send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                            await send_message.send(file=file, embed=embed)
                        else:
                            result_title = f'**ALL MACHINES ARE UP AND RUNNING**'
                            embed = discord.Embed(title=result_title, color=8311585)
                            file = discord.File('images/icon.png', filename='icon.png')
                            embed.set_thumbnail(url='attachment://icon.png')
                            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                            embed.set_footer(text="/roomchecks")
                            for guild in bot.guilds:
                                for channel in guild.channels:
                                    if channel.name.lower() == 'cave-roomchecks-bot' and str(channel.type).lower() == 'text':
                                        send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                        await send_message.send(file=file, embed=embed)
            elif session_type == 1:
                if current_date == 'Monday' or current_date == 'Tuesday' or current_date == 'Wednesday' or current_date == 'Thursday':
                    if current_time == '13:00' or current_time == '18:00':
                        for room in room_dictionary:
                            for machine in room_dictionary[room]:
                                with open(f'ilab_machines/{machine}.txt', 'r') as file:
                                    data = json.load(file)
                                    if data['host_status'].lower() != 'up':
                                        downmachines.append((machine, data))
                        if len(downmachines) > 0:
                            for machine in downmachines:
                                result_title = f'**MACHINE MAY BE DOWN**'
                                result_description = f'**{machine[0]}**\'s status is currently down.'
                                embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                                file = discord.File('images/icon.png', filename='icon.png')
                                embed.set_thumbnail(url='attachment://icon.png')
                                embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                                embed.add_field(name="Machine Name", value=machine[1]['name'], inline=False)
                                embed.add_field(name="Room Number", value=machine[1]['room_number'], inline=False)
                                embed.add_field(name="Host Status", value=machine[1]['host_status'], inline=False)
                                embed.add_field(name="Last Check Time", value=machine[1]['last_check_time'], inline=False)
                                embed.add_field(name="Next Schedule Active Check", value=machine[1]['next_schedule_active_check'], inline=False)
                                embed.add_field(name="Is Scheduled Downtime", value=machine[1]['is_scheduled_downtime'], inline=False)
                                embed.add_field(name="GPU Current Temp", value=machine[1]['gpu_current_temp'], inline=False)
                                embed.add_field(name="GPU Fans Speed", value=machine[1]['gpu_fan_speed'], inline=False)
                                embed.add_field(name="Connections", value=machine[1]['connections'], inline=False)
                                embed.add_field(name="Load", value=machine[1]['load'], inline=False)
                                embed.add_field(name="Ping", value=machine[1]['ping'], inline=False)
                                embed.add_field(name="Packet Loss", value=machine[1]['packet_loss'], inline=False)
                                embed.add_field(name="RTA", value=machine[1]['rta'], inline=False)
                                embed.add_field(name="Root Disk", value=machine[1]['root_disk'], inline=False)
                                embed.add_field(name="Smart Failed", value=machine[1]['smart_failed'], inline=False)
                                embed.add_field(name="Smart Predicted", value=machine[1]['smart_predicted'], inline=False)
                                embed.add_field(name="SSH", value=machine[1]['ssh'], inline=False)
                                embed.add_field(name="VarDisk", value=machine[1]['vardisk'], inline=False)
                                embed.add_field(name="X2GO", value=machine[1]['x2go'], inline=False)

                                embed.set_footer(text="/roomchecks")
                                for guild in bot.guilds:
                                    for channel in guild.channels:
                                        if channel.name.lower() == 'cave-roomchecks-bot' and str(channel.type).lower() == 'text':
                                            send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                            await send_message.send(file=file, embed=embed)
                        else:
                            result_title = f'**ALL MACHINES ARE UP AND RUNNING**'
                            embed = discord.Embed(title=result_title, color=8311585)
                            file = discord.File('images/icon.png', filename='icon.png')
                            embed.set_thumbnail(url='attachment://icon.png')
                            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                            embed.set_footer(text="/roomchecks")
                            for guild in bot.guilds:
                                for channel in guild.channels:
                                    if channel.name.lower() == 'cave-roomchecks-bot' and str(channel.type).lower() == 'text':
                                        send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                        await send_message.send(file=file, embed=embed)
            elif session_type == 2:
                continue
            
            await asyncio.sleep(60)

    async def checkmachine(bot : commands.Bot):
        history_dictionary = {}
        for room in room_dictionary:
            for machine in room_dictionary[room]:
                if machine not in history_dictionary:
                    history_dictionary[machine] = {'status': 'UP'}
        print(history_dictionary)
        while True:
            for room in room_dictionary:
                for machine in room_dictionary[room]:
                    url = f"https://report.cs.rutgers.edu/nagios4/cgi-bin/status.cgi?style=details&host={machine}"
                    page_text = webscraper.fetch_page_content(url).strip('\n')
                    webscraper.write_to_file(f"{machine}.txt", page_text)
                    current_network_status_output = webscraper.current_network_status(f'{machine}.txt', machine)
                    os.remove(f'{machine}.txt')

                    url = f"https://report.cs.rutgers.edu/nagios4/cgi-bin/extinfo.cgi?type=1&host={machine}"
                    page_text = webscraper.fetch_page_content(url).strip('\n')
                    webscraper.write_to_file(f"{machine}.txt", page_text)
                    extended_information_output = webscraper.extended_information(f'{machine}.txt', machine)
                    os.remove(f'{machine}.txt')

                    ilab_machine = IlabMachine(machine, room, extended_information_output[0], current_network_status_output[0],
                                            extended_information_output[1], extended_information_output[2], current_network_status_output[1],
                                            current_network_status_output[2], current_network_status_output[3], current_network_status_output[4],
                                            current_network_status_output[5], current_network_status_output[6], current_network_status_output[7],
                                            current_network_status_output[8], current_network_status_output[9], current_network_status_output[10],
                                            current_network_status_output[11], current_network_status_output[12], current_network_status_output[13])

                    ilab_machine.to_json()
                    if ilab_machine.host_status.lower() != 'up':
                        if history_dictionary[machine]['status'].lower() != 'down':
                            result_title = f'**MACHINE MAY BE DOWN**'
                            result_description = f'**{machine[0]}**\'s status is currently down.'
                            embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                            file = discord.File('images/icon.png', filename='icon.png')
                            embed.set_thumbnail(url='attachment://icon.png')
                            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                            embed.add_field(name="Machine Name", value= ilab_machine.name, inline=False)
                            embed.add_field(name="Room Number", value= ilab_machine.room_number, inline=False)
                            embed.add_field(name="Host Status", value= ilab_machine.host_status, inline=False)
                            embed.add_field(name="Last Check Time", value= ilab_machine.last_check_time, inline=False)
                            embed.add_field(name="Next Schedule Active Check", value= ilab_machine.next_schedule_active_check, inline=False)
                            embed.add_field(name="Is Scheduled Downtime", value= ilab_machine.is_scheduled_downtime, inline=False)
                            embed.add_field(name="GPU Current Temp", value= ilab_machine.gpu_current_temp, inline=False)
                            embed.add_field(name="GPU Fans Speed", value= ilab_machine.gpu_fan_speed, inline=False)
                            embed.add_field(name="Connections", value= ilab_machine.connections, inline=False)
                            embed.add_field(name="Load", value= ilab_machine.load, inline=False)
                            embed.add_field(name="Ping", value= ilab_machine.ping, inline=False)
                            embed.add_field(name="Packet Loss", value= ilab_machine.packet_loss, inline=False)
                            embed.add_field(name="RTA", value= ilab_machine.rta, inline=False)
                            embed.add_field(name="Root Disk", value= ilab_machine.root_disk, inline=False)
                            embed.add_field(name="Smart Failed", value= ilab_machine.smart_failed, inline=False)
                            embed.add_field(name="Smart Predicted", value= ilab_machine.smart_predicted, inline=False)
                            embed.add_field(name="SSH", value= ilab_machine.ssh, inline=False)
                            embed.add_field(name="VarDisk", value= ilab_machine.vardisk, inline=False)
                            embed.add_field(name="X2GO", value= ilab_machine.x2go, inline=False)
                            embed.set_footer(text="/checkmachine")
                            for guild in bot.guilds:
                                for channel in guild.channels:
                                    if channel.name.lower() == 'cave-roomchecks-bot' and str(channel.type).lower() == 'text':
                                        send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                        await send_message.send(file=file, embed=embed)
                            history_dictionary[machine]['status'] = 'DOWN'
                        else:
                            continue


            await asyncio.sleep(300)

    @bot.tree.command(name = "status", description = "Get a Status of an iLab Machine.")
    @app_commands.describe(machine = "Enter iLab Machine Name (e.g. If you want to check batch.cs.rutgers.edu ... Enter batch)")
    async def status(interaction : discord.Interaction, machine : str):
        username = str(interaction.user)
        mention = str(interaction.user.mention)
        user_message = str(interaction.command.name)
        channel = str(interaction.channel)
        print(f'{username} ({mention}) said: "{user_message}" ({channel})')

        await response.status(interaction, machine, room_dictionary)

    @bot.tree.command(name = "changesession", description = "Change session on how the bot pings everyone.")
    @app_commands.describe(user_input_session = "Enter [regular] or [summer] or [break]")
    async def changesession(interaction : discord.Interaction, user_input_session : str):
        username = str(interaction.user)
        mention = str(interaction.user.mention)
        user_message = str(interaction.command.name)
        channel = str(interaction.channel)
        print(f'{username} ({mention}) said: "{user_message}" ({channel})')

        await response.changesession(interaction, user_input_session)

    bot.run(TOKEN)
    
