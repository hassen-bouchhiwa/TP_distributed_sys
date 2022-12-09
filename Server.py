import socket
import json
from query import query
import os
import time

ips = {
  "A": '192.168.122.1',
  "B": "192.168.122.33",
  "C": '192.168.122.206',
  "D": '192.168.122.178',
  "E": '192.168.122.',
  "F": '192.168.122.',
  "G": '192.168.122.',
}
 
def sendFile(IP,fichier):
    PORT = 4455
    ADDR = (IP, PORT)
    FORMAT = "utf-8"
    SIZE = 1024
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    """ Connecting to the server. """
    client.connect(('192.168.122.33',4455))
    fichier1='ftp/'+fichier
    """ Opening and reading the file data. """
    file = open(fichier1, "r")
    data = file.read()
 
    """ Sending the filename to the server. """
    client.send(fichier.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
 
    """ Sending the file data to the server. """
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
 
    """ Closing the file. """
    file.close()
 
    """ Closing the connection from the server. """
    client.close()


neighbours = ['B','C','D']
directory = '/home/hassen/repartis/ftp/'
ids = []
sock = socket.socket()


port = 1500
sock.bind(('', port))
sock.listen(5)

print('Listener is running ...')
print('***********------------------************')

while True:
    c, addr = sock.accept()

    jsonReceived = c.recv(1024)
    #print("Json received -->", jsonReceived)
    q = json.loads(jsonReceived)
    if(  (int(q['ttl'])<1) ):
        print('No more ttl')
        print('***********------------------************')
        continue
    if (q['id'] in ids):
        print('Query already handeled, dropping now ..')
        print('***********------------------************')
        continue
    ids.append(q['id'])
    file = directory + q['file']
    print('The host ',q['host'],' asked to download the file ',q['file'])
    
    if(os.path.exists(file)):
        time.sleep(2)
        print('sending file to ',q['host'])
        sendFile(q['f_ip'],q['file'])
    else:
        print('File was not found locally - - -')
        for host in neighbours:
            if(ips[host]!=q['l_ip'] and ips[host]!=q['f_ip']):
                query1 = query(ips[host],q['host'],q['f_ip'],'192.168.122.1',int(q['ttl'])-1,q['file'])
                query1.changeID(q['id'])
                try:
                    query1.send()
                except socket.gaierror:
                    print('host is not up')
    print('***********------------------************')
    c.close()
