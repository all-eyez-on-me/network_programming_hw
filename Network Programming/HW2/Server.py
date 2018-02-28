import socket
import sys
from multiprocessing import Process, Queue
import threadpool
import logging
from urllib import request

import json
import nltk
import ipdb



def download(url, i):
    request.urlretrieve(url, "%d.jpg" % i)

def multiProcess(i, connect_queue):

    MAX_THREADING_NUM = 4
    pool = threadpool.ThreadPool(MAX_THREADING_NUM)


    logger = logging.getLogger(str(i))
    formatter = logging.Formatter(
        "  [%(levelname)s] : %(message)s")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    ch.setFormatter(formatter)



    logger.info("go into while loop")
    while(True):
        if not connect_queue.empty():
            #logger.info("queue.empty, %d", connect_queue.empty())
            print("creating thread")
            (q_socket, q_address) = connect_queue.get(block=True)
            dic_vars = {'process_id': i, 'client_socket': q_socket, 'address': q_address}
            reqs = threadpool.makeRequests(server_worker, args_list=[(dic_vars,None),])
            for req in reqs:
                pool.putRequest(req)





def server_worker(process_id, client_socket, address):
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        "Process %(i)s thread%(name)s, [%(levelname)s] : %(message)s")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    ch.setFormatter(formatter)

    print("go into thread")
    recieve_string = ""

    # Read data from a client and send it response back
    while True:
        data = client_socket.recv(2048)
        data_decode = data.decode(("utf-8"))
        recieve_string = recieve_string + data_decode

        # All the message from client is recieved completely
        if recieve_string[-3:] == 'END':
            recieve_string = recieve_string[:-3]
            tokens = nltk.word_tokenize(recieve_string)
            tagged = nltk.pos_tag(tokens)
            print(recieve_string)
            json_data = json.dumps(tagged)
            # print("json %s  " % json_data)
            json_data = json_data.encode('utf-8')
            client_socket.sendall(json_data)
            client_socket.close()
            print("Client disconnected.")
            break


def main():

    PROCESS_NUM = 4
    THREADING_NUM = 4


    process_list = []

    # Setting logger
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        "%(name)s, [%(levelname)s] : %(message)s")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # create an INET socket in main thread
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # parsing the argument
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

    # A Global queue with connect clients
    connect_queue = Queue()
    # Create Multi-Process
    for i in range(PROCESS_NUM):
        p = Process(target=multiProcess, args=(i, connect_queue,))
        p.start()
        process_list.append(p)


    # A indefinite loop
    while True:
        # Waiting for connection

        (client_socket, address) = server_socket.accept()
        connect_queue.put((client_socket, address))
        logger.info("queue number %d", connect_queue.qsize())
        logger.info("Client %s connected" % address[0])

if __name__ == '__main__':
    main()
