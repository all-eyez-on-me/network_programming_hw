import socket
# Create a socket and connect to CUHK's web server on port 80
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("www.cuhk.edu.hk", 80))
# Create an HTTP request and send it to the server
req = "GET / HTTP/1.1\nHost: www.cuhk.edu.hk\nAccept-Language: en\n\r\n".encode("ascii")
s.sendall(req)
# Read the HTTP response from the server
resp = s.recv(2048)
print(resp)  # "HTTP/1.1 200 OK\r\nServer: 02_1517723009\r\n..."