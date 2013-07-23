from Tkinter import *
import tkMessageBox
from datetime import datetime
#from PIL import Image, ImageTk
from usermenu import UserMenu
from satellite import Satellite
from tle import TLE
from stime import Time
from track import Track
from time import sleep # REMOVE

class App(Tk):
    def __init__(self, ftimer):
        Tk.__init__(self)
        self.timer = ftimer
        self.timer.callback_function = self.redraw
        self.time_speed = 1                 # normal speed
            
        self.sats = Track()
        self.sats.load_local("data.txt")    # to be changed
        self.sats.add_satellite(3)          # achtung, hardcode
        
        menu = UserMenu(parent = self)
        self.config(menu = menu)
    
    def redraw(self):
        
        self.timer.set_speed(self.time_speed)
        self.sats.update_satellites(self.time_speed)
        print self.time_speed 
        # recompute "current" time, later,,,
        self.sats.anim.grid()
        self.sats.draw() 

with Time() as ftimer:   # CHANGE IT TOTALLY 
    root = App(ftimer)
    root.mainloop()

# TODO:
#   set grid geometry
#   set menu
#   set toolbar
#   timer start/ init/ handle
"""
# BYDLOKoD BELOW
tr = Track()
tr.load_local('data.txt')
tr.anim.grid()
i = 0
tr.add_satellite(3)
tr.add_satellite(0)
tr.add_satellite(9)
tr.add_satellite(7)
tr.add_satellite(11)
while i < 2000:
    tr.update_satellites()
    tr.draw()
    tr.anim.update()
    sleep(0.2)
    i += 1

if __name__ == "__main__":
    app=App()
    app.mainloop()
"""
