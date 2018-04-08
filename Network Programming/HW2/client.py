import socket
import sys
import logging



def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Wait_Flag = False
    
    
    # Setting logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] :  %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # connect to the server (change localhost to an IP address if necessary)
    while True:
        try:
            if len(sys.argv) is not 4:
                logger.error("you should set arguments, server name:localhost ,port number:55703.")
                return 0
            else:
                soc.connect((sys.argv[1], int(sys.argv[2])))
                logger.info("Connected to server at (%s, %s)" % (sys.argv[1], sys.argv[2]))
                break
        except ConnectionRefusedError:
            if Wait_Flag is False:
                logger.error("Cannot Connected to server at (%s, %s)" % (sys.argv[1], sys.argv[2]))
                return 0

    # Send a message to the server

    msg = sys.argv[3]
    msg = msg + "[END]"
    #logger.info(msg)

    msg = msg.encode("utf-8")
    soc.send(msg)
    logger.info("URL sent to the server")

    # Receive data from the server
    rec = soc.recv(1024)
    rec = rec.decode('utf-8')
    rec_list = rec.split(';')
    logger.info("Server response: (\'%s\', %f)" % (rec_list[0], float(rec_list[1])))

    # Always close the socket after use
    soc.close()


if __name__ == '__main__':
    main()