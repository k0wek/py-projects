import random
import pyperclip as pc
import sqlite3
import base64

conn = sqlite3.connect("password-generator/main.db")
cur = conn.cursor()

exit = False
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()*+-./:;<=>?"

def generate_password(len):
    newPassword = None
    for i in range(len):
        rnd = random.choice(chars)
        newPassword += rnd
    return newPassword

def store_password(app, username, password):
    cur.execute("INSERT INTO passwords (app, username, password) VALUES (?, ?, ?)", (app, username, encode_password(password)))
    conn.commit()

def get_password(app):
    res = cur.execute("SELECT password FROM passwords WHERE app=?", (app,))
    x = res.fetchone()
    if x is None:
        print("No password found for " + app)
        return
    else: 
        for i in x:
            password = decode_password(i)
            pc.copy(password)
            print(f"Copied password for {app} to the clipboard. Use CTRL-V to paste the password")   
        return password

def delete_password(app):
    cur.execute("DELETE FROM passwords WHERE app=?", (app,))
    conn.commit()

def list_apps():
    id = 1
    res = cur.execute("SELECT app FROM passwords")
    x = res.fetchall()
    for i in x:
        print(f"{id}: {i[0]}")
        id += 1

def encode_password(password):
    password_bytes = password.encode('ascii')
    base64_bytes = base64.b64encode(password_bytes)
    base64_password = base64_bytes.decode('ascii')
    return base64_password

def decode_password(encoded_password):
    base64_bytes = encoded_password.encode('ascii')
    password_bytes = base64.b64decode(base64_bytes)
    password = password_bytes.decode('ascii')
    return password    

while not exit:
    choice = input("Use 'get'  to get a password, or 'set'  to set a password: ")
    if(choice == "set"):
        app = input("Enter the application/website name: ")
        user = input("Enter the username for this account: ")
        length = input("Length of the password: ")
        if(length.isnumeric()):
            password = generate_password((int(length)))
            store_password(app, user, password)
            pc.copy(password)
            print("Stored the password in the database, it's also copied to the clipboard. Use CTRL-V to paste the password")
        elif length == "x":
            exit = True
        else:
            print("Please enter a number")
    elif(choice == "get"):
        app = input("For which app do you want to request your password?: ")
        get_password(app)
    
    elif(choice == "del"):
        app = input("For which app do you want to delete the password?: ")
        delete_password(app)

    elif(choice == "list"):
        list_apps()