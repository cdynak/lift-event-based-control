import threading
import time
from Tkinter import *
from elevator import *
import socket
from _elementtree import tostring
import random


class MoveLift(threading.Thread):
    def __init__(self, elevator_object, floor_no, moving_time, queue):
        self.elevator = elevator_object
        self.floor = floor_no
        self.m_time = moving_time
        self.queue_out = queue
        super(MoveLift, self).__init__()
    
    def run(self):
        if self.elevator.actual_floor < self.floor:
            state = "moveup"
        else:
            state = "movedown"         
        self.elevator.floors[self.elevator.actual_floor].setState(state)
        self.elevator.setState(state)
        time.sleep(self.m_time)
        self.elevator.actual_floor = self.floor
        self.elevator.UpdateLift(state)
        self.sendACK()
            
    def sendACK(self):
        message = "%d:%s" % (self.elevator.id+1, "a")
        self.queue_out.put_nowait(message)


class StopLift(threading.Thread):
    def __init__(self, elevator_object, breaking_time, queue):
        self.elevator = elevator_object
        self.b_time = breaking_time 
        self.queue_out = queue
        super(StopLift, self).__init__()
        
    def run(self):
        self.elevator.floors[self.elevator.actual_floor].setState("stay")
        time.sleep(self.b_time)
        self.elevator.setState("stay")
        self.sendACK()
        
    def sendACK(self):
        message = "%d:%s" % (self.elevator.id+1, "a")
        self.queue_out.put_nowait(message)    
     
        
class OpenDoors(threading.Thread):
    def __init__(self, elevator_object, openning_time, queue):
        self.elevator = elevator_object
        self.o_time = openning_time
        self.queue_out = queue
        super(OpenDoors, self).__init__()

    def run(self):
        self.elevator.setState("open")
        time.sleep(self.o_time)
        self.elevator.floors[self.elevator.actual_floor].setState("open")
        self.sendACK()
        
    def sendACK(self):
        message = "%d:%s" % (self.elevator.id+1, "a")
        self.queue_out.put_nowait(message)         

class CloseDoors(threading.Thread):
    def __init__(self, elevator_object, closing_time, queue):
        self.elevator = elevator_object
        self.c_time = closing_time
        self.queue_out = queue
        super(CloseDoors, self).__init__()

    def run(self):
        self.elevator.floors[self.elevator.actual_floor].setState("stay")
        time.sleep(self.c_time)
        self.elevator.setState("stay")
        self.sendACK()
        
    def sendACK(self):
        message = "%d:%s" % (self.elevator.id+1, "a")
        self.queue_out.put_nowait(message)


class ListenInstructions(threading.Thread):

    def __init__(self, port_no, queue, segregate):
        self.port = port_no
        self.instruction_queue = queue
        self.segregate_task = segregate   
        super(ListenInstructions, self).__init__()
        
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(('localhost', self.port))
        self.serversocket.listen(5)

    def run(self):
        connection, address = self.serversocket.accept()
        while True:    
            buf = connection.recv(64)
            if len(buf) > 0:
                self.instruction_queue.put_nowait(buf)
                self.segregate_task()
                
    def exit(self):
        self.serversocket.close()
        self._Thread__stop()


class SendInstructions(threading.Thread):
    def __init__(self, port_no, queue):
        self.port = port_no
        self.sending_queue = queue
        super(SendInstructions, self).__init__() 
        
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(('localhost', self.port))
        self.serversocket.listen(5)

    def run(self):
        connection, address = self.serversocket.accept()
        while True:
            if not self.sending_queue.empty(): 
                elem = self.sending_queue.get()
                #print elem
                connection.sendall(elem)
                
    def exit(self):
        self.serversocket.close()
        self._Thread__stop()
        
        
        
        
class AI_component(threading.Thread):
    directions = ['d', 'u']
    
    def __init__(self, floor_list, queue_out, stage_object):
        self.stage = stage_object
        self.floor_list = floor_list
        self.queue = queue_out
        super(AI_component, self).__init__() 
        
    def run(self):
        i = 0
        while i<10:
            if self.queue.qsize() < 10:
                mess = self.make_message()
                self.queue.put_nowait(mess)
                i+=1
                time.sleep(0.5)
        self.stage.input_type = "manual"
                
    def exit(self):
        self._Thread__stop()
        
    def make_message(self):
        if (random.randint(0,2) == 0):
            #stoimy przed winda na pietrze)
            floor = random.randint(0, max(self.floor_list))
            dir = random.choice(self.directions)
            return ("%d:%s" % (floor, dir))
        else:
            #jestesmy w windzie
            elevator = random.randint(1, len(self.floor_list))
            floor = random.randint(0, self.floor_list[elevator-1])
            return ("%d:%d" % (elevator, floor))
            
            
