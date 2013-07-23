import numpy as np
from datetime import timedelta, datetime

miu = 398600                # could be changed by G * (M + m)
J2 = 1.08263 * pow(10, -3)  # for Earth oblateness
R = 6371                    # km, radius of Earth
DAY = 24*60*60              # seconds in a day

def ratio(Ecc_an, Mean_an, ecc):    #Eccentric and Mean anomaly, eccentricity
    """ function for solving Kepler's equation"""
    r = (Ecc_an - ecc*np.sin(Ecc_an) - Mean_an) / (1 - ecc*np.cos(Ecc_an))
    return r

def rate(ecc, a):   #eccentricity, semi-major axis of the orbit
    """ function for computing effects of the Earth's oblateness"""
    r = -(3*np.sqrt(miu)*J2*R*R) / (2*pow((1-ecc*ecc), 2)*pow(a, 3.5))
    return r

def rotation(O, w, i): #RAAN, arg of perigee, inclination(rad)
    """computes rotation matrix, probably will be replaced by Gibbs vector"""
    s = np.sin
    c = np.cos
    Q = np.matrix([ 
        [
        -s(O)*c(i)*s(w) + c(O)*c(w),
        -s(O)*c(i)*c(w) - c(O)*s(w),
        s(O)*s(i)
        ], 
        [
        c(O)*c(i)*s(w) + s(O)*c(w),
        c(O)*c(i)*c(w) - s(O)*s(w),
        -c(O)*s(i)
        ],
        [
        s(i)*s(w), 
        s(i)*c(w), 
        c(i)
        ] 
        ])
    return Q

class Satellite:
    """Class representation of a satellite.
    
    for initialization it needs TLE set, and current datetime, for
    synchronization with real data
    
    """
    
    def __init__(self, tle, current_time):
        self.name = tle.name
        self.inclination = tle.inclination * np.pi / 180    # rad
        self.raan = tle.omega * np.pi / 180                 # rad
        self.eccentricity = tle.e
        self.perigee_argument = tle.perigee * np.pi / 180   # rad
        self.mean_anomaly = tle.mean_anomaly *np.pi / 180   # rad
        self.mean_motion = tle.n                            # revs/day
        
        # position, velocity, computed after first update
        self.r = None
        self.v = None
        self.map_coords = (0, 0)
        
        # for ground tracking:
        self.longitude = 0 # degrees
        self.latitude = 0 # degrees [-90(S); 90(N)]
        
        # data for computing position
        # semimajor axis:
        self.a = pow(DAY*DAY*miu / pow(tle.n*2*np.pi, 2), 1.0 / 3)
        # specific relative angular momentum:
        self.h = np.sqrt(miu * self.a * (1 - pow(self.eccentricity, 2)))            
        
        # constants, for computing advance of RAAN, perigee(in rad/s):
        k = rate(self.eccentricity, self.a)     
        self.raan_rate =  k * np.cos(self.inclination)                      
        self.perigee_rate = k*(5.0*pow(np.sin(self.inclination), 2)/2 -2) 
        self.period = DAY / self.mean_motion # seconds, floating point
        
        # time in seconds from perigee to the TLE time
        time_offset = DAY*self.mean_anomaly / self.mean_motion*2*np.pi
        dt = timedelta(seconds = time_offset)
        # time of period (varies [0; self.period])
        self.t = (current_time-tle.time-dt).total_seconds() % self.period   
        
        # update of data, because of earth oblateness 
        self.update((current_time-tle.time).total_seconds())
        
    #Call this from global update:
    def update(self, dt):  
        self.t += dt
        if self.t > self.period: # a new period starts
            self.t = self.t % self.period
        
        # 1. Recompute Mean anomaly:
        self.mean_anomaly = 2 * np.pi * self.t / self.period  # in radians 

        # 2. Compute Eccentric anomaly
        err = pow(10,-8) #error tolerance
        e = self.eccentricity
        if self.mean_anomaly > np.pi:
            E_anomaly = self.mean_anomaly - e/2
        else:
            E_anomaly = self.mean_anomaly + e/2
        while abs(ratio(E_anomaly, self.mean_anomaly, e)) > err:
            E_anomaly -= ratio(E_anomaly, self.mean_anomaly, e)
        
        # 3. Compute True anomaly
        true_anomaly = 2*np.arctan(np.sqrt((1+e)/(1-e)) * np.tan(E_anomaly/2))
        if true_anomaly < 0:
            true_anomaly += 2 * np.pi
        
        # r in perifocal frame:
        rx = self.h*self.h / (miu*(1 + e*np.cos(true_anomaly)))
        # as a vector:
        rx *= np.array([[np.cos(true_anomaly)], [np.sin(true_anomaly)], [0]])   
        
        # 4. Take into consideration oblatness deviation !!Numerical errors 
        self.raan += self.raan_rate * dt
        self.perigee_argument += self.perigee_rate * dt  
        self.raan = self.raan % (2*np.pi)
        self.perigee_argument = self.perigee_argument % (2*np.pi)
        #print self.raan, self.perigee_argument          
        QxX = rotation(self.raan, self.perigee_argument, self.inclination)
        # 5. Compute (r,v)
        rX = QxX * rx       #r in geocentric equatorial XYZ frame
        self.r = rX

        theta = 72.9217 * pow(10,-6) * self.t
        r_xr = np.matrix([[np.cos(theta),
                           np.sin(theta), 0],
                          [-np.sin(theta),
                           np.cos(theta), 0],
                          [0, 0, 1]]) * rX #r in rotating, fixed to earth coordinates
        r_len = np.sqrt(r_xr[0]*r_xr[0] + r_xr[1]*r_xr[1] + r_xr[2]*r_xr[2])
        #print 'rx:', rx, 'r_xr', r_xr, 'rX:',rX

        l = float(r_xr[0] / r_len)   #direction cosine over X
        m = float(r_xr[1] / r_len)   #direction cosine over Y
        n = float(r_xr[2] / r_len)   #direction cosine over Z
        # 6. Compute (long, lat)
        self.latitude = np.arcsin(n)     # values from -pi/2(south) to pi/2 (north)
        if m > 0:
            self.longitude = np.arccos(l / np.cos(self.latitude))
        else:
            self.longitude = 2*np.pi - np.arccos(l / np.cos(self.latitude))
        self.longitude = self.longitude * 180 / np.pi   # into degrees
        self.latitude = self.latitude * 180 / np.pi # into degrees
        #_____>>>achtung<<<___hardcode
        # 2.84 need to be computed from current image size
        self.map_coords = (int(2.84*self.longitude), int(2.84*(90-self.latitude)))

#if __name__ == '__main__':
#here may be added code for debugging
