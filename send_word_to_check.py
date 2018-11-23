import socket
import sqlite3
import pickle

def  Main():
    host = "localhost"
    port = 5000

    # s1 =  socket.socket()
    # s1.connect((host,port))

    s2 =  socket.socket()
    s2.connect((host,port))

    message = input("input word or words separated by space to check \n->")
    code_2 =  8
    data =  {}
    word_list =  message.split()
    # if len(word_list) == 1:
    #     data['message'] = word_list[0]
    #     data['code'] = code_1
    # else:
    data['message'] = word_list
    data['code'] = code_2

    try:
        while message != 'q':#this is the user input
            message_to_send = pickle.dumps(data)

            # if data['code'] == code_1:
            #     s1.send(message_to_send)
            #     data_rec = s1.recv(1024).decode('utf-8')

            # if data['code'] == code_2:
            s2.send(message_to_send)
            data_rec = s2.recv(1024)
            data_rec = pickle.loads(data_rec)

            for i in data_rec:
                print(i)
            print("\n")
            message = input("input word or words separated by space to check \n->")

            word_list =  message.split()

            # if len(word_list) == 1:
            #
            #     data['message'] = word_list[0]
            #     data['code'] = code_1

            # else:
            data['message'] = word_list
            data['code'] = code_2


    except:
        # s1.close()
        s2.close()
    print("all _connections have been terminated...bye")
    # s1.close()
    # s2.close()


if __name__ == "__main__":
    Main()
