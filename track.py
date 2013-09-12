from Tkinter import Canvas, NW
import urllib2
from PIL import Image, ImageTk
from tle import TLE
from satellite import Satellite
from datetime import datetime
#import Canvas
# hardcode:
url = 'http://www.celestrak.com/NORAD/elements/tle-new.txt'
file_name = 'data.txt'

class Track:
    """ operates with list of satellites
    
    it can read data about satellites from file, from url, display satellites

    """
    def __init__(self):
        # loading images:
        img = Image.open('map.jpg')
        self.map_img = ImageTk.PhotoImage(img)
        img = Image.open('sat.png').convert("RGBA")
        self.sat_img = ImageTk.PhotoImage(img)
        
        self.anim = Canvas(width = 1024, height = 513)
        self.anim.create_image((0,0), anchor = NW, image = self.map_img)
        
        self.satellites = []    # list of satelites loaded from TLE
        self.draw_sats = []     # indices of desired satellites, and their
                                # canvas ID, for animation
    def load_local(self, file_name):
        fp = open(file_name, 'r')
        line = fp.readline()
        print "load"
        while line > '':
            title = line
            l1 = fp.readline()
            l2 = fp.readline()
            tle_data = TLE(title, l1, l2)
            sat = Satellite(tle_data, datetime.today())
            self.satellites.append(sat)
            line = fp.readline()

    def load_url(self, url, file_name):
        # will be improved later,,, now just downloading txt
        # and writes it to file
        buff = urllib2.urlopen(url)
        fp = open(file_name, 'rw')
        fp.write(buff.read())
    
    def update_satellites(self, dt):
        """ recalculate data about satellites """
        for (index, _id) in self.draw_sats:
            self.satellites[index].update(dt)
#        for sat in self.satellites:
#            sat.update(15)
    
    def add_satellite(self, index):
        # index will be taken from GUI,,,aditional images can be added
        _id = self.anim.create_image(self.satellites[index].map_coords, 
                                     image = self.sat_img)
        self.draw_sats.append((index, _id)) # better use dictionaries
        # testing:
        self.satellites[index].get_coords()
        self.anim.create_line(self.satellites[index].trajectory)
    def draw(self):
        """updates position of the satellites on the canvas"""
        for (index, _id) in self.draw_sats:
            self.anim.coords(_id, self.satellites[index].map_coords)
             
