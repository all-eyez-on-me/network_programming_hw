import socket
import sys
import json
import nltk


def main():
    # create an INET socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if len(sys.argv) is not 2 or int(sys.argv[1]) is not 55703:
        # bind the socket to the host and a port
        server_socket.bind(("localhost", 55703))

    # Listen for incoming connections from clients
    server_socket.listen(10)

    # A indefinite loop
    while True:
        # accept connections from outside
        (client_socket, address) = server_socket.accept()
        recieve_string = ""

        # Read data from client and send it back
        while True:
            data = client_socket.recv(12)
            data_decode = data.decode(("utf-8"))
            recieve_string =  recieve_string + data_decode
            if recieve_string[-3:] == 'END':
                recieve_string = recieve_string[:-3]
                tokens = nltk.word_tokenize(recieve_string)
                tagged = nltk.pos_tag(tokens)
                #print("Received %s  " % recieve_string)
                json_data = json.dump(tagged)
                client_socket.sendall(json_data)
                client_socket.close()
                break

        # Close the socket


if __name__ == '__main__':
    main()