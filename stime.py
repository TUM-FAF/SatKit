import datetime
from datetime import timedelta
from threading import Timer
from time import sleep

#constant definitions:
DAY = 24*60*60 # seconds in a day

class Time:
    """
    Time representation in the app.

    callback_function - called every TIMER_INTERVAL.
    Initially set to an empty function. Set it to any extern function.

    Time(speed = 1) - initialises with the corresponding speed;
    
    set_speed(speed = 1) - sets the current speed within MIN_TIME_SPEED and 
    MAX_TIME_SPEED.
    """
    #class constant definitions:
    MIN_TIME_SPEED = 0 # Time stops.
    MAX_TIME_SPEED = DAY*365 # One year per second.
    TIMER_INTERVAL = .1 # How often the time is updated.

    def callback_function(self):
        print 'helloworld!'
        pass

    def __init__(self, speed = 1):
        self.current_speed = speed
        self.current_time = datetime.datetime.now()
        #start time update:
        self.__timer = Timer(self.TIMER_INTERVAL, self.__time_changed)
        self.__timer.start()
        
    def __time_changed(self):
        #print self.current_time
        interval = timedelta(seconds = self.current_speed * self.TIMER_INTERVAL)
        self.current_time += interval
        #schedule next time update:
        self.__timer = Timer(self.TIMER_INTERVAL, self.__time_changed)
        self.__timer.start()
        self.callback_function()
        
    def set_speed(self, speed = 1):
        if (speed >= self.MIN_TIME_SPEED) and \
            (speed <= self.MAX_TIME_SPEED):
            self.current_speed = speed
            
        else:
            print 'Cannot set speed'
        
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        print 'Timer canceled'
        self.__timer.cancel()

    def __del__(self):
        self.__timer.cancel()


if __name__ == '__main__':
    print 'asda'    
    c = Time()
    sleep(3)
    c.__del__()
       
