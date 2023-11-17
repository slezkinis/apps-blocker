import subprocess
import hashlib
import time


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
        try:
            subprocess.check_output(['pkill', 'Python'])
        except:
            time.sleep(1)
            subprocess.check_output(['pkill', 'Python'])
        child = subprocess.Popen(["networksetup", "-setairportpower", "airport", "on"], stdout=subprocess.PIPE)
        output, error = child.communicate()
        print('Разблокировано')
        break
    else:
        print('Неверный пароль')