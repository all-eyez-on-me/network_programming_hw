import socket
import sys
from queue import Queue
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
import threading

import logging
from urllib import request

def download(url, i):
    request.urlretrieve(url, "%d.jpg" % i)

def multiProcess(queue):
    MAX_THREADING_NUM = 4
    pool = ThreadPool(MAX_THREADING_NUM)
    if not queue.empty():
        queue_object = queue.get()
        worker = pool.apply_async(server_worker, args=(queue_object(1),
                                                       queue_object(2)))

    pool.close()
    pool.join()


def server_worker(client, address):



def main():
    PROCESS_NUM = 4
    THREADING_NUM = 4

    process_list = []

    # create an INET socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if len(sys.argv) is not 2:
        print("you should set arguments, port number:")

    try:
        server_socket.bind(('localhost', int(sys.argv[1])))
    except:
        print("Cannot set server localhost:%s" % sys.argv[1])
        return 0

    # Control the number of client in queue when listening
    server_socket.listen(20)
    print("Listening for incoming connections on port %s" % sys.argv[1])

    for i in range(PROCESS_NUM):
        p = Process(target=multiProcess, args=(connect_queue, ))
        p.start()
        process_list.append(p)


    connect_queue = Queue()
    # A indefinite loop
    while True:
        # Waiting for connection
        (client_socket, address) = server_socket.accept()
        connect_queue.put((client_socket, address))
        print("Client %s connected" % address[0])
        recieve_string = ""

        # Read data from a client and send it response back
        while True:
            data = client_socket.recv(2048)
            data_decode = data.decode(("utf-8"))
            recieve_string =  recieve_string + data_decode

            # All the message from client is recieved completely
            if recieve_string[-3:] == 'END':
                recieve_string = recieve_string[:-3]
                tokens = nltk.word_tokenize(recieve_string)
                tagged = nltk.pos_tag(tokens)
                print(recieve_string)
                json_data = json.dumps(tagged)
                #print("json %s  " % json_data)
                json_data = json_data.encode('utf-8')
                client_socket.sendall(json_data)
                client_socket.close()
                print("Client disconnected.")
                break

        # Close the socket


if __name__ == '__main__':

