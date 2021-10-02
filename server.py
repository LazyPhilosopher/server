#!/usr/bin/env python3

import socket, threading, func, json, time

HEADER  = 64
PORT    = 5050
SERVER  = socket.gethostbyname(socket.gethostname())
ADDR    = (SERVER, PORT)
FORMAT  = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" 
FINISHED_MESSAGE   = "!FINISHED"

mydb = func.commence_db_connection("localhost", "admin", "Sharicho_3718")
mycursor = mydb.cursor()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send(conn, msg):
    message = msg.encode(FORMAT)    # encoded message iself
    msg_length = len(message)       # main message length
    send_length = str(msg_length).encode(FORMAT)    # encoded length of main message 
    send_length += b' ' * (HEADER - len(send_length)) # length of size message
    conn.send(send_length)
    conn.send(message)

def handle_client(conn, addr, lock):
    print(f"[SERVER]> {addr} connected.")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)   # receive size of main message
        if(msg_length):
            msg_length = int(msg_length)    # string to int 
            msg = conn.recv(msg_length).decode(FORMAT)  # receiving the message itself
            if(msg == DISCONNECT_MESSAGE):  # end of session routine
                connected = False
            else:
                print(f"[{addr}]> {msg}")
            #send(conn, "Message was received")
            
            lock.acquire()
            response = func.get_employee_by_job(mycursor, msg)
            lock.release()

            for i in range(len(response)):
                temp_json = json.dumps(response[i])
                #time.sleep(10)
                send(conn, temp_json)
            send(conn, FINISHED_MESSAGE)
                #print(temp_json)
    conn.close()

def start():
    lock = threading.Lock()
    server.listen()
    while True:
        print(f"[SERVER]> Listening on {ADDR}...")
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, lock))
        thread.start()
        #print(f"[SERVER]> Now active threads: {threading.active_count() - 1}")


print(f"[SERVER]> Server is starting...")
start()
            