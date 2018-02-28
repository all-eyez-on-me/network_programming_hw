
import socket
import sys
from multiprocessing import Process, Queue, Lock, Value
import threadpool
import logging
from urllib import request
import os
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.preprocessing import image
import tensorflow as tf




def download(url, i):
    request.urlretrieve(url, "%d.jpg" % i)

def multiProcess(connect_queue, graph, pic_num, lock, process_id):

    MAX_THREADING_NUM = 4
    pool = threadpool.ThreadPool(MAX_THREADING_NUM)

    try:
        while(True):
            (q_socket, q_address) = connect_queue.get()
            lock.acquire()
            _pic_num = pic_num.value + 1
            pic_num.value =  _pic_num
            lock.release()

            dic_vars = {'client_socket': q_socket, 'address': q_address, 'tf_graph':graph, 'pic_num':_pic_num, }
            #print("get the address %s %s"%(q_address[0], q_address[1]))
            reqs = threadpool.makeRequests(server_worker, args_list=[(None, dic_vars),])
            for req in reqs:
                pool.putRequest(req)
    except:
        print("counter except, exit the process-%d" %(process_id))
        pool.joinAllDismissedWorkers()





def server_worker(client_socket, address, tf_graph, pic_num):

    logger = logging.getLogger('logger'+str(pic_num))
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(processName)s], [%(threadName)s] :  %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Recieved Client ('%s', %s)." % (address[0], address[1]))

    recieve_string = ""

    # Read data from a client and send it response back
    while True:
        #print(client_socket)
        data = client_socket.recv(2048)
        data_decode = data.decode(("utf-8"))
        recieve_string = recieve_string + data_decode
        # All the message from client is recieved completely
        if recieve_string.find("[END]") != -1:
            break
    recieve_string= recieve_string[:-5]
    logger.info("Client submitted URL %s" % recieve_string)
    request.urlretrieve(recieve_string, "images/%d.jpg" % pic_num)

    logger.info("Image saved to images/%d.jpg" %(pic_num))
    with tf_graph.as_default():
        model = SqueezeNet()
        image_str = "images/" + str(pic_num) + ".jpg"
        img = image.load_img(image_str, target_size=(227, 227))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        result =  decode_predictions(preds)
        #print('Predicted:', result)
        result = result[0][0]

    logger.info("SqueezeNet result: (\"%s\", %.3f)" % (result[1], result[2]))
    result = [result[1], str(result[2])]
    result_string = ';'.join(result)
    client_socket.sendall(result_string.encode("utf-8"))
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
    logger.info("Client connection closed")
    del logger



def main():

    PROCESS_NUM = 4
    THREADING_NUM = 4
    LISTENING_NUM = 20


    process_list = []

    # Setting logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] :  %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # create an INET socket in main thread
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # parsing the argument
    if len(sys.argv) is not 3:
        logger.error("you should set arguments, port number, the number of processor:")

    try:
        server_socket.bind(('localhost', int(sys.argv[1])))
        PROCESS_NUM = int(sys.argv[2])
    except:
        logger.error("Cannot set server localhost:%s" % sys.argv[1])
        return 0

    # Control the number of client in queue when listening
    server_socket.listen(LISTENING_NUM)
    logger.info("Start listening for connections on port %s" % sys.argv[1])

    # A Global queue with connect clients
    connect_queue = Queue()
    lock = Lock()
    pic_num = Value('i', 0)

    graph = tf.get_default_graph()

    # Create Multi-Process
    for i in range(PROCESS_NUM):
        p = Process(target=multiProcess, args=(connect_queue, graph, pic_num, lock, i, ))
        logger.info("Created process Process-%d" % (i + 1))
        p.start()


    if not (os.path.isdir("images/")):
        os.mkdir('images')



    # A indefinite loop
    while True:
        # Waiting for connection

        (client_socket, address) = server_socket.accept()
        connect_queue.put((client_socket, address))
        logger.info("Client ('%s', %s) connected." % (address[0], address[1]))

if __name__ == '__main__':
    main()
