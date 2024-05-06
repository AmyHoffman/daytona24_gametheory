import pandas as pd
import math
import random

BUFFER = 0.1
HOURS2SEC = (60*60)

class driver():
    #' Initialize a driver
    def __init__(self, name):
        self.name = name

        self.fastest_sector_times = None
        self.craziness = -1
        self.skill = -1
        self.fastest_lap = None
        self.fastest_lap_speed = None
        self.lap_speed = None
        self.lap_std = None
        self.stints = []
        self.total_stints = pd.DataFrame(columns = ['total_track','total_pits','total_time'])

        self.total_time_in_car = 0
        self.stint_duration = 0
        self.stint_start = None
        self.stint_end = None

    #' ------ Start & End Stints -------
    #' Add completed stint to driver's log
    def log_stint(self):
        self.stints.append([self.stint_start, self.stint_end])
        t = self.stint_end - self.stint_start

        self.stint_duration += t
        self.total_time_in_car += t
        return(False)
    
    #' Start a new stint
    def start_stint(self, t):
        self.stint_start = t
        self.stint_duration = 0
        self.stint_end = 0

    #' End current stint
    def end_stint(self, t):
        self.stint_end = t
        self.log_stint()

    #' ------ Driver Eligiblity Checks -------
    #' Check if driver is eligible for driver change or to keep driving
    def is_eligible(self, t):
        return_val = True
        stint_duration = t - self.stint_start
        sixhr_duration = self.get_time_in_past_6hrs(t)

        if (sixhr_duration >= (BUFFER * 6 * HOURS2SEC)) | (stint_duration >= (BUFFER * 4 * HOURS2SEC)) | (self.total_time_in_car >= (BUFFER * 13 * HOURS2SEC)):
            eligible = False

        return(return_val)
    
    #' Check how long a driver can drive for a stint
    def get_time_remaining(self, t):
        stint_duration = t - self.stint_start
        sixhr_duration = self.get_time_in_past_6hrs(t)
        
        time_remaining_6hrs = (4 * HOURS2SEC) - (stint_duration + sixhr_duration)
        time_remaining_13hrs = (13 * HOURS2SEC) - (stint_duration + self.total_time_in_car)
        time_remaining = math.min(time_remaining_6hrs, time_remaining_13hrs)
        return(time_remaining)

    #' Calculate how long the driver was in the car over the past six hours
    def get_time_in_past_6hrs(self, t):
        sixhrs_ago = t - (6 * HOURS2SEC)
        priorto6hrs = True
        i = 0
        sixhr_duration = 0

        while priorto6hrs:
            if i > len(self.stints):
                priorto6hrs = False
            else:
                start = self.stints[len(self.stints) - i][0]
                end = self.stints[len(self.stints) - i][1]
                if start >= sixhrs_ago:
                    sixhr_duration += (end - start)
                elif (start < sixhrs_ago ) & (end > sixhrs_ago):
                    sixhr_duration += (end - sixhrs_ago)
                else:
                    priorto6hrs = False   
                i += 1

        return(sixhr_duration)

    #' ------- SPEED AND LOCATION ---------
    #' Return the driver's current speed
    #' TODO: update to use sector time
    def get_current_speed(self, random_assign = False):
        if random_assign:
            self.lap_speed = self.fastest_lap_speed * random.randrange(74, 100, 2)/ 100  
        return(self.lap_speed)

    #' ------ UTIL -------
    def __str__(self):
        return(self.name)
    
    def __eq__(self, other):
        return (self.name) == (other.name)


