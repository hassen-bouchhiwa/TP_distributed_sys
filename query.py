import socket
import sys
import json
import random

class query:

        def __init__(self, dest_ip,host,f_ip,l_ip,ttl,file):
            self.id= random.randint(10000, 99999)
            self.dest_ip = dest_ip
            self.host = host
            self.f_ip = f_ip
            self.l_ip = l_ip
            self.ttl  = ttl
            self.file = file
        def toString(self):
            stre = json.dumps(self.__dict__)
            return stre
        def send(self):
            q = self.toString()
            try:
                 sock = socket.socket()
            except socket.error as err:
                 print('Socket error because of %s' %(err))
            try:
                sock.connect((self.dest_ip, 1500))
                sock.send(q.encode())
                print('The query ',self.id,' was sent to host ',self.dest_ip)
            except socket.gaierror:
                print('There an error resolving the host')
                sys.exit()
            sock.close()
        def changeID(self,idd):
            self.id = idd
