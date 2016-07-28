#this is just a test client for server testing

#python 3

import socket

PORT = 55555
MAX_DATA_SIZE = 4096
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Attempting Connection")
sock.connect(('72.84.110.148', PORT))
print("Connected")

try:
    
    #print(sock.recv(MAX_DATA_SIZE).decode())
    
    sock.send('?'.encode())
    
    print(sock.recv(MAX_DATA_SIZE).decode())
    
    sock.send('pons'.encode())
    
    print(sock.recv(MAX_DATA_SIZE).decode())
    
    sock.close()
except Exception as err:
    print("client error: " + str(err))
