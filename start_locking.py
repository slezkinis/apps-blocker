import psutil
import threading
import subprocess
import os


all_processes = []
def check():
    while True:
        try:
            child = subprocess.Popen(["networksetup", "-setairportpower", "airport", "off"], stdout=subprocess.PIPE)
            output, error = child.communicate()
        except:
            try:
                child = subprocess.Popen(['nmcli', 'device', 'disconnect', 'wlan0'], stdout=subprocess.PIPE)
                output, error = child.communicate()
            except:
                a = 1
        processes = psutil.process_iter()
        try:
            for i in processes:
                if i.pid not in all_processes and 'ytho' not in i.name().lower():
                    try:
                        i.terminate()
                    except:
                        continue
        except psutil.NoSuchProcess:
            continue


def main():
    current_file = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file)
    # Обязательно указывтаь полный путь!
    with open(f'{current_directory}/pid.txt', 'w') as file:
        file.write(str(os.getpid()))
    processes = psutil.process_iter()
    for i in processes:
        all_processes.append(i.pid)
    thread = threading.Thread(target=check)
    thread.start()