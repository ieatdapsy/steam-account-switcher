"""
Steam logo icon used was created by Jackson @ https://findicons.com/icon/607299/steam
"""

from db import SimpleDataBase
import os
import tkinter as tk
from tkinter import ttk

DATABASE_NAME = 'sasdb.json'


db = SimpleDataBase(DATABASE_NAME, 'encryptme')


def add_account():
    account_nickname = add_account_tab_username_entry.get()
    if db.exists(account_nickname):
        return False
    password = add_account_tab_password_entry.get()
    db.set_key(account_nickname, {'username': account_nickname,
                                  'password': db.encrypt_key(password)})

    update_options()


def remove_account():
    username = login_tab_selected.get()
    if username in db.db:
        db.remove_key(username)
        update_options()


def login():
    username = login_tab_selected.get()
    if username in db.db:
        os.system('taskkill /f /im steam.exe')
        command = "start \"\" \"C:\\Program Files (x86)\\Steam\\steam.exe\" -login " +\
                  f"{username} {db.decrypt_key(db.db[username]['password'])}"
        os.system(command)


def update_options():
    global options
    menu = login_tab_drop_down['menu']
    menu.delete(0, tk.END)
    keys = db.get_all_keys()
    if len(keys):
        for name in keys:
            menu.add_command(label=name, command=lambda added_name=name:login_tab_selected.set(added_name))
        login_tab_selected.set(options[0])
    else:
        options = db.get_all_keys() or ['No accounts added']
        login_tab_selected.set(options[0])


window = tk.Tk()
window.title('SAS')
window.geometry('200x120')
window.resizable(0, 0)
try:
    window.iconbitmap('.\\steam1.ico')
except Exception as e:
    print(e)


notebook_parent = ttk.Notebook(window)

login_tab = ttk.Frame(notebook_parent)
login_tab_selected = tk.StringVar(login_tab)
options = db.get_all_keys() or ['No accounts added']
login_tab_drop_down = tk.OptionMenu(login_tab, login_tab_selected, *options)
login_tab_selected.set(options[0])
login_tab_drop_down.grid(column=0, row=0)
login_tab_drop_down.config(width=15)
login_tab_login_button = tk.Button(login_tab, text='Login', command=login)
login_tab_login_button.grid(column=0, row=1, sticky=tk.W)
login_tab_remove_button = tk.Button(login_tab, text='remove', command=remove_account)
login_tab_remove_button.grid(column=0, row=2, sticky=tk.W)


add_account_tab = ttk.Frame(notebook_parent)
add_account_tab_label_username = tk.Label(add_account_tab, text='Username')
add_account_tab_label_username.grid(column=0, row=1)
add_account_tab_username_entry_text_var = tk.StringVar()
add_account_tab_username_entry = tk.Entry(add_account_tab)
add_account_tab_username_entry.grid(column=1, row=1)
add_account_tab_label_password = tk.Label(add_account_tab, text='Password')
add_account_tab_label_password.grid(column=0, row=2)
add_account_tab_password_entry = tk.Entry(add_account_tab)
add_account_tab_password_entry.grid(column=1, row=2)
add_account_tab_save_button = tk.Button(add_account_tab, text='Save', command=add_account)
add_account_tab_save_button.grid(column=0, row=3)


notebook_parent.add(login_tab, text='Select account')
notebook_parent.add(add_account_tab, text='Add account')
notebook_parent.pack(expand=1, fill='both')


window.mainloop()
