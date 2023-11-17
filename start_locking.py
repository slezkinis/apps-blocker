import psutil
import threading
import subprocess


all_processes = []
def check():
    while True:
        child = subprocess.Popen(["networksetup", "-setairportpower", "airport", "off"], stdout=subprocess.PIPE)
        output, error = child.communicate()
        processes = psutil.process_iter()
        try:
            for i in processes:
                if i.name() not in all_processes:
                    try:
                        i.kill()
                    except:
                        continue
        except psutil.NoSuchProcess:
            continue


def main():
    processes = psutil.process_iter()
    for i in processes:
        all_processes.append(i.name())
    thread = threading.Thread(target=check)
    thread.start()