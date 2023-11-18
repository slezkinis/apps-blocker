import subprocess
import hashlib
import time
import psutil
import os


with open('password.hash', 'rb') as file:
    storage = file.read()

salt = storage[:32]
key = storage[32:]

while True:
    password = input('Введите пароль: ')
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'), # Конвертирование пароля в байты
        salt, 
        100000
    )
    if new_key == key:
        with open('pid.txt', 'r') as file:
            pid = int(file.read())
        locking_process = psutil.Process(pid)
        locking_process.terminate()
        os.remove('pid.txt')
        try:
            child = subprocess.Popen(["networksetup", "-setairportpower", "airport", "on"], stdout=subprocess.PIPE)
            output, error = child.communicate()
        except:
            try:
                child = subprocess.Popen(['nmcli', 'device', 'connect', 'wlan0'], stdout=subprocess.PIPE)
                output, error = child.communicate()
            except:
                a = 1
        print('Разблокировано')
        break
    else:
        print('Неверный пароль')