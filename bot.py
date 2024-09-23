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
import logging

load_dotenv()

logging.basicConfig(filename='bot_events.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

session_type = "summer"
history_dictionary = {}

def run_discord_bot():    
    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.all()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    room_dictionary = {248: [
        "cd.cs.rutgers.edu",
        "cp.cs.rutgers.edu",
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

    for room in room_dictionary:
        for machine in room_dictionary[room]:
            if machine not in history_dictionary:
                history_dictionary[machine] = {'status': 'UP'}

    @bot.event
    async def on_ready():
        try:
            synced = await bot.tree.sync()
            logging.info(f'Synced {len(synced)} command(s)')
            await checkmachine(bot)

            setup_scheduler()            
            logging.info(f'{bot.user} is now running!')

            async def run_scheduler():
                while True:
                    schedule.run_pending()
                    await asyncio.sleep(60)
                    
            asyncio.create_task(run_scheduler())
            
        except Exception as e:
            logging.error(f'Error in on_ready: {e}')
        
    async def perform_room_checks():
        global room_checks_done
        room_checks_done = False
        date = datetime.datetime.now()
        current_time = date.strftime('%H:%M')
        current_day = date.strftime('%A')
        downmachines = []

        if session_type == 'regular':
            if current_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday']:
                if (current_time in ['13:00', '23:00'] and not room_checks_done):
                    for room in room_dictionary:
                        for machine in room_dictionary[room]:
                            with open(f'ilab_machines/{machine}.json', 'r') as file:
                                data = json.load(file)
                                if data['host_status'].lower() != 'up':
                                    downmachines.append((machine, data))
                    await send_room_check_results(downmachines, current_day, current_time)
                    room_checks_done = True
                else:
                    room_checks_done = False
            elif current_day == 'Friday':
                if (current_time in ['13:00', '18:00'] and not room_checks_done):
                    for room in room_dictionary:
                        for machine in room_dictionary[room]:
                            with open(f'ilab_machines/{machine}.json', 'r') as file:
                                data = json.load(file)
                                if data['host_status'].lower() != 'up':
                                    downmachines.append((machine, data))
                    await send_room_check_results(downmachines, current_day, current_time)
                    room_checks_done = True
                else:
                    room_checks_done = False
            elif current_day == 'Sunday':
                if (current_time in ['15:00', '23:00'] and not room_checks_done):
                    for room in room_dictionary:
                        for machine in room_dictionary[room]:
                            with open(f'ilab_machines/{machine}.json', 'r') as file:
                                data = json.load(file)
                                if data['host_status'].lower() != 'up':
                                    downmachines.append((machine, data))
                    await send_room_check_results(downmachines, current_day, current_time)
                    room_checks_done = True
                else:
                    room_checks_done = False
        elif session_type == 'summer':
            if current_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday']:
                if (current_time in ['13:00', '18:00'] and not room_checks_done):
                    for room in room_dictionary:
                        for machine in room_dictionary[room]:
                            with open(f'ilab_machines/{machine}.json', 'r') as file:
                                data = json.load(file)
                                if data['host_status'].lower() != 'up':
                                    downmachines.append((machine, data))
                    await send_room_check_results(downmachines, current_day, current_time)
                    room_checks_done = True
                else:
                    room_checks_done = False

    async def send_room_check_results(downmachines, current_day, current_time):
        if len(downmachines) > 0:
            for machine in downmachines:
                result_title = f'**Machine may be down.**'
                result_description = f'({current_day} {current_time}) - **{machine[0]}**\'s status is currently down.'
                embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                embed.set_author(name="CAVE-iLab-Machine-Bot says:")
                embed.set_footer(text="/roomchecks")
                logging.warning(f'{machine[0]} is down')
                for guild in bot.guilds:
                    for channel in guild.channels:
                        # if (channel.name.lower() == 'room-check' or channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                        if (channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                            send_message = bot.get_guild(guild.id).get_channel(channel.id)
                            with open('images/icon.png', 'rb') as f:
                                file = discord.File(f, filename='icon.png')
                                embed.set_thumbnail(url='attachment://icon.png')
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
            logging.info('All machines are running normally')
            for guild in bot.guilds:
                for channel in guild.channels:
                    # if (channel.name.lower() == 'room-check' or channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                    if (channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                        send_message = bot.get_guild(guild.id).get_channel(channel.id)
                        with open('images/icon.png', 'rb') as f:
                            file = discord.File(f, filename='icon.png')
                            embed.set_thumbnail(url='attachment://icon.png')
                        await send_message.send(file=file, embed=embed)
                        break
    
    async def checkmachine(bot : commands.Bot):
        global history_dictionary
        logging.info('Starting machine check')
        for room in room_dictionary:
            for machine in room_dictionary[room]:
                url = f"https://report.cs.rutgers.edu/nagios4/cgi-bin/status.cgi?style=details&host={machine}"
                page_text = webscraper.fetch_page_content(url)
                page_text.strip('\n')
                if "Error fetching page content" in page_text:
                    logging.error(f'Error fetching page content for {machine}')
                    continue
                webscraper.write_to_file(f"{machine}.txt", page_text)
                current_network_status_output = webscraper.current_network_status(f'{machine}.txt', machine)
                os.remove(f'{machine}.txt')

                url = f"https://report.cs.rutgers.edu/nagios4/cgi-bin/extinfo.cgi?type=1&host={machine}"
                page_text = webscraper.fetch_page_content(url)
                page_text.strip('\n')
                if "Error fetching page content" in page_text:
                    logging.error(f'Error fetching extended info for {machine}')
                    continue
                webscraper.write_to_file(f"{machine}.txt", page_text)
                extended_information_output = webscraper.extended_information(f'{machine}.txt', machine)
                os.remove(f'{machine}.txt')

                ilab_machine = IlabMachine(machine, room, extended_information_output[0], current_network_status_output[0],
                                        extended_information_output[1], extended_information_output[2], current_network_status_output[1],
                                        current_network_status_output[2], current_network_status_output[3], current_network_status_output[4])
                
                ilab_machine.set_status()
                json_filename = machine + '.json'
                ilab_machine.output_json(json_filename)
                logging.info(f'Successfully created JSON file for {machine}')

                with open(f'ilab_machines/{machine}.json', 'r') as f:
                    newdata = json.load(f)
                if (history_dictionary[machine]['status'] != newdata['host_status']):
                    logging.info(f'{machine} status changed from {history_dictionary[machine]["status"]} to {newdata["host_status"]}')
                    history_dictionary[machine]['status'] = newdata['host_status']
                    await notify_machine_status_change(newdata['host_name'], newdata['host_status'])
                else:
                    continue

    async def notify_machine_status_change(machine_name, status):
        title = f"**{machine_name}'s status has changed.**"
        description = f"The new status is {status.upper()}."
        color = 13632027 if status.lower() != 'up' else 8311585
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_author(name="CAVE-iLab-Machine-Bot says:")
        embed.set_footer(text="/roomchecks")
        logging.warning(f'Machine {machine_name} changed status to {status.upper()}')
        for guild in bot.guilds:
            for channel in guild.channels:
                # if (channel.name.lower() == 'room-check' or channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                if (channel.name.lower() == 'cave-roomchecks-bot') and str(channel.type).lower() == 'text':
                    send_message = bot.get_guild(guild.id).get_channel(channel.id)
                    with open('images/icon.png', 'rb') as f:
                        file = discord.File(f, filename='icon.png')
                        embed.set_thumbnail(url='attachment://icon.png')
                    await send_message.send(file=file, embed=embed)
                    break

    def setup_scheduler():
        logging.info('Setting up schedule')
        schedule.every(3).hours.do(asyncio.run_coroutine_threadsafe, checkmachine(bot), asyncio.get_event_loop())
        schedule.every().day.at("13:00").do(asyncio.run_coroutine_threadsafe, perform_room_checks(), asyncio.get_event_loop())
        schedule.every().day.at("18:00").do(asyncio.run_coroutine_threadsafe, perform_room_checks(), asyncio.get_event_loop())
        schedule.every().day.at("23:00").do(asyncio.run_coroutine_threadsafe, perform_room_checks(), asyncio.get_event_loop())
        logging.info('Scheduler setup complete')

    bot.run(TOKEN)
