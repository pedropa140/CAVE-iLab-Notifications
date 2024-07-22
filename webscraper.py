from bs4 import BeautifulSoup
import requests
from ilabmachine import IlabMachine
import os
import datetime

def fetch_page_content(url : str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text()
        print(f"{url}'s Page Type is -> {type(page_text)}")
        return page_text

    except requests.exceptions.RequestException as e:
        return f"Error fetching page content: {e}"

def write_to_file(filename : str, content : str):
    try:
        with open(filename, 'w') as file:
            for line in content.splitlines():
                if line.strip():
                    file.write(line + "\n")
    except IOError as e:
        print(f"Error writing to file: {e}")

def current_network_status(file_name : str, machine_name : str):
    with open(file_name, "r") as file:
        lines = file.readlines()
        last_checked = lines[2].replace('Last Updated: ', '')[4:].strip()
        temperature_status = lines[51].replace('OK - GPUCurrentTemp: ', '').replace(' (Threshold: High: 97 Warning: 93)', '').strip()
        gpu_fan_speed = lines[57].replace('OK - GPUFanSpeed: ', '').strip()
        connections = lines[63].replace('OK - Connections: ', '').replace(' (Threshold: High: 8000 Warning: 5000)','').strip()
        
        end_index = lines[69].index('(')
        end_string = lines[69][end_index:]
        load = lines[69].replace('OK - Load: ', '').replace(end_string, '').strip().strip()
        substring = " - Packet loss = "
        ping = lines[75].replace('PING ', '').strip()
        start_index = ping.find(substring)
        ping = ping[:start_index]
        start_index = lines[75].index('Packet loss = ')
        end_index = lines[75].index('%')
        first_string = lines[75][:start_index + 14]
        end_string = lines[75][end_index:]
        packet_loss = lines[75].replace(first_string, '').replace(end_string, '').strip()
        start_index = lines[75].index('RTA = ')
        end_index = lines[75].index(' ms')
        first_string = lines[75][:start_index + 5]
        end_string = lines[75][end_index:]
        rta = lines[75].replace(first_string, '').replace(end_string, '').strip()
        start_index = lines[81].index('OK - RootDisk: ')
        end_index = lines[81].index(' (Threshold: High: 99 Warning: 97)')
        first_string = lines[81][:start_index + len('OK - RootDisk: ')]
        end_string = lines[81][end_index:]
        root_disk = lines[81].replace(first_string, '').replace(end_string, '').strip()
        start_index = lines[87].index('- smartfailed: ')
        end_index = lines[87].index(' (Threshold: High: 1 Warning: 1)')
        first_string = lines[87][:start_index + len('- smartfailed: ')]
        end_string = lines[87][end_index:]
        smartfailed = lines[87].replace(first_string, '').replace(end_string, '').strip()
        start_index = lines[93].index('- smartpredicted: ')
        end_index = lines[93].index(' (Threshold: High: 1 Warning: 1)')
        first_string = lines[93][:start_index + len('- smartpredicted: ')]
        end_string = lines[93][end_index:]
        smartpredicted = lines[93].replace(first_string, '').replace(end_string, '').strip()
        start_index = lines[99].index('SSH ')
        end_index = lines[99].index(' - OpenSSH_8.9p1 Ubuntu-3ubuntu0.10 (protocol 2.0)')
        first_string = lines[99][:start_index + len('SSH ')]
        end_string = lines[99][end_index:]
        ssh = lines[99].replace(first_string, '').replace(end_string, '').strip()
        start_index = lines[117].index('- VarDisk: ')
        end_index = lines[117].index(' (Threshold: High: 99 Warning: 97)')
        first_string = lines[117][:start_index + len('- VarDisk: ')]
        end_string = lines[117][end_index:]
        vardisk = lines[117].replace(first_string, '').replace(end_string, '').strip()
        try:
            start_index = lines[123].index(' - x2go: ')
            end_index = lines[123].index(' (Threshold: High: 100 Warning: 80)')
            first_string = lines[123][:start_index + len(' - x2go: ')]
            end_string = lines[123][end_index:]
            x2go = lines[123].replace(first_string, '').replace(end_string, '').strip()
        except Exception as e:
            start_index = lines[123].index(' - x2go: ')
            end_index = lines[123].index(' (Threshold: High: 60 Warning: 48)')
            first_string = lines[123][:start_index + len(' - x2go: ')]
            end_string = lines[123][end_index:]
            x2go = lines[123].replace(first_string, '').replace(end_string, '').strip()

    return [last_checked, int(temperature_status), int(gpu_fan_speed), int(connections), float(load), ping,
            float(packet_loss), float(rta), float(root_disk), float(smartfailed), float(smartpredicted), ssh, float(vardisk), int(x2go)]
    

def extended_information(file_name : str, machine_name : str):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        end_index = lines[19].index('(')
        end_string = lines[19][end_index:]
        status = lines[19].replace('Host Status:', '').replace(end_string, '').strip()
        next_scheduled_check = lines[26].replace('Next Scheduled Active Check:', '').strip()
        in_scheduled_downtime = lines[30].replace('In Scheduled Downtime?', '').strip()
        return [status, next_scheduled_check, in_scheduled_downtime]

if __name__ == '__main__':
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
    def find_key_by_value(search_string : str):
        for key, value_list in room_dictionary.items():
            if search_string in value_list:
                return key
        return None

    machine = input('')
    url = f"https://report.cs.rutgers.edu/nagios4/cgi-bin/status.cgi?style=details&host={machine}.cs.rutgers.edu"
    page_text = fetch_page_content(url).strip('\n')
    write_to_file(f"{machine}.txt", page_text)
    current_network_status_output = current_network_status(f'{machine}.txt', machine)
    os.remove(f'{machine}.txt')

    url = f"https://report.cs.rutgers.edu/nagios4/cgi-bin/extinfo.cgi?type=1&host={machine}.cs.rutgers.edu"
    page_text = fetch_page_content(url).strip('\n')
    write_to_file(f"{machine}.txt", page_text)
    extended_information_output = extended_information(f'{machine}.txt', machine)

    key = find_key_by_value(machine + '.cs.rutgers.edu')
    ilab_machine = IlabMachine(machine + '.cs.rutgers.edu', key, extended_information_output[0], current_network_status_output[0],
                               extended_information_output[1], extended_information_output[2], current_network_status_output[1],
                               current_network_status_output[2], current_network_status_output[3], current_network_status_output[4],
                               current_network_status_output[5], current_network_status_output[6], current_network_status_output[7],
                               current_network_status_output[8], current_network_status_output[9], current_network_status_output[10],
                               current_network_status_output[11], current_network_status_output[12], current_network_status_output[13])
    
    for room in room_dictionary:
        for machine in room_dictionary[room]:
            page_text = fetch_page_content(url)
            page_text.strip('\n')
            if "Error fetching page content" in page_text:
                continue
            webscraper.write_to_file(f"{machine}.txt", page_text)
            current_network_status_output = webscraper.current_network_status(f'{machine}.txt', machine)
            os.remove(f'{machine}.txt')

            url = f"https://report.cs.rutgers.edu/nagios4/cgi-bin/extinfo.cgi?type=1&host={machine}"
            page_text = fetch_page_content(url)
            page_text.strip('\n')
            if "Error fetching page content" in page_text:
                continue
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