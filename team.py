import scipy.stats as st
import random
from driver import * 

LAP_TIRES = 32 
AVG_LAP_TIME = 104.2 # assumes average lap time of 1:44.2
LAP_TIME = LAP_TIRES * AVG_LAP_TIME 
HOURS2SEC = 60 * 60
MAX_STINT_TIME = 4 * HOURS2SEC 
MAX_DRIVE_TIME = 13 * HOURS2SEC 
LAP_LENGTH = 2.5 #miles

class team():
    #' Initialize a team
    def __init__(self, name, number, car, raceclass):
        self.name = name
        self.number = number
        self.car = car 
        self.raceclass = raceclass

        self.drivers = []
        self.current_driver = None
        self.position_array = []
        self.position = None
        self.lap_loc = 0
        self.lap_loc_temp = 0
        self.absolute_lap_loc = 0

        self.tire_wear_prob_func = self.build_tire_wear_prob()
        self.tire_wear_prob = 0
        self.driver_exhuastion_prob = self.build_driver_exhaustion_prob()

    #' Add a driver to the list of drivers on the team
    def add_driver(self, new_driver):
        self.drivers.append(new_driver)
        return(True)
    
    #' Get a driver by name from the team driver list
    def get_driver(self, driver_name):
        return_driver = None
        driver_lastname = driver_name.split(" ")[1]
        for d in self.drivers:
            if driver_lastname in d.name:
                return_driver = d
                break
            elif (d.name == 'F. Habsburg-Lothrin') & (driver_lastname == 'Habsburg-Lothringen'):
                return_driver = d
                break
        return(return_driver)
    
    #' Remove the drivers that did not start, meaning they do not have a fastest lap time
    def remove_nonstarters(self):
        new_driver_list = []
        for d in self.drivers:
            if d.fastest_lap_speed > 1.0:
                new_driver_list.append(d)
        self.drivers = new_driver_list
    
    #' -------- SIMULATION UTIL ---------
    #' Increment track location based on time passed
    #' TODO: update to use calculate sector
    def update_location(self, time_increment):
        self.lap_loc += (self.current_driver.get_current_speed(False) / HOURS2SEC) * time_increment
        self.update_absolute_location(self.lap_loc)

    def update_temp_location(self, time_increment):
        self.lap_loc_temp += (self.current_driver.get_current_speed(True) / HOURS2SEC) * time_increment
        self.update_absolute_location(self.lap_loc_temp)

    #' Update the track location to the next full lap, indicating pitting
    def update_location_fulllap(self):
        self.lap_loc = LAP_LENGTH * (math.floor(self.lap_loc / LAP_LENGTH) + 1)
        self.update_absolute_location(self.lap_loc)

    def update_absolute_location(self, loc):
        self.absolute_lap_loc = loc % LAP_LENGTH
        if self.absolute_lap_loc < 1e-12:
            self.absolute_lap_loc = 1e-5

    def update_loctemp_basedon_abs(self, newabs):
        self.absolute_lap_loc = newabs
        old_abs = self.lap_loc % LAP_LENGTH
        if newabs < old_abs:
            # update to next full lap, then add new abs
            self.lap_loc_temp = LAP_LENGTH * (math.floor(self.lap_loc / LAP_LENGTH) + 1) + newabs
        else:
            # add difference abs loc to new lap loc
            self.lap_loc_temp = self.lap_loc + (old_abs - newabs)

    #' Update the position of the team in total rankings
    def append_position_array(self, timestep, n):
        self.position_array.append([timestep, n])
        self.position = n
    
    #' -------- TIRES ---------
    #' Build the tire wear probability distribution
    def build_tire_wear_prob(self):
        pdf = st.norm(loc = LAP_TIME/2, scale = LAP_TIME/4)
        return(pdf)
    
    #' Get probablity that tires need replaced
    def tire_prob(self, time, inverse = False):
        rounded_to_sec = round(time%LAP_TIME,0)
        # z = self.tire_wear_prob_func.ppf(rounded_to_sec)
        return_value = self.tire_wear_prob_func.cdf(rounded_to_sec)

        if (inverse):
            return_value = 1 - return_value
        return(return_value)
    
    #' Add additional tirewear due to overtaking
    def update_tire_wear(self, overtake):
        if overtake:
            self.tire_wear_prob = 2 * (1 / LAP_TIRES)
        else:
            self.tire_wear_prob = (1 / LAP_TIRES)

    #' --------- DRIVER --------
    #' Build the driver exhaustion probability distribution
    #' TODO: are these bad parameters (visualize?)
    def build_driver_exhaustion_prob(self, max_time = None):
        if max_time is None:
            pdf = st.norm(loc = MAX_STINT_TIME/2, scale = MAX_STINT_TIME/6)
        else:
            pdf = st.norm(loc = max_time/2, scale = MAX_STINT_TIME/6)
        return(pdf)
    
    #' Get the probability the of neededing a driver change
    def driver_exhaustion_prob(self, time, inverse = False):
        # rounded_to_sec = round(time%MAX_STINT_TIME,0)
        # z = self.driver_exhuastion_prob.ppf(time)
        return_value = self.driver_exhuastion_prob.cdf(time)

        if (inverse):
            return_value = 1 - return_value
        return(return_value)
    
    #' Get binary if the driver needs changed
    def need_driver_change(self, time):
        prob = self.driver_exhaustion_prob(time)
        return_val = False
        if prob > 0.8:
            return_val = True
        return(return_val)
    
    #' Randomly assign a driver
    #' TODO: Control for rules here
    def random_assign_driver(self):
        if (len(self.drivers) > 0):
            if (self.current_driver is None):
                self.current_driver = random.choice(self.drivers)
            else:
                d = self.current_driver
                while d == self.current_driver:
                    d = random.choice(self.drivers)
                self.current_driver = d
    
    #' Assign the next driver based on rules and eligibility
    def assign_driver(self, t):
        newdriverfound = False
        while not newdriverfound:
            d = random.choice(self.drivers)
            if d != self.current_driver:
                if d.is_eligible():
                    self.change_driver(d, t)
                    newdriverfound = True
        return(True)
    
    def change_driver(self, d, t):
        self.current_driver = d
        self.driver_exhuastion_prob = self.build_driver_exhaustion_prob(d.get_time_remaining(t))

    #' ------- PITTING --------
    #' Get the utility of pitting
    def get_pit_need(self, time, driver_change):
        p_pit = self.tire_prob(time)
        if driver_change:
            p_pit = p_pit * self.driver_exhaustion_prob(time, False)
        return(p_pit)

    #' Get binary decision of if the team will pit
    def will_pit(self, time):
        # calculate the team's need to pit
        driver_change = self.need_driver_change(time)
        p_pit = self.get_pit_need(time, driver_change)
        return_value = False
        if (p_pit > 0.75):
            return_value = True

        return(return_value)
    
    #' Update and reset parameters after pitting
    def pitted(self, t, driver_change):
        self.tire_wear_prob = 0
        if (driver_change):
            self.current_driver.end_stint(t)
            self.assign_driver()
            self.current_driver.start_stint(t)

    #' ------ UTIL --------
    def __str__(self):
        return self.number + ": " + self.name + ", " + str(len(self.drivers)) + " drivers"
    
    #Rich comparison methods
    # def __lt__(self, other):
    #     return self.absolute_lap_loc < other.absolute_lap_loc

    # def __le__(self, other):
    #     return self.absolute_lap_loc <= other.absolute_lap_loc

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    # def __ge__(self, other):
    #     return self.absolute_lap_loc >= other.absolute_lap_loc

    # def __gt__(self, other):
    #     return self.absolute_lap_loc > other.absolute_lap_loc
    