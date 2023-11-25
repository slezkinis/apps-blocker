import subprocess
import hashlib
import getpass
import psutil
import os


with open('password.hash', 'rb') as file:
    storage = file.read()

salt = storage[:32]
key = storage[32:]

while True:
    if not os.path.exists('pid.txt'):
        print('Защита не включена!')
        break
    password = getpass.getpass('Введите пароль: ')
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt, 
        100000
    )
    if new_key == key:
        with open('pid.txt', 'r') as file:
            pid = int(file.read())
        locking_process = psutil.Process(pid)
        locking_process.terminate()
        os.remove('pid.txt')
        print('Разблокировано')
        break
    else:
        print('Неверный пароль')