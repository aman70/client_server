import socket
import sqlite3
from threading import Thread
import pickle
import sys

def Main():

    palindrome_dict = {}
    palindrome_list = []
    host = "localhost"
    port = 5000
    print("Binding .....")
    s = socket.socket() #create a scoket object
    s.bind((host,port))
    s.listen(1) #listen for one connection at a time
    print("listening .....")

    while True:
        c, addr = s.accept()  # we have accepted a connection
        print("Connection from: " + str(addr))
        data = c.recv(1024)
        if not data:
            print("breaking because no data received")
            break;
        data_1 = pickle.loads(data)
        print(data_1)
        threads = []
        if data_1['code'] == 0: #check if palindrome, and if it is a palindrome put it in
            threads.append(Thread(target = check_palindrome, daemon = True, args = (c, addr,data_1,palindrome_dict,palindrome_list)))
            threads[-1].start()
        if data_1['code'] == 1: #get count of a palindrome in a set
            threads.append(Thread(target = get_count, daemon = True, args = (c, addr,data_1,palindrome_dict)))
            threads[-1].start()
        if data_1['code'] == 2: #get count of all unique palindromes in the set
            threads.append(Thread(target = get_all_count, daemon=True, args = (c, addr,data_1,palindrome_dict)))
            threads[-1].start()
        if data_1['code'] == 3:  #get a stream of palindromes
            threads.append(Thread(target = get_palindromes, args = (c, addr,data_1,palindrome_dict,palindrome_list)))
            threads[-1].start()
        if data_1['code'] == 4:   #delete all palindromes
            threads.append(Thread(target = delete_all, args = (c, addr,data_1,palindrome_dict,palindrome_list)))
            threads[-1].start()
        if data_1['code'] == 5: #get a stream of all palindromes
            threads.append(Thread(target = get_palindromes, args = (c, addr,data_1,palindrome_dict,palindrome_list,"None")))
            threads[-1].start()
        if data_1['code'] == 6:   #delete all palindromes
            threads.append(Thread(target = delete_all, args = (c, addr,data_1,palindrome_dict,palindrome_list,0)))
            threads[-1].start()
        if data_1['code'] == 8: #check if palindrome, and if it is a palindrome put it in
            print(" I am here ")
            threads.append(Thread(target = check_palindrome_list, daemon = True, args = (c, addr,data_1,palindrome_dict,palindrome_list)))
            threads[-1].start()
        if data_1['code'] == 7:   #terminate connection with server
            for i in threads:
               i.join()
            print("all connections terminated")
            data_return = "all connections have been terminated"
            c.send(data_return.encode('utf-8'))
            sys.exit(1)


    s.close()

def get_all_count(clientsocket,addr,data,palindrome_dict):
    while True:

        if palindrome_dict != {}:
            data_return = len(palindrome_dict.keys())
            data_return = "the number of palindromes in the ledger are: {}".format(str(data_return))
        else:
            data_return = "Sorry no palindromes exist in the ledger yet"
        clientsocket.send(data_return.encode('utf-8'))
        data = clientsocket.recv(1024)
        data = pickle.loads(data)

def get_palindromes(clientsocket,addr,data,palindrome_dict,palindrome_list,flag="all"):
    while True:
        if flag is not "all":
            if len(palindrome_list) > 0:
                data_return = pickle.dumps([palindrome_list[-1]])
            else:
                data_return = pickle.dumps([])
        else:
            data_return = pickle.dumps(list(palindrome_dict.keys()))
        clientsocket.send(data_return)
        data = clientsocket.recv(1024)
        data = pickle.loads(data)

def get_count(clientsocket, addr,data,palindrome_dict):



    while True:



        if not data:  # if there is no data
            break;
        if data['message'] in palindrome_dict.keys():
            data_return = palindrome_dict[data['message']]
            data_return = "data has been injected in the ledger {} times".format(str(data_return))
        else:
            data_return = "Sorry the palindrome does not exist yet"
        clientsocket.send(data_return.encode('utf-8'))
        data = clientsocket.recv(1024)
        data = pickle.loads(data)

def delete_all(clientsocket, addr,data,palindrome_dict,palindrome_list,flag = 1):

    if flag == 1:
        if len(palindrome_list) > 0:
            palindrome_dict.clear()
            palindrome_list = []
            data_return ="the ledger has been cleared out"
            print(data_return)
        else:
            data_return = "the ledger was already empty"
        clientsocket.send(data_return.encode('utf-8'))

    else:
        while True:
            content = data['message']
            if content in palindrome_dict.keys():
                del palindrome_dict[content]
                palindrome_list.remove(content)
                data_return = "palindrome {} has been removed from the ledger".format(content)
                print(data_return)
            else:
                data_return = "this item does not exist in the ledger and hence cannot be removed from the ledger"

            clientsocket.send(data_return.encode('utf-8'))
            data = clientsocket.recv(1024)
            data = pickle.loads(data)








def check_palindrome_list(clientsocket,addr,data,palindrome_dict,palindrome_list):
    while True:

        #do some checks and if msg == someWeirdSignal: break:
        if not data:  # if there is no data
            break;
        # print("data['message")
        word_list = data['message']
        data_return_global = []
        for i,v in enumerate(word_list):
            print("word {} received from user: {}".format(i,v))
            print("Checking if {} is a Palindrome  \n".format(v))
            yn = isPalindrome(v)

            if yn:
                data_return_local = "{} is a palindrome".format(v)
                data_return_global.append(data_return_local)
                # if flag == 1:
                #     dbc.execute("REPLACE INTO palindrome_ledger VALUES (?)", (data,))
                # else:  #if the flag is zero we will create a global dictionary and write to it
                if v not in palindrome_dict.keys():
                    palindrome_dict[v] = 1
                    palindrome_list.append(v)
                else:
                    palindrome_dict[v] += 1
            else:
                data_return_local = "Sorry {} is not a Pallindrome".format(v)
                data_return_global.append(data_return_local)

        data_return_global_2 = pickle.dumps(data_return_global)
        clientsocket.send(data_return_global_2)
        data = clientsocket.recv(1024)
        data = pickle.loads(data)


    clientsocket.close()



def check_palindrome(clientsocket,addr,data,palindrome_dict,palindrome_list):


    # if flag == 1:
    #     conn, dbc = create_database()

    while True:

        #do some checks and if msg == someWeirdSignal: break:
        if not data:  # if there is no data
            break;
        # print("data['message")
        print("From Connected user: " + data['message'])
        print("Checking if it is a Palindrome")
        yn = isPalindrome(data['message'])

        if yn:
            data_return = "A pallindrome was found"
            # if flag == 1:
            #     dbc.execute("REPLACE INTO palindrome_ledger VALUES (?)", (data,))
            # else:  #if the flag is zero we will create a global dictionary and write to it
            if data['message'] not in palindrome_dict.keys():
                palindrome_dict[data['message']] = 1
                palindrome_list.append(data['message'])
            else:
                palindrome_dict[data['message']] += 1
        else:
            data_return = "Sorry not a Pallindrome"
        clientsocket.send(data_return.encode('utf-8'))
        data = clientsocket.recv(1024)
        data = pickle.loads(data)


    clientsocket.close()

def reverse(s):
    return s[::-1]

def isPalindrome(s):
    # Calling reverse function
    rev = reverse(s)

    # Checking if both string are equal or not
    if (s == rev):
        return True
    return False


if __name__ == "__main__":
    Main()
