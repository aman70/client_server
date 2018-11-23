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

    code = 3
    data = {}
    data['code'] = code

    while True:
        try:

            message_to_send = pickle.dumps(data)
            s.send(message_to_send)
            data_rec = s.recv(1024)
            data_rec = pickle.loads(data_rec)

            if not len(data_rec) == 0:
                print("printing all unique palindromes in the ledger")
                print(*data_rec, sep="\n")
                print("\n")
            else:
                print("The ledger is empty")

        except KeyboardInterrupt:
            print("[CTRL+C detected]")
            sys.exit()
        time.sleep(20)

    print("terminating connection from client...bye")
    s.close()


if __name__ == "__main__":
    Main()
