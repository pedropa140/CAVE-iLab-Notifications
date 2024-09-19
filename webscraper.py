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
        last_checked = lines[2].split()[2:]
        last_checked_output = f'{last_checked[0]} {last_checked[1]} {last_checked[2]} {last_checked[3]} {last_checked[5]} {last_checked[4]}'
        temperature_status = lines[51].split()[3]
        gpu_fan_speed = lines[57].split()[3]
        connections = lines[63].split()[3]
        
        load = lines[69].split()[3]
        ping = lines[75].split()[1]
        packet_loss = lines[75].split()[6]
        rta = " ".join(lines[75].split()[9:])
        root_disk = lines[81].split()[3]
        smartfailed = lines[87].split()[3]
        smartpredicted = lines[93].split()[3]
        ssh = lines[105].split()[0]
        ssh = ssh.replace("Logins=", "")
        print(ssh)
        vardisk = lines[117].split()[3]
        x2go = lines[123].split()[3]
    return [last_checked, int(temperature_status), int(gpu_fan_speed), int(connections), load, ping,
            packet_loss, rta, int(root_disk), int(smartfailed), int(smartpredicted), int(ssh), int(vardisk), int(x2go)]    

def extended_information(file_name : str, machine_name : str):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        status = lines[19].split()[2]
        next_scheduled_check = " ".join(lines[26].split()[4:])
        in_scheduled_downtime = lines[30].split()[3]
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

    machine = 'assembly.cs.rutgers.edu'
    # https://report.cs.rutgers.edu/nagios4/cgi-bin/status.cgi?style=details&host=assembly.cs.rutgers.edu
    url = f"https://report.cs.rutgers.edu/nagios4/cgi-bin/status.cgi?style=details&host={machine}"
    page_text = fetch_page_content(url).strip('\n')
    write_to_file(f"ilab_machines/{machine}.txt", page_text)
    current_network_status_output = current_network_status(f'ilab_machines/{machine}.txt', machine)
    os.remove(f'ilab_machines/{machine}.txt')

    url = f"https://report.cs.rutgers.edu/nagios4/cgi-bin/extinfo.cgi?type=1&host={machine}"
    page_text = fetch_page_content(url).strip('\n')
    write_to_file(f"ilab_machines/{machine}.txt", page_text)
    extended_information_output = extended_information(f'ilab_machines/{machine}.txt', machine)

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
            write_to_file(f"ilab_machines/{machine}.txt", page_text)
            current_network_status_output = current_network_status(f'ilab_machines/{machine}.txt', machine)
            os.remove(f'ilab_machines/{machine}.txt')

            url = f"https://report.cs.rutgers.edu/nagios4/cgi-bin/extinfo.cgi?type=1&host={machine}"
            page_text = fetch_page_content(url)
            page_text.strip('\n')
            if "Error fetching page content" in page_text:
                continue
            write_to_file(f"ilab_machines/{machine}.txt", page_text)
            extended_information_output = extended_information(f'ilab_machines/{machine}.txt', machine)
            os.remove(f'ilab_machines/{machine}.txt')

            ilab_machine = IlabMachine(machine, room, extended_information_output[0], current_network_status_output[0],
                                    extended_information_output[1], extended_information_output[2], current_network_status_output[1],
                                    current_network_status_output[2], current_network_status_output[3], current_network_status_output[4],
                                    current_network_status_output[5], current_network_status_output[6], current_network_status_output[7],
                                    current_network_status_output[8], current_network_status_output[9], current_network_status_output[10],
                                    current_network_status_output[11], current_network_status_output[12], current_network_status_output[13])

            ilab_machine.to_json()