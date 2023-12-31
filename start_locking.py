import psutil
import sys
import subprocess
import os


all_processes_names = []
def check():
    while True:
        processes = psutil.process_iter()
        try:
            for i in processes:
                # if i.pid not in all_processes and 'ytho' not in i.name().lower() and 'ermin' not in i.name().lower() and 'onsol' not in i.name().lower() and 'Терминал' not in i.name().lower() and 'bash' not in i.name().lower():
                if i.pid not in all_processes_names and 'ython' not in i.name() and 'lock' not in i.name():
                    try:
                        i.terminate()
                    except:
                        continue
        except psutil.NoSuchProcess:
            continue


def main():
    # Обязательно указывтаь полный путь!
    with open(f'{sys.argv[1]}/pid.txt', 'w') as file:
        file.write(str(os.getpid()))
    processes = psutil.process_iter()
    for i in processes:
        all_processes_names.append(i.pid)
    print(all_processes_names)
    check()

if __name__ == '__main__' and os.path.exists('password.hash'):
    main()