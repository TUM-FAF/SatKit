from datetime import datetime
from math import modf

def get_date_time(string):
    year = int(string[:2])
    time, days = modf(float(string[2:]))
    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0:
        months[1] = 29
    month = 1; days = int(days)                     #tak, na vseakii sluch
    for m in months:
        if days > m:
            days, month = days - m, month + 1
        else:
            break
    time, hour = modf(time * 24)
    time, mins = modf(time * 60)
    time, sec = modf(time * 60)
    hour = int(hour)
    mins = int(mins)
    sec = int(sec)
    year += 1900
    if year<56:
        year += 100
    return datetime(year , month, days, hour, mins, sec)
        
class TLE:
    """class for extracting data from TLE
    
    it receives data from 3 strings, which will be downloaded from celestrak.com
    or http://www.tle.info/joomla/index.php and transforming into necessary data 
    to calculate position of a satellite at given time 
    
    """

    def __init__(self, title_line, line_1, line_2): 
        """loads data from TLE, each input field is respective line of TLE"""
        self.time = get_date_time(line_1[18:32])
        self.name = title_line.rstrip()					
        self.inclination = float(line_2[8:16])			#angle i, degrees
        self.omega = float(line_2[17:25])				#RAAN, degrees
        self.e = float('0.' + line_2[26:33])    		#Eccentricity
        self.perigee = float(line_2[34:42])		    	#omega, degrees
        self.mean_anomaly = float(line_2[43:51])		#degrees
        self.n = float(line_2[52:63])					#mean motion, revs/day

    def output(self):
        """print on command line the elements"""
        print """Name: {0}\nInclination: {1}\nOmega: {2}\neccentricity: {3}
w: {5}\nMe: {6}\nn: {4}\n""".format(self.name, self.inclination,
                                  self.omega, self.e, self.n,
                                  self.perigree, self.mean_anomaly)
        print self.time, datetime.today()
        print 'time passed:', datetime.today() - self.time

if __name__ == "__main__":
    import sys
    sat = TLE(sys.argv[1], sys.argv[2], sys.argv[3])
    sat.output()
