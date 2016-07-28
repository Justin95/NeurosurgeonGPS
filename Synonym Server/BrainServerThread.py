"""
    This class is used to run the server while the main thread listens for a close signal.

    @author Justin Bonner
"""
#for python 3
import threading


class BrainServerThread(threading.Thread):
    
    def __init__(self, server):
        super(BrainServerThread, self).__init__()
        self.server = server
    
    
    def shutdown(self):
        print("Attempting Server Shutdown")
        self.server.shutdown()
    
    
    
    def run(self):
        self.server.serve_forever()
        print("Closing Server")
