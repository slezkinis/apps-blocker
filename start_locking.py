import psutil
import threading
import subprocess
import os


all_processes_names = []
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
                # if i.pid not in all_processes and 'ytho' not in i.name().lower() and 'ermin' not in i.name().lower() and 'onsol' not in i.name().lower() and 'Терминал' not in i.name().lower() and 'bash' not in i.name().lower():
                if i.name() not in all_processes_names:
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
        all_processes_names.append(i.name())
    thread = threading.Thread(target=check)
    thread.start()