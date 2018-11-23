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

    code = 4
    data = {}
    data['code'] = code


    message = input("print are you sure you want to delete all palindromes? enter y/n or hit q to exit \n ->")
    try:
        while message != 'q':
            if (message == 'y'):
                message_to_send = pickle.dumps(data)
                s.send(message_to_send)
                data_rec = s.recv(1024)
                data_rec = data_rec.decode('utf-8')
                print(data_rec)
                print("\n")
                message = input("would you like to delete palindromes again? enter y/n or enter q to exit \n ->")
            elif(message == 'n'):
                print("OK, not going to delete")
            else:
                print("incorrect option, please input valid option")
                message = input("are you sure you want to delete all palindromes? enter y/n or enter q to exit \n ->")
    except:
        s.close()
    print("terminating connection from client...bye")
if __name__ == "__main__":
    Main()
