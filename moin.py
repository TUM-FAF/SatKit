from Tkinter import *
import tkMessageBox
from datetime import datetime
#from PIL import Image, ImageTk
#import usermenu as um
from satellite import Satellite
from tle import TLE
from stime import Time
from track import Track
from time import sleep # REMOVE

root = Tk() #main window
root.title('SatKit ground tracking')

# TODO:
#   set grid geometry
#   set menu
#   set toolbar
#   timer start/ init/ handle

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

root.mainloop()
