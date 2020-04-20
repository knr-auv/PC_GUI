import asyncio, socket, struct, random, time

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8080       # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = struct.pack('iiiii',random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100))
        s.sendall(message)
        time.sleep(0.5)
   




