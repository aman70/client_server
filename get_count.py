import socket
import sqlite3
import threading
import pickle
import sys

import time

def  Main():
    host = "localhost"
    port = 5000

    s =  socket.socket()
    s.connect((host,port))

    code = 2
    data = {}
    data['code'] = code

    try:

        while True:
            try:
                message_to_send = pickle.dumps(data)
                s.send(message_to_send)
                data_rec = s.recv(1024).decode('utf-8')
                print("Received from server: " + data_rec)
            except KeyboardInterrupt:
                print("[CTRL+C detected]")
                sys.exit()
            time.sleep(20)
    except:
        s.close()

    print("all _connections have been terminated...bye")


if __name__ == "__main__":
    Main()
