"""
    This script is responcible for listening for connecting clients and
    starting a new clientHandler thread for each connected client.
    For the future this may be implimented by extending python's
    TCPserver class for more flexability.

    @author Justin Bonner
"""
#this script is written for python 3, may work in 2
import socket
from jsonReader import getSortedJsonEntries
from ClientHandlerThread import ClientHandlerThread

#the port this server will use
SERVER_PORT = 55555

brainData = getSortedJsonEntries()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))
serverSocket.bind((socket.gethostbyname(socket.gethostname()), SERVER_PORT))
serverSocket.listen(4)

keepRunning = True
while keepRunning:
    print("Listening for clients")
    (client, address) = serverSocket.accept()
    clientThread = ClientHandlerThread(brainData, client)
    clientThread.run()
    print("Client Connected from " + str(address))

serverSocket.close()
