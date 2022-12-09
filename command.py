import socket
import sys
import json
import random
import sys
from query import query

ips = {
        '192.168.122.1' : 'A',
        "192.168.122.33" : 'B',
        '192.168.122.206' : 'C',
        '192.168.122.178' : 'D',
        '192.168.122.64': 'E',
        '192.168.122.55': 'F',
}

command = query('192.168.122.1','B','192.168.122.33','192.168.122.33',3,sys.argv[1])
command.send()


IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
""" Server has accepted the connection from the client. """
""" Bind the IP and PORT to the server. """
server.bind(ADDR)

""" Server is listening, i.e., server is now waiting for the client to connected. """
server.listen()
print("Searching for file ...")
conn, addr = server.accept()
print("File found in host ",ips[addr[0]])

""" Receiving the filename from the client. """
filename = conn.recv(SIZE).decode(FORMAT)
print(f"[RECV] Receiving the filename.")
file = open(filename, "w")
conn.send("Filename received.".encode(FORMAT))

""" Receiving the file data from the client. """
data = conn.recv(SIZE).decode(FORMAT)
print(f"[RECV] Receiving the file data.")
file.write(data)
conn.send("File data received".encode(FORMAT))

""" Closing the file. """
file.close()

""" Closing the connection from the client. """
