"""
    This script initalized a TCPServer with a custom Handler class for dealing with clients.
    It also waits on keyboard input to properly stop the server.

    @author Justin Bonner
"""
#this script is written for python 3, may work in 2
import socketserver
import socket
import jsonReader
from SynonymServerHandler import SynonymServerHandler
from BrainServerThread import BrainServerThread

#the port this server will use
SERVER_PORT = 55555
SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())

#file path to the json file
JSON_FILE_PATH = "brainParts.json" #if the json file must be moved adjust this

reader = jsonReader.JsonReader(JSON_FILE_PATH)
reader.getSortedJsonEntries() #call once to read the file into memory

server = socketserver.TCPServer((SERVER_ADDRESS, SERVER_PORT), SynonymServerHandler)


#create thread to run server
serverThread = BrainServerThread(server)
serverThread.start()


#wait for input and send shutdown signal to server thread
keepRunning = True
while(keepRunning):
    message = input("Type 'END' to shutdown server: ")
    if(message == "END"):
        keepRunning = False

serverThread.shutdown()
