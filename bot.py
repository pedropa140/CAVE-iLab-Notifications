import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import schedule
import datetime
import json
import time
import response
import webscraper
from ilabmachine import IlabMachine

load_dotenv()

session_type = "regular"

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
            bot.loop.create_task(checkmachine(bot))
            time.sleep(5)
            bot.loop.create_task(roomchecks(bot))
        except Exception as e:
            print(e)
        
    async def roomchecks(bot : commands.Bot):
        room_checks_done = False
        downmachines = []
        while True:  
            date = datetime.datetime.now()
            current_time = date.strftime('%H:%M')
            current_day = date.strftime('%A')

            if session_type == 'regular':
                if current_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday']:
                    if (current_time in ['13:00', ['23:00']] and not room_checks_done):
                    # if current_time == current_time and not room_checks_done:
                        for room in room_dictionary:
                            for machine in room_dictionary[room]:
                                with open(f'ilab_machines/{machine}.json', 'r') as file:
                                    data = json.load(file)
                                    if data['host_status'].lower() != 'up':
                                        downmachines.append((machine, data))
                        if len(downmachines) > 0:
                            for machine in downmachines:
                                result_title = f'**Machine may be down.**'
                                result_description = f'({current_day} {current_time}) - **{machine[0]}**\'s status is currently down.'
                                embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                                embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                                embed.add_field(name="Machine Name", value=machine[1]['name'], inline=True)
                                embed.add_field(name="Room Number", value=machine[1]['room_number'], inline=True)
                                embed.add_field(name="Host Status", value=machine[1]['host_status'], inline=True)
                                embed.add_field(name="Last Check Time", value=machine[1]['last_check_time'], inline=True)
                                embed.add_field(name="Next Schedule Active Check", value=machine[1]['next_schedule_active_check'], inline=True)
                                embed.add_field(name="Is Scheduled Downtime", value=machine[1]['is_scheduled_downtime'], inline=True)
                                embed.add_field(name="GPU Current Temp", value=machine[1]['gpu_current_temp'], inline=True)
                                embed.add_field(name="GPU Fans Speed", value=machine[1]['gpu_fan_speed'], inline=True)
                                embed.add_field(name="Connections", value=machine[1]['connections'], inline=True)
                                embed.add_field(name="Load", value=machine[1]['load'], inline=True)
                                embed.add_field(name="Ping", value=machine[1]['ping'], inline=True)
                                embed.add_field(name="Packet Loss", value=machine[1]['packet_loss'], inline=True)
                                embed.add_field(name="RTA", value=machine[1]['rta'], inline=True)
                                embed.add_field(name="Root Disk", value=machine[1]['root_disk'], inline=True)
                                embed.add_field(name="Smart Failed", value=machine[1]['smart_failed'], inline=True)
                                embed.add_field(name="Smart Predicted", value=machine[1]['smart_predicted'], inline=True)
                                embed.add_field(name="SSH", value=machine[1]['ssh'], inline=True)
                                embed.add_field(name="VarDisk", value=machine[1]['vardisk'], inline=True)
                                embed.add_field(name="X2GO", value=machine[1]['x2go'], inline=True)

                                embed.set_footer(text="/roomchecks")
                                for guild in bot.guilds:
                                    for channel in guild.channels:
                                        if (channel.name.lower() == 'room-check' or channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                        # if (channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                            send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                            with open(f'images/{machine[1]['room_number']}.png', 'rb') as f:
                                                file = discord.File(f, filename=f'{machine[1]['room_number']}.png')
                                                await send_message.send(file=file, embed=embed)
                                            break
                        else:
                            result_title = f'**Machines up and running.**'
                            result_description = f'({current_day} {current_time}) - All Machines Green'
                            embed = discord.Embed(title=result_title, description=result_description, color=8311585)
                            file = discord.File('images/icon.png', filename='icon.png')
                            embed.set_thumbnail(url='attachment://icon.png')
                            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                            embed.set_footer(text="/roomchecks")
                            for guild in bot.guilds:
                                for channel in guild.channels:
                                    if (channel.name.lower() == 'room-check' or channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                    # if (channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                        send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                        with open('images/icon.png', 'rb') as f:
                                            file = discord.File(f, filename='icon.png')
                                            await send_message.send(file=file, embed=embed)
                                        break
                        room_checks_done = True
                    else:
                        room_checks_done = False
                elif current_day in ['Friday']:
                    if (current_time in ['13:00', ['18:00']] and not room_checks_done):
                        for room in room_dictionary:
                            for machine in room_dictionary[room]:
                                with open(f'ilab_machines/{machine}.json', 'r') as file:
                                    data = json.load(file)
                                    if data['host_status'].lower() != 'up':
                                        downmachines.append((machine, data))
                        if len(downmachines) > 0:
                            for machine in downmachines:
                                result_title = f'**Machine may be down.**'
                                result_description = f'({current_day} {current_time}) - **{machine[0]}**\'s status is currently down.'
                                embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                                file = discord.File(f'images/{machine[1]['room_number']}.png', filename=f'{machine[1]['room_number']}.png')
                                embed.set_image(url=f'attachment://{machine[1]['room_number']}.png')
                                embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                                embed.add_field(name="Machine Name", value=machine[1]['name'], inline=True)
                                embed.add_field(name="Room Number", value=machine[1]['room_number'], inline=True)
                                embed.add_field(name="Host Status", value=machine[1]['host_status'], inline=True)
                                embed.add_field(name="Last Check Time", value=machine[1]['last_check_time'], inline=True)
                                embed.add_field(name="Next Schedule Active Check", value=machine[1]['next_schedule_active_check'], inline=True)
                                embed.add_field(name="Is Scheduled Downtime", value=machine[1]['is_scheduled_downtime'], inline=True)
                                embed.add_field(name="GPU Current Temp", value=machine[1]['gpu_current_temp'], inline=True)
                                embed.add_field(name="GPU Fans Speed", value=machine[1]['gpu_fan_speed'], inline=True)
                                embed.add_field(name="Connections", value=machine[1]['connections'], inline=True)
                                embed.add_field(name="Load", value=machine[1]['load'], inline=True)
                                embed.add_field(name="Ping", value=machine[1]['ping'], inline=True)
                                embed.add_field(name="Packet Loss", value=machine[1]['packet_loss'], inline=True)
                                embed.add_field(name="RTA", value=machine[1]['rta'], inline=True)
                                embed.add_field(name="Root Disk", value=machine[1]['root_disk'], inline=True)
                                embed.add_field(name="Smart Failed", value=machine[1]['smart_failed'], inline=True)
                                embed.add_field(name="Smart Predicted", value=machine[1]['smart_predicted'], inline=True)
                                embed.add_field(name="SSH", value=machine[1]['ssh'], inline=True)
                                embed.add_field(name="VarDisk", value=machine[1]['vardisk'], inline=True)
                                embed.add_field(name="X2GO", value=machine[1]['x2go'], inline=True)

                                embed.set_footer(text="/roomchecks")
                                for guild in bot.guilds:
                                    for channel in guild.channels:
                                        if (channel.name.lower() == 'room-check' or channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                        # if (channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                            send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                            with open(f'images/{machine[1]['room_number']}.png', 'rb') as f:
                                                file = discord.File(f, filename=f'{machine[1]['room_number']}.png')
                                                await send_message.send(file=file, embed=embed)
                                            break
                        else:
                            result_title = f'**Machines up and running.**'
                            result_description = f'({current_day} {current_time}) - All Machines Green'
                            embed = discord.Embed(title=result_title, description=result_description, color=8311585)
                            file = discord.File('images/icon.png', filename='icon.png')
                            embed.set_thumbnail(url='attachment://icon.png')
                            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                            embed.set_footer(text="/roomchecks")
                            for guild in bot.guilds:
                                for channel in guild.channels:
                                    if (channel.name.lower() == 'room-check' or channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                    # if (channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                        send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                        with open('images/icon.png', 'rb') as f:
                                            file = discord.File(f, filename='icon.png')
                                            await send_message.send(file=file, embed=embed)
                                        break
                        room_checks_done = True
                    else:
                        room_checks_done = False
                elif current_day in ['Sunday']:
                    if (current_time in ['15:00', ['23:00']] and not room_checks_done):
                        for room in room_dictionary:
                            for machine in room_dictionary[room]:
                                with open(f'ilab_machines/{machine}.json', 'r') as file:
                                    data = json.load(file)
                                    if data['host_status'].lower() != 'up':
                                        downmachines.append((machine, data))
                        if len(downmachines) > 0:
                            for machine in downmachines:
                                result_title = f'**Machine may be down.**'
                                result_description = f'({current_day} {current_time}) - **{machine[0]}**\'s status is currently down.'
                                embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                                file = discord.File(f'images/{machine[1]['room_number']}.png', filename=f'{machine[1]['room_number']}.png')
                                embed.set_image(url=f'attachment://{machine[1]['room_number']}.png')
                                embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                                embed.add_field(name="Machine Name", value=machine[1]['name'], inline=True)
                                embed.add_field(name="Room Number", value=machine[1]['room_number'], inline=True)
                                embed.add_field(name="Host Status", value=machine[1]['host_status'], inline=True)
                                embed.add_field(name="Last Check Time", value=machine[1]['last_check_time'], inline=True)
                                embed.add_field(name="Next Schedule Active Check", value=machine[1]['next_schedule_active_check'], inline=True)
                                embed.add_field(name="Is Scheduled Downtime", value=machine[1]['is_scheduled_downtime'], inline=True)
                                embed.add_field(name="GPU Current Temp", value=machine[1]['gpu_current_temp'], inline=True)
                                embed.add_field(name="GPU Fans Speed", value=machine[1]['gpu_fan_speed'], inline=True)
                                embed.add_field(name="Connections", value=machine[1]['connections'], inline=True)
                                embed.add_field(name="Load", value=machine[1]['load'], inline=True)
                                embed.add_field(name="Ping", value=machine[1]['ping'], inline=True)
                                embed.add_field(name="Packet Loss", value=machine[1]['packet_loss'], inline=True)
                                embed.add_field(name="RTA", value=machine[1]['rta'], inline=True)
                                embed.add_field(name="Root Disk", value=machine[1]['root_disk'], inline=True)
                                embed.add_field(name="Smart Failed", value=machine[1]['smart_failed'], inline=True)
                                embed.add_field(name="Smart Predicted", value=machine[1]['smart_predicted'], inline=True)
                                embed.add_field(name="SSH", value=machine[1]['ssh'], inline=True)
                                embed.add_field(name="VarDisk", value=machine[1]['vardisk'], inline=True)
                                embed.add_field(name="X2GO", value=machine[1]['x2go'], inline=True)

                                embed.set_footer(text="/roomchecks")
                                for guild in bot.guilds:
                                    for channel in guild.channels:
                                        if (channel.name.lower() == 'room-check' or channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                        # if (channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                            send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                            with open(f'images/{machine[1]['room_number']}.png', 'rb') as f:
                                                file = discord.File(f, filename=f'{machine[1]['room_number']}.png')
                                                await send_message.send(file=file, embed=embed)
                                            break
                        else:
                            result_title = f'**Machines up and running.**'
                            result_description = f'({current_day} {current_time}) - All Machines Green'
                            embed = discord.Embed(title=result_title, description=result_description, color=8311585)
                            file = discord.File('images/icon.png', filename='icon.png')
                            embed.set_thumbnail(url='attachment://icon.png')
                            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                            embed.set_footer(text="/roomchecks")
                            for guild in bot.guilds:
                                for channel in guild.channels:
                                    if (channel.name.lower() == 'room-check' or channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                    # if (channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                        send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                        with open('images/icon.png', 'rb') as f:
                                            file = discord.File(f, filename='icon.png')
                                            await send_message.send(file=file, embed=embed)
                                        break
                        room_checks_done = True
                    else:
                        room_checks_done = False
            elif session_type == 'summer':
                if current_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday']:
                    if (current_time in ['13:00', ['18:00']] and not room_checks_done):
                        for room in room_dictionary:
                            for machine in room_dictionary[room]:
                                with open(f'ilab_machines/{machine}.json', 'r') as file:
                                    data = json.load(file)
                                    if data['host_status'].lower() != 'up':
                                        downmachines.append((machine, data))
                        if len(downmachines) > 0:
                            for machine in downmachines:
                                result_title = f'**Machine may be down.**'
                                result_description = f'({current_day} {current_time}) - **{machine[0]}**\'s status is currently down.'
                                embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                                file = discord.File(f'images/{machine[1]['room_number']}.png', filename=f'{machine[1]['room_number']}.png')
                                embed.set_image(url=f'attachment://{machine[1]['room_number']}.png')
                                embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                                embed.add_field(name="Machine Name", value=machine[1]['name'], inline=True)
                                embed.add_field(name="Room Number", value=machine[1]['room_number'], inline=True)
                                embed.add_field(name="Host Status", value=machine[1]['host_status'], inline=True)
                                embed.add_field(name="Last Check Time", value=machine[1]['last_check_time'], inline=True)
                                embed.add_field(name="Next Schedule Active Check", value=machine[1]['next_schedule_active_check'], inline=True)
                                embed.add_field(name="Is Scheduled Downtime", value=machine[1]['is_scheduled_downtime'], inline=True)
                                embed.add_field(name="GPU Current Temp", value=machine[1]['gpu_current_temp'], inline=True)
                                embed.add_field(name="GPU Fans Speed", value=machine[1]['gpu_fan_speed'], inline=True)
                                embed.add_field(name="Connections", value=machine[1]['connections'], inline=True)
                                embed.add_field(name="Load", value=machine[1]['load'], inline=True)
                                embed.add_field(name="Ping", value=machine[1]['ping'], inline=True)
                                embed.add_field(name="Packet Loss", value=machine[1]['packet_loss'], inline=True)
                                embed.add_field(name="RTA", value=machine[1]['rta'], inline=True)
                                embed.add_field(name="Root Disk", value=machine[1]['root_disk'], inline=True)
                                embed.add_field(name="Smart Failed", value=machine[1]['smart_failed'], inline=True)
                                embed.add_field(name="Smart Predicted", value=machine[1]['smart_predicted'], inline=True)
                                embed.add_field(name="SSH", value=machine[1]['ssh'], inline=True)
                                embed.add_field(name="VarDisk", value=machine[1]['vardisk'], inline=True)
                                embed.add_field(name="X2GO", value=machine[1]['x2go'], inline=True)

                                embed.set_footer(text="/roomchecks")
                                for guild in bot.guilds:
                                    for channel in guild.channels:
                                        if (channel.name.lower() == 'room-check' or channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                        # if (channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                            send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                            with open(f'images/{machine[1]['room_number']}.png', 'rb') as f:
                                                file = discord.File(f, filename=f'{machine[1]['room_number']}.png')
                                                await send_message.send(file=file, embed=embed)
                                            break
                        else:
                            result_title = f'**Machines up and running.**'
                            result_description = f'({current_day} {current_time}) - All Machines Green'
                            embed = discord.Embed(title=result_title, description=result_description, color=8311585)
                            file = discord.File('images/icon.png', filename='icon.png')
                            embed.set_thumbnail(url='attachment://icon.png')
                            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                            embed.set_footer(text="/roomchecks")
                            for guild in bot.guilds:
                                for channel in guild.channels:
                                    if (channel.name.lower() == 'room-check' or channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                    # if (channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                        send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                        with open('images/icon.png', 'rb') as f:
                                            file = discord.File(f, filename='icon.png')
                                            await send_message.send(file=file, embed=embed)
                                        break
                        room_checks_done = True
                    else:
                        room_checks_done = False
            elif session_type == 'break':
                continue
            await asyncio.sleep(60)

    async def checkmachine(bot : commands.Bot):
        history_dictionary = {}
        for room in room_dictionary:
            for machine in room_dictionary[room]:
                if machine not in history_dictionary:
                    history_dictionary[machine] = {'status': 'UP'}
        while True:
            for room in room_dictionary:
                for machine in room_dictionary[room]:
                    url = f"https://report.cs.rutgers.edu/nagios4/cgi-bin/status.cgi?style=details&host={machine}"
                    page_text = webscraper.fetch_page_content(url).strip('\n')
                    webscraper.write_to_file(f"{machine}.json", page_text)
                    current_network_status_output = webscraper.current_network_status(f'{machine}.json', machine)
                    os.remove(f'{machine}.json')

                    url = f"https://report.cs.rutgers.edu/nagios4/cgi-bin/extinfo.cgi?type=1&host={machine}"
                    page_text = webscraper.fetch_page_content(url).strip('\n')
                    webscraper.write_to_file(f"{machine}.json", page_text)
                    extended_information_output = webscraper.extended_information(f'{machine}.json', machine)
                    os.remove(f'{machine}.json')

                    ilab_machine = IlabMachine(machine, room, extended_information_output[0], current_network_status_output[0],
                                            extended_information_output[1], extended_information_output[2], current_network_status_output[1],
                                            current_network_status_output[2], current_network_status_output[3], current_network_status_output[4],
                                            current_network_status_output[5], current_network_status_output[6], current_network_status_output[7],
                                            current_network_status_output[8], current_network_status_output[9], current_network_status_output[10],
                                            current_network_status_output[11], current_network_status_output[12], current_network_status_output[13])

                    ilab_machine.to_json()
                    if ilab_machine.host_status.lower() != 'up':
                        current = datetime.datetime.now()
                        current_day = current.strftime('%A')
                        current_time = current.strftime('%H:%M')
                        if history_dictionary[machine]['status'].lower() != 'down':
                            result_title = f'**Machine may be down.**'
                            result_description = f'({current_day} {current_time}) - **{machine[0]}**\'s status is currently down.'
                            embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                            file = discord.File(f'images/{machine[1]['room_number']}.png', filename=f'{machine[1]['room_number']}.png')
                            embed.set_image(url=f'attachment://{machine[1]['room_number']}.png')
                            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                            embed.add_field(name="Machine Name", value=machine[1]['name'], inline=True)
                            embed.add_field(name="Room Number", value=machine[1]['room_number'], inline=True)
                            embed.add_field(name="Host Status", value=machine[1]['host_status'], inline=True)
                            embed.add_field(name="Last Check Time", value=machine[1]['last_check_time'], inline=True)
                            embed.add_field(name="Next Schedule Active Check", value=machine[1]['next_schedule_active_check'], inline=True)
                            embed.add_field(name="Is Scheduled Downtime", value=machine[1]['is_scheduled_downtime'], inline=True)
                            embed.add_field(name="GPU Current Temp", value=machine[1]['gpu_current_temp'], inline=True)
                            embed.add_field(name="GPU Fans Speed", value=machine[1]['gpu_fan_speed'], inline=True)
                            embed.add_field(name="Connections", value=machine[1]['connections'], inline=True)
                            embed.add_field(name="Load", value=machine[1]['load'], inline=True)
                            embed.add_field(name="Ping", value=machine[1]['ping'], inline=True)
                            embed.add_field(name="Packet Loss", value=machine[1]['packet_loss'], inline=True)
                            embed.add_field(name="RTA", value=machine[1]['rta'], inline=True)
                            embed.add_field(name="Root Disk", value=machine[1]['root_disk'], inline=True)
                            embed.add_field(name="Smart Failed", value=machine[1]['smart_failed'], inline=True)
                            embed.add_field(name="Smart Predicted", value=machine[1]['smart_predicted'], inline=True)
                            embed.add_field(name="SSH", value=machine[1]['ssh'], inline=True)
                            embed.add_field(name="VarDisk", value=machine[1]['vardisk'], inline=True)
                            embed.add_field(name="X2GO", value=machine[1]['x2go'], inline=True)
                            embed.set_footer(text="/checkmachine")
                            for guild in bot.guilds:
                                for channel in guild.channels:
                                    if (channel.name.lower() == 'room-check' or channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                    # if (channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                                        send_message = bot.get_guild(guild.id).get_channel(channel.id)
                                        with open(f'images/{machine[1]['room_number']}.png', 'rb') as f:
                                            file = discord.File(f, filename=f'{machine[1]['room_number']}.png')
                                        await send_message.send(file=file, embed=embed)
                                        break
                            history_dictionary[machine]['status'] = 'DOWN'
                        else:
                            continue
                time.sleep(1)


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
        completed = False
        
        global session_type
        if user_input_session == 'regular':
            session_type = user_input_session
            completed = True
        elif user_input_session == 'summer':
            session_type = user_input_session
            completed = True
        elif user_input_session == 'break':
            session_type = user_input_session
            completed = True

        if completed:
            result_title = f'**Session Changed** to ***{user_input_session}***'
            embed = discord.Embed(title=result_title, description=result_description, color=8311585)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
            embed.set_footer(text="/changesession")
        else:
            result_title = f'**Invalid Input**'
            embed = discord.Embed(title=result_title, color=13632027)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="CAVE-iLab-Machine-Bot says:")
            embed.set_footer(text="/changesession")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=False)

    bot.run(TOKEN)