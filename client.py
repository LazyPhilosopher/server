#!/usr/bin/env python3

import socket

HEADER  = 64
PORT    = 5050
SERVER  = socket.gethostbyname(socket.gethostname())
ADDR    = (SERVER, PORT)
FORMAT  = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" 
FINISHED_MESSAGE   = "!FINISHED"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive():
    running = True
    while running:
        msg_length = client.recv(HEADER).decode(FORMAT)     # receive size of main message
        if(msg_length):
            msg_length = int(msg_length)                    # string to int 
            msg = client.recv(msg_length).decode(FORMAT)    # receiving the message itself
            if(msg == FINISHED_MESSAGE):                  # end of session routine
                running = False
            else:
                print(f"[SERVER]> {msg}\n")

def send(msg):
    message = msg.encode(FORMAT)                        # encoded message iself
    msg_length = len(message)                           # main message length
    send_length = str(msg_length).encode(FORMAT)        # encoded length of main message 
    send_length += b' ' * (HEADER - len(send_length))   # length of size message
    client.send(send_length)
    client.send(message)
    print(f"[CLIENT]> {msg}\n")
    receive()


send("Geologist II")
send("Staff Scientist")
send("Assistant Professor")
send(DISCONNECT_MESSAGE)

