import socket
import sys
from multiprocessing import Process, Queue
import threadpool
import logging
from urllib import request
import os
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.preprocessing import image
import tensorflow as tf

def server_worker(client_socket, address, tf_graph, pic_num):

    logger = logging.getLogger('logger'+str(pic_num))
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s], [%(levelname)s], [%(processName)s], [%(threadName)s] :  %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Recieve Client ('%s', %s)." % (address[0], address[1]))

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

    logger.info("finish download")

    with tf_graph.as_default():
        model = SqueezeNet()
        img = image.load_img('images/1.jpg', target_size=(227, 227))
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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s], [%(levelname)s], [%(processName)s], [%(threadName)s] :  %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("start")
    # bind the socket to the host and a port
    server_socket.bind(('localhost', int(sys.argv[1])))

    # Listen for incoming connections from clients
    server_socket.listen(10)

    if not (os.path.isdir("images/")):
        os.mkdir('images')

    graph = tf.get_default_graph()
    pic_num = 0
    while True:

        (client_socket, address) = server_socket.accept()
        logger.info("Client ('%s', %s) connected." % (address[0], address[1]))
        server_worker(client_socket, address, graph, pic_num)



if __name__ == '__main__':
    main()
