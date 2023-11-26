from tkinter import *
from PIL import ImageTk, Image
import subprocess
import hashlib
import psutil

import os


def enable_locking():
    label_locked.configure(text='Защита включена')
    btn.configure(text='Отключить защиту', command=disable_locking)
    DETACHED_PROCESS = 8
    subprocess.Popen('python ./start_locking.py', creationflags=DETACHED_PROCESS, close_fds=True)


def disable_locking():
    def _disable():
        with open('password.hash', 'rb') as file:
            storage = file.read()

        salt = storage[:32]
        key = storage[32:]
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            enter_password_entry.get().encode('utf-8'),
            salt, 
            100000
        )
        if key == new_key:
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', enter_password_entry.get().encode('utf-8'), salt, 100000)
            storage = salt + key 
            with open('password.hash', 'wb') as file:
                file.write(storage)
            status = Label(disable_window, text='Защита отключена', font=("Arial", 15), fg='#06b800')
            status.grid(column=0, row=3)
            label_locked.configure(text='Защита отключена')
            btn.configure(text='Включить защиту', command=enable_locking)
            with open('pid.txt', 'r') as file:
                pid = int(file.read())
            locking_process = psutil.Process(pid)
            locking_process.terminate()
            os.remove('pid.txt')

        else:
            status = Label(disable_window, text='Неверный пароль', font=("Arial", 15), fg='#f52c00')
            status.grid(column=0, row=3)

    
    disable_window = Tk()
    disable_window.title("Отключение защиты")
    disable_window.geometry("310x200")
    enter_password_lbl = Label(disable_window, text='Введите пароль:', font=("Arial", 15))
    enter_password_lbl.grid(column=0, row=0)
    enter_password_entry = Entry(disable_window)
    enter_password_entry.grid(column=1, row=0)
    ok = Button(disable_window, text='Отключить', command=_disable)
    ok.grid(column=0, row=2)
    status = Label(disable_window, text='', font=("Arial", 15))
    status.grid(column=0, row=3)


def change_password():
    def _change():
        if os.path.exists('password.hash'):
            with open('password.hash', 'rb') as file:
                storage = file.read()

            salt = storage[:32]
            key = storage[32:]
            new_key = hashlib.pbkdf2_hmac(
                'sha256',
                enter_old_password_entry.get().encode('utf-8'),
                salt, 
                100000
            )
            if key == new_key:
                salt = os.urandom(32)
                key = hashlib.pbkdf2_hmac('sha256', enter_new_password_entry.get().encode('utf-8'), salt, 100000)
                storage = salt + key 
                with open('password.hash', 'wb') as file:
                    file.write(storage)
                status = Label(change_password_window, text='Пароль успешно изменён', font=("Arial", 15), fg='#06b800')
                status.grid(column=0, row=3)
            else:
                status = Label(change_password_window, text='Неверный пароль', font=("Arial", 15), fg='#f52c00')
                status.grid(column=0, row=3)
        else:
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', enter_new_password_entry.get().encode('utf-8'), salt, 100000)
            storage = salt + key 
            with open('password.hash', 'wb') as file:
                file.write(storage)
            status = Label(change_password_window, text='Пароль успешно создан', font=("Arial", 15), fg='#06b800')
            status.grid(column=0, row=3)
            btn["state"] = NORMAL
            change_pass_btn.configure(text='Изменить пароль')

    
    change_password_window = Tk()
    change_password_window.title("Изменить пароль")
    change_password_window.geometry("310x200")
    if os.path.exists('password.hash'):
        enter_old_password_lbl = Label(change_password_window, text='Введите старый пароль:', font=("Arial", 15))
        enter_old_password_lbl.grid(column=0, row=0)
        enter_old_password_entry = Entry(change_password_window)
        enter_old_password_entry.grid(column=1, row=0)
    enter_new_password_lbl = Label(change_password_window, text='Введите новый пароль:', font=("Arial", 15))
    enter_new_password_lbl.grid(column=0, row=1)
    enter_new_password_entry = Entry(change_password_window)
    enter_new_password_entry.grid(column=1, row=1)
    ok = Button(change_password_window, text='Изменить пароль', command=_change)
    ok.grid(column=0, row=2)
    status = Label(change_password_window, text='', font=("Arial", 15))
    status.grid(column=0, row=3)


root = Tk()
root.title("Apps-Blocker")
root.geometry('400x350')
locking_is_active = os.path.exists('pid.txt')
info_frame = Frame(root)
button_frame = Frame(root)
if locking_is_active:
    label_locked = Label(info_frame, text='Защита включена', font=("Arial Bold", 20))
    btn = Button(button_frame, text='Отключить защиту', command=disable_locking)
    btn.pack(side=LEFT)
else:
    label_locked = Label(info_frame, text='Защита отключена', font=("Arial Bold", 20))
    btn = Button(button_frame, text='Включить защиту', command=enable_locking)
    btn.pack(side=LEFT)
    if not os.path.exists('password.hash'):
        btn["state"] = DISABLED
if os.path.exists('password.hash'):
    change_pass_btn = Button(button_frame, text='Изменить пароль', command=change_password)
else:
    change_pass_btn = Button(button_frame, text='Задать пароль', command=change_password)
change_pass_btn.pack()
info_frame.pack(side=TOP)
button_frame.pack(side=BOTTOM)
label_locked.pack()
root.mainloop()
