import daemon
from start_locking import main
import os
import hashlib
import sys
import os
 

if __name__ == '__main__':
    if len(sys.argv) > 1:
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', sys.argv[1].encode('utf-8'), salt, 100000)
        storage = salt + key 
        with open('password.hash', 'wb') as file:
            file.write(storage)
        print('Задан новый пароль!')
    elif not os.path.exists('password.hash'):
        password = input('[!] Не задан пароль! введите новый пароль: ')
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        storage = salt + key 
        with open('password.hash', 'wb') as file:
            file.write(storage)
        print('Задан новый пароль!')
    print('Защита включена')
    with daemon.DaemonContext():
        main()
