import requests
import base64
import socket
import time
import os
from tqdm import tqdm
from art import tprint

file_name = ''

def sendFile(path, file_name, username):

    print(f'Отправка {file_name} пользователю {username}')

    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    chunks, chunk_size = len(encoded_string), len(encoded_string)//10
    x = [encoded_string[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]

    for i in tqdm(range(0, len(x) - 1)):
        r = requests.post("https://tcp-server.228ihackeri228.repl.co/sendFile", json={"key": x[i], "done": False, "username": username})
        print(f"{i + 1} of {len(x)}")
        print(r.status_code, r.reason)
        print(r.text[:300] + '...')

        clear = lambda: os.system('cls')
        clear()

        if str(r.reason) == '500':
            return
        if r.text == 'User not found':
            return
    else:
        r = requests.post("https://tcp-server.228ihackeri228.repl.co/sendFile", json={"key": x[i + 1], "done": True, "filename": file_name, "username": username})
        print(r.status_code, r.reason)
        print(r.text[:300] + '...')

def getFile(file_name):
    r = requests.post("https://tcp-server.228ihackeri228.repl.co/getFile", json={"filename": file_name, "username": socket.gethostname()})
    with open(file_name, "wb") as fh:
        fh.write(base64.decodebytes(str.encode(r.text)))

def getFileName():
    r = requests.post("https://tcp-server.228ihackeri228.repl.co/getFileName", json={"username": socket.gethostname()})
    print("Get " + r.text[0:100] + "...")
    return r.text

def getInfo():
    r = requests.post("https://tcp-server.228ihackeri228.repl.co/info", json={"username": socket.gethostname()})
    print(r.text)
    if r.text == "True":
        file_name = getFileName()
        getFile(file_name)

# sendFile('LeviathanBackground2.png', 'localhost')
if __name__ == '__main__':
    tprint('|xFILEx|')
    r = requests.get("https://tcp-server.228ihackeri228.repl.co/users")
    data = r.json()
    users = ''

    for key, value in data.items():
        users += f'\n{key}'

    s_o = ''

    while (s_o.lower() != 'о') and (s_o.lower() != 'п'):
        s_o = input('Отправить или получить?(О/п)')

    if s_o.lower() == 'п':
        while True:
            getInfo()
    else:

        print(f'Доступные пользователи:{users}')

        path = input('Путь к файлу: ')
        user = input('Имя пользователя: ')

        sendFile(path, path.split('\\')[-1], user)
