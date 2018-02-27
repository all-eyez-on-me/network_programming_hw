import socket
import sys
import json

import os
# create an INET TCP socket


def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Wait_Flag = False

    # connect to the server (change localhost to an IP address if necessary)
    while True:
        try:
            if len(sys.argv) is not 4:
                print("you should set arguments, server name:localhost ,port number:55703.")
                return 0
            else:
                soc.connect(("localhost", 55703))
                print("Connected to server.")
                break
        except ConnectionRefusedError:
            if Wait_Flag is False:
                print('Cannot connect to server at localhost:55703')
                return 0

    # Send a message to the server

    with open(sys.argv[3]) as f:
        msg = f.read()
    msg = msg + "END"
    print(msg)

    msg = msg.encode("utf-8")
    soc.send(msg)

    # Receive data from the server
    data = soc.recv(1024)
    data = json.loads(data)
    print(data)

    # Always close the socket after use
    soc.close()dddddd


if __name__ == '__main__':
    main()