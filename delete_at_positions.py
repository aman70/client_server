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

    code = 6
    data = {}
    data['code'] = code


    message = input("What palindrome would you like to delete or hit q to exit \n ->")
    try:
        data['message'] = message
        while message != 'q':

            message_to_send = pickle.dumps(data)
            s.send(message_to_send)
            data_rec = s.recv(1024)
            data_rec = data_rec.decode('utf-8')
            print(data_rec)
            print("\n")
            message = input("enter another palindrome to delete or enter q to exit \n ->")
            data['code'] = code
            data['message'] = message
    except:
        s.close()

    print("all _connections have been terminated...bye")

if __name__ == "__main__":
    Main()
