import socket
import sqlite3
import threading
import pickle
import sys
import os
import time

def  Main():
    host = "localhost"
    port = 5000

    s =  socket.socket()
    s.connect((host,port))

    code = 7
    data = {}
    data['code'] = code


    message = input("are you sure you want to terminate all connections with the client? enter y or n \n ->")

    while True:
        try:
            if (message == 'y'):
                message_to_send = pickle.dumps(data)
                s.send(message_to_send)
                data_rec = s.recv(1024)
                data_rec = data_rec.decode('utf-8')
                print(data_rec)
                print("\n")
            elif(message == 'n'):
                print("OK, not going to delete")
            else:
                print("incorrect option, please input valid option")
                message = input("are you sure you want to terminate all connections with the client? enter y or no \n ->")
        except:
            s.close()

    print("all _connections have been terminated...bye")
    # s.close()

if __name__ == "__main__":
    Main()