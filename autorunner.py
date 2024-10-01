import subprocess
import time
import schedule
from datetime import datetime

def run_script():
    print("Starting 'main.py'...")
    global process
    process = subprocess.Popen(["python", "main.py"])

def terminate_and_restart():
    print(f"Terminating 'main.py' at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    process.terminate()
    process.wait()
    print("Waiting for 5 minutes before restarting...")
    time.sleep(300)
    run_script()

schedule.every().day.at("00:00").do(terminate_and_restart)
run_script()

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Program interrupted, terminating 'main.py'...")
    process.terminate()
    process.wait()
    print("Terminated.")
