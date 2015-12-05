import socket
import threading
import time
from Queue import *

instructions=("1:1", "1:2", "1:3", "1:4", "1:s")#, "1:o", "1:c", "1:5", "1:6", "1:5")

ack = Queue(100)

class Sender(threading.Thread):
    def __init__(self):
        self.iter = 1
        self.clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket1.connect(('localhost', 8089))
             
        super(Sender, self).__init__()
    def run(self):
        for elem in instructions:
            self.clientsocket1.send(elem)
            print elem 
            if elem == "1:o":
                time.sleep(3)
                
            while ack.empty(): 
                pass
            ack.get()    


 
class Listener(threading.Thread):
    def __init__(self):
        self.clientsocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       
        self.clientsocket2.connect(('localhost', 8090))
                
        super(Listener, self).__init__()
    def run(self):
        while True:
            buf = self.clientsocket2.recv(64)
            if len(buf) > 0:
                print buf
                if buf[2] == 'a':
                    ack.put_nowait(buf)
            
    

sender = Sender()
sender.start()
listener = Listener()
listener.start()
