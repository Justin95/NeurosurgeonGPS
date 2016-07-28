"""
    This file is the Handler that controls the Brain Synonym Server requests

    @author Justin Bonner
"""
#for python 3

import socketserver


class SynonymServerHandler(socketserver.StreamRequestHandler):
    
    
        #this method is specific to the way dictionary keys are represented as a string in python 3
    def formatKeysString(self, keysStr):
        return keysStr.replace("dict_keys(['", "Valid Entries:\n").replace("', '", "\n").replace("'])", "\nEND Valid Entries\n")
    
    
    def getResponce(self, request, brainData):
        if(request == ""):
            return None
        elif(request == "?"):
            return self.formatKeysString(str(brainData.keys()))
        elif(request in brainData.keys()):
            return json.dumps(brainData[clientInput], sort_keys = True, indent = 4)
        else:
            return "Unrecognized Input"
    
    def handle(self):
        brainData = self.getSortedJsonEntries()
        try:
            keepRunning = True
            while(keepRunning):
                print("Handling request from: " + self.client_address)
                request = self.rfile.readline().strip()
                responce = self.getResponce(request, self.brainData)
                if(responce == None):
                    keepRunning = False
                else:
                    self.wfile.write(responce)
                    
        except:
            print("Connection ended with exception")
        
