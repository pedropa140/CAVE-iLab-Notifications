import json
class IlabMachine:
    def __init__(self, 
                 name,
                 room_number,
                 host_status,
                 last_check_time,
                 next_schedule_active_check,
                 is_scheduled_downtime,
                 gpu_current_temp,
                 gpu_fan_speed,
                 connections,
                 load,
                 ping,
                 packet_loss,
                 rta,
                 root_disk,
                 smart_failed,
                 smart_predicted,
                 ssh,
                 vardisk,
                 x2go
                 ):
        self.name = name
        self.room_number = room_number
        self.host_status = host_status
        self.last_check_time = last_check_time
        self.next_schedule_active_check = next_schedule_active_check
        self.is_scheduled_downtime = is_scheduled_downtime
        self.gpu_current_temp = gpu_current_temp
        self.gpu_fan_speed = gpu_fan_speed
        self.connections = connections  
        self.load = load
        self.ping = ping
        self.packet_loss = packet_loss
        self.rta = rta
        self.root_disk = root_disk
        self.smart_failed = smart_failed
        self.smart_predicted = smart_predicted
        self.ssh = ssh
        self.vardisk = vardisk
        self.x2go = x2go

    def __repr__(self):
        return (f"IlabMachine(name={self.name}, room_number={self.room_number}, host_status={self.host_status}, "
                f"last_check_time={self.last_check_time}, next_schedule_active_check={self.next_schedule_active_check}, "
                f"is_scheduled_downtime={self.is_scheduled_downtime}, gpu_current_temp={self.gpu_current_temp}, "
                f"gpu_fan_speed={self.gpu_fan_speed}, connections={self.connections}, load={self.load}, "
                f"ping={self.ping}, root_disk={self.root_disk}, smart_failed={self.smart_failed}, "
                f"smart_predicted={self.smart_predicted}, ssh={self.ssh}, " 
                f"vardisk={self.vardisk}, x2go={self.x2go})")

    def to_json(self):
        data = {
            "name": self.name,
            "room_number": self.room_number,
            "host_status": self.host_status,
            "last_check_time": self.last_check_time,
            "next_schedule_active_check": self.next_schedule_active_check,
            "is_scheduled_downtime": self.is_scheduled_downtime,
            "gpu_current_temp": self.gpu_current_temp,
            "gpu_fan_speed": self.gpu_fan_speed,
            "connections": self.connections,
            "load": self.load,
            "ping": self.ping,
            "packet_loss": self.packet_loss,
            "rta": self.rta,
            "root_disk": self.root_disk,
            "smart_failed": self.smart_failed,
            "smart_predicted": self.smart_predicted,
            "ssh": self.ssh,
            "vardisk": self.vardisk,
            "x2go": self.x2go
        }
        json_data = json.dumps(data, default=str, indent=4)
        
        try:
            with open('ilab_machines/' + self.name + '.json', 'w') as file:
                file.write(json_data)
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}.txt")