import socket
import sqlite3
import threading
import pickle




def  Main():
    host = "localhost"
    port = 5000

    s =  socket.socket()
    s.connect((host,port))

    message = input("->")
    code = 1
    data = {}
    data['message'] = message
    data['code'] = code

    while message != 'q':
        message_to_send = pickle.dumps(data)
        s.send(message_to_send)
        data_rec = s.recv(1024).decode('utf-8')
        print("Received from server: " + data_rec)
        message = input("->")

        data['message'] = message
        data['code'] = code

    s.close()


if __name__ == "__main__":
    Main()
