from Tkinter import *  

class Elevator():
    lift_in_row = None    
    class Floor():
        state_machine = {'moveup': 'green', 'movedown': 'green', 'stay': 'red', 'clear': 'white', 'open': 'blue'}    
        def __init__(self, canvas, floor_no, height):
            self.canvas = canvas
            self.rec = canvas.create_rectangle(canvas.winfo_width()/2-20, canvas.winfo_height()-25-floor_no*height, canvas.winfo_width()/2+20, canvas.winfo_height()-25-(floor_no+1)*height+2, fill="white")
        
        def setState(self, state):
            self.canvas.itemconfigure(self.rec, fill=self.state_machine[state])
    
        

    def __init__(self, frame, floors, id, count):
        self.max_floors = floors
        self.lift_in_row = (count+1)//2
        self.id = id
        self.actual_floor=0
        self.floors = []
        self.canvas = Canvas(frame, height=(frame.winfo_height()/2)-2, width=(frame.winfo_width()/self.lift_in_row)-self.lift_in_row)
        self.canvas.grid(row=id/self.lift_in_row, column=id%self.lift_in_row, padx=1, pady=1)
        self.add_arrows()
        
        for i in range(floors+1):
            floor = self.Floor(self.canvas, i, (self.canvas.winfo_height()-50)/(floors+1))
            self.floors.append(floor)
            
        self.floor_display = self.canvas.create_text(self.canvas.winfo_width()-10, self.canvas.winfo_height()-10, anchor="se")    
        self.canvas.insert(self.floor_display, 15, "")
        
    def add_arrows(self):
        self.canvas.update()
        self.arrow_up = self.canvas.create_text(self.canvas.winfo_width()/2-4, 10, anchor="nw")
        self.canvas.itemconfig(self.arrow_up, text=u'\N{BLACK UP-POINTING TRIANGLE}')
        self.canvas.insert(self.arrow_up, 15, "")    
        
        self.arrow_down = self.canvas.create_text(self.canvas.winfo_width()/2-4, self.canvas.winfo_height()-10, anchor="sw")
        self.canvas.itemconfig(self.arrow_down, text=u'\N{BLACK DOWN-POINTING TRIANGLE}')
        self.canvas.insert(self.arrow_down, 15, "") 
    
    def UpdateLift(self, state='stay'):
        for floor_no in range(self.max_floors+1):
            self.floors[floor_no].setState('clear')       
        if self.actual_floor > self.max_floors:
            self.floors[self.max_floors].setState(state)
        else:
            self.floors[self.actual_floor].setState(state)       
        self.canvas.itemconfig(self.floor_display, text=self.actual_floor)
    
    def setState(self, state):
        self.canvas.itemconfig(self.arrow_up, text=u'\N{BLACK UP-POINTING TRIANGLE}', fill="black")
        self.canvas.itemconfig(self.arrow_down, text=u'\N{BLACK DOWN-POINTING TRIANGLE}', fill="black")
        if state == "moveup":
            self.canvas.itemconfig(self.arrow_up, text=u'\N{BLACK UP-POINTING TRIANGLE}', fill="green")
        if state == "movedown":
            self.canvas.itemconfig(self.arrow_down, text=u'\N{BLACK DOWN-POINTING TRIANGLE}', fill="green") 
        if state == "open":
            self.canvas.itemconfig(self.arrow_up, text=u'\N{BLACK UP-POINTING TRIANGLE}', fill="blue")
            self.canvas.itemconfig(self.arrow_down, text=u'\N{BLACK DOWN-POINTING TRIANGLE}', fill="blue")        
            
    def OpenDoors(self):
        pass
        
    def CloseDoors(self):
        pass
    
    def MoveLiftToFloor(self, floor):
        pass