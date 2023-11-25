import subprocess
import os
import hashlib
import sys
import os
import getpass
import time

if __name__ == '__main__':
    if len(sys.argv) > 1:
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', sys.argv[1].encode('utf-8'), salt, 100000)
        storage = salt + key 
        with open('password.hash', 'wb') as file:
            file.write(storage)
        print('Задан новый пароль!')
    elif not os.path.exists('password.hash'):
        password = getpass.getpass('[!] Не задан пароль! введите новый пароль: ')
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        storage = salt + key 
        with open('password.hash', 'wb') as file:
            file.write(storage)
        print('Задан новый пароль!')
    current_file = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file)
    if os.path.exists('pid.txt'):
        print('Уже запущена!')
        exit()
    print('Защита включена')
    DETACHED_PROCESS = 8
    current_file = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file)
    subprocess.Popen(f'python ./start_locking.py {current_directory}', creationflags=DETACHED_PROCESS, close_fds=True)
    time.sleep(1)