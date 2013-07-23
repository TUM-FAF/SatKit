from Tkinter import *
from tkFileDialog import *
from track import Track # remove
from stime import Time 

class UserMenu(Menu):
    """ menu for app """
    def __init__(self, parent):
        Menu.__init__(self, parent)
        file_menu = Menu(self, tearoff = False)
        
        self.add_cascade(label = "File", menu = file_menu)
        file_menu.add_command(label = "New", command = self.callback)
        file_menu.add_command(label = "Open", command = self.open_tle)
        file_menu.add_command(label = "Exit", command = self.quit)
    
        time_menu = Menu(self, tearoff = False)
        self.add_cascade(label = "Time", menu = time_menu)
        time_menu.add_command(label = "Increase Speed", command = self.faster)
        time_menu.add_command(label = "Decrease Speed", command = self.slower)
        time_menu.add_command(label = "Normal Speed", command = self.normal)
        
        self.master = parent
    def callback(self):
        print 'to be defined later'
    def open_tle(self):
        file_name = askopenfilename()

        self.master.sats.load_local(file_name)
        # to add dialog for choosing satellites, or on the list
        self.master.sats.add_satellite(17)

    def faster(self):
        if self.master.time_speed < 10:
            self.master.time_speed +=1
        else:
            self.master.time_speed = int(self.master.time_speed * 1.2)
                
    def slower(self):
        if self.master.time_speed < 10:
            self.master.time_speed -=1
        else:
            self.master.time_speed = int(self.master.time_speed / 1.2)

    def normal(self):
        self.master.time_speed = 1
