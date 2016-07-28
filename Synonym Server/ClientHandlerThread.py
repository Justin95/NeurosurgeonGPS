"""
    DEPRECATED WARNING: this class is being phased out, not currently in use
    
    This class is given a client socket and exchanges information in accordance with
    NeurosergeonGPS protocol.
    For the future this will probably be rewritten as part of a
    TCPserver subclass.

    @author Justin Bonner
"""
#for python 3

import threading
import socket
import json

MAX_DATA_PACKET_LENGTH = 4096

class ClientHandlerThread(threading.Thread):
    
    def __init__(self, brainDataDict, clientSocket):
        super(ClientHandlerThread, self).__init__()
        self.brainData = brainDataDict
        self.client = clientSocket
        print("Client Connected: " + self.client.address)

    #this method is specific to the way dictionary keys are represented as a string in python 3
    def formatKeysString(self, keysStr):
        return keysStr.replace("dict_keys(['", "Valid Entries:\n").replace("', '", "\n").replace("'])", "\nEND Valid Entries\n")
    
    
    def handleClientInput(self, clientInput):
        if clientInput == "?":
            return self.formatKeysString(str(self.brainData.keys()))
        if clientInput in self.brainData.keys():
            return json.dumps(self.brainData[clientInput], sort_keys = True, indent = 4)
        return "Unrecognized input"
    
    
    def run(self):
        if self.client is None:
            print("client is null")
            return
        self.client.send("connection accepted".encode())
        try:
            while True:
                order = self.client.recv(MAX_DATA_PACKET_LENGTH).decode()
                toSend = self.handleClientInput(order)
                self.client.send(toSend.encode())
        except Exception as error:
            print("Error: " + str(error))
            return
        print("Client Disconnected: " + self.client.address)
    
    
