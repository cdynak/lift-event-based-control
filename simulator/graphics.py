# -*- coding: utf-8 -*-
from Tkinter import *           # Importing the Tkinter (tool box) library 
import __main__
from elevator import *
from my_threads import *
from Queue import *


class Stage():
    window_width = 1200
    window_height = 800
    digit_in_row = 7
    elevators = []

    
    def __init__(self, lifts, floors, queue_out):
        self.lifts = lifts
        self.floors = floors
        self.queue_out = queue_out
        self.input_type = "manual"
       
        self.root = Tk()
        self.root.title("Elevator Simulator")    
        self.root.minsize(width=self.window_width, height=self.window_height)
        self.root.maxsize(width=self.window_width, height=self.window_height)
        self.frame_left = Frame(self.root, bg="lightblue")
        self.frame_right = Frame(self.root, bg="white")

        split = 0.7
        self.frame_left.place(relx=0, relwidth=split, relheight=1)
        self.frame_right.place(relx=split, relwidth=1.0-split, relheight=1)  
        self.frame_left.place(relx=0, relwidth=split, relheight=1)
        self.frame_right.place(relx=split, relwidth=1.0-split, relheight=1)
        
        self.frame_right_top = Frame(self.frame_right, bg="lightblue")
        self.frame_right_bottom = Frame(self.frame_right, bg="lightblue")
        split2 = 0.35
        self.frame_right_top.place(rely=0, relheight=split2, relwidth=1)
        self.frame_right_bottom.place(rely=split2, relheight=1.0-split2, relwidth=1)
        
        self.frame_left.update()       
        self.add_main_panel()
        self.add_digital_panel()
        self.build_lifts()

        self.AI_thread = AI_component(self.floors, self.queue_out, self)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            

    def add_main_panel(self):
        self.input_box = Entry(self.frame_right_top, width=3, font = "Helvetica 44 bold", justify="center")
        up = Button(self.frame_right_top, text=u'\N{BLACK UP-POINTING TRIANGLE}', font = "Helvetica 30 bold", width=2, height=1, command= lambda: self.callback_up_or_down("u"))
        down = Button(self.frame_right_top, text=u'\N{BLACK DOWN-POINTING TRIANGLE}', font = "Helvetica 30 bold", width=2, height=1, command= lambda: self.callback_up_or_down("d"))
        self.input_box.grid(row=1, column=0, rowspan=2, pady = 65, padx = 65)
        up.grid(row=1, column=1, sticky=W+S)
        down.grid(row=2, column=1, sticky=W+N, pady=5)

        auto = Button(self.frame_right_top, text="Automatic", font = "Helvetica 13 bold", width=9, height=2, command= lambda: self.automatic_on())
        auto.grid(row=0, column=0,  padx=0, pady=0)

    def add_digital_panel(self):
        for elem in range(max(self.floors) + 1):
            digit = Button(self.frame_right_bottom, text=elem, font = "Helvetica 13 bold", width=3, height=1, command= lambda var=elem: self.callback_inside(var))
            digit.grid(row=elem/self.digit_in_row, column=elem%self.digit_in_row, padx=2, pady=2)
        
    def build_lifts(self):
        for elem in range(self.lifts):
            winda = Elevator(self.frame_left, self.floors[elem], elem, self.lifts)
            self.elevators.append(winda)
        
        for lift in self.elevators:
            lift.UpdateLift()

    
    def callback_up_or_down(self, text):
        floor = self.input_box.get()
        self.queue_out.put_nowait(floor + ":" + text)    
    def callback_inside(self, destination):
        floor = self.input_box.get()
	if floor == "":
		floor = "0"
        self.queue_out.put_nowait(floor + ":" + str(destination))    
        
        
    def automatic_on(self):
        #print self.input_type
        if self.input_type == "manual":
            self.AI_thread.start()
            self.input_type = "auto"
            self.AI_thread = AI_component(self.floors, self.queue_out, self)

            
    def MakeALoop(self):
        self.root.mainloop()
     
    def on_closing(self):
        self.AI_thread.exit()
        self.root.destroy()
     

def scheduler(queue_in, queue_out, stage_object):
    instruction = queue_in.get()
    moving_time = 0.2
    breaking_time = 0.2 
    openning_time = 0.4
    closing_time = 0.4
    
    elevator, command = instruction.split(':')
    
    if command.isdigit():
        move_lift = MoveLift(stage_object.elevators[int(elevator)-1], int(command), moving_time, queue_out)
        move_lift.start()        
    if command == 's':
        stop_lift = StopLift(stage_object.elevators[int(elevator)-1], breaking_time, queue_out)
        stop_lift.start()       
    if command == 'o':
        open_door = OpenDoors(stage_object.elevators[int(elevator)-1], openning_time, queue_out)
        open_door.start()       
    if command == 'c':
        close_door = CloseDoors(stage_object.elevators[int(elevator)-1], closing_time, queue_out)
        close_door.start()
    
     
if __name__ == '__main__':
    
    lista_pieter = [10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 8, 20]
    queue_in = Queue(100)
    queue_out = Queue(100)
    
    scena = Stage(len(lista_pieter), lista_pieter, queue_out)# Execute the main event handler

    
#    for child in scena.frame_right_bottom.winfo_children():
#        child.configure(state='disable')
    
    listener = ListenInstructions(8089, queue_in, lambda: scheduler(queue_in, queue_out, scena))
    sender = SendInstructions(8090, queue_out)
    listener.start()  #watek nasluchujący instrukcje sterownika
    sender.start()    #watek wysylajacy odpowiedzi do sterownika
    
    
    scena.MakeALoop()
    listener.exit()
    sender.exit()
    
