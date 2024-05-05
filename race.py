import scipy.stats as st
import collections
import pandas as pd
from plotnine import *
from overtake_game import overtake_game
from pitting_game import pitting_game

DURATION = 24
HOURS2SEC = 60 * 60
AVG_LAP_TIME = 104.2

class race():
    #' Initilize the race
    def __init__(self, ti = 60):
        self.time = 0 
        self.teams = None
        self.teams_temp = None
        self.all_teams = None
        self.time_probability = self.build_time_probability()
        self.time_increment = ti
        
        self.pit_game = pitting_game(self)
        self.results_pitting = []
        self.n_pitted_drivers = 0
        self.overtake_game = overtake_game(self)
        self.results_overtake = []
        self.results_driver_change = []

    # ------ Start of race activitiies ------
    #' Randomly assign initial drivers and starting positions
    def assign_start_positions(self):
        for t in range(0, len(self.teams)):
            self.teams[t].position = t + 1
            self.teams[t].random_assign_driver()
        return(self)

    #' Remove the drivers that did not start, meaning they do not have a fastest lap time
    def remove_nonstarters(self):
        new_teams_list = []
        for t in self.teams:
            t.remove_nonstarters()
            if (len(t.drivers) >= 3):
                new_teams_list.append(t)
        self.teams = new_teams_list
        return(self)

    #' ------- Simulation Utilities --------
    #' Simulate the race in time increments
    def simulate(self):
        while self.time < (DURATION * HOURS2SEC):
            print(self.time)
            self.make_decisions()
            self.time += self.time_increment
        return(True)

    #' Increment time
    def make_decisions(self):
        # team.lap_loc_temp will log where drivers were after simulation step
            # team.lap_loc will log where the driver was before simulation step
        for t in range(0, len(self.teams)):
            self.teams[t].update_temp_location(self.time_increment)
        
        # create second array (self.teams_temp) of where drivers will be after simulation step
            # self.teams will track where drivers were before simulation step
        self.teams_temp = self.teams.copy()
        self.teams_temp.sort(key=lambda x: x.absolute_lap_loc, reverse = True)

        # starting at first position before step, check for pit and overtake
        for t in range(1, len(self.teams)):
            pitted = self.check_pit(t)
            if not pitted:
                self.check_overtake(t)
            # after decisions, finalize the driver's location
            self.teams[t].lap_loc = self.teams[t].lap_loc_temp

        # reassign positions after decisions
        self.teams.sort(key=lambda x: x.lap_loc, reverse = True) 
        for t in range(0, len(self.teams)):
            self.teams[t].append_position_array(self.time, t + 1)

        # prep for next simulation step
        self.teams.sort(key=lambda x: x.absolute_lap_loc, reverse = True) 
        self.n_pitted_drivers = 0    
    
    #' ------- Game Theory Functions --------
    #' determine which drivers are trying to overtake which
    def check_overtake(self, t):
        if (self.time > AVG_LAP_TIME):
            attacker_before = self.teams[t]
            attacker_after_index = self.get_team_index(attacker_before.number, self.teams_temp)
            
            # if the driver moved up based on time alone 
            if attacker_after_index > t:
                # the drivers they would need to overtake to get to that position
                overtakes = [t for t in self.teams[:t] if t not in self.teams_temp[:attacker_after_index]]
                for d in range(len(overtakes)-1, -1, -1):
                    attack = self.apply_overtake_game(self.teams[t], overtakes[d], False)
                    # if they failed an attack, then break because they cannot attack a driver in front a defender they did not attack
                    if not attack:
                        break
    
    #' Apply over take game
    def apply_overtake_game(self, attacker, defender, absolute_loc):
        self.overtake_game.overtake_game(attacker, defender)
        result = self.overtake_game.solve_overtake_game()
        attack = True

        # if did not attack, update their location to be behind the defender
        if (result[0] == 0):
            attacker.update_loctemp_basedon_abs(defender.absolute_lap_loc*0.99999)
            attack = False
        # else if did attack, then do not change lap location because it's correct...for now
        
        self.results_overtake.append(result)
        return(attack)

    def get_overtake_results(self):
        counter = collections.Counter(self.results_overtake)
        print(counter)
    
    #' Apply pitting game
    def check_pit(self, t):
        pitted_bool = False
        if (t > 0) :
            current_team = self.get_team_byposition(t)
            if current_team.lap_loc % 1 >= 0.75:
                # this seems backwards, but it's converting index to position
                self.pit_game.pit_game(self.get_team_byposition(t+1), current_team, self.n_pitted_drivers, False)
                result = self.pit_game.solve_pit_game()
                if result[1] == 0:
                    if current_team.will_pit(self.time):
                        result = (result[0], 1)
                if result == (1,1):
                    self.n_pitted_drivers += 1
                if result[1] == 1:
                    pitted_bool = True
                    self.check_driver_change(current_team)
                self.results_pitting.append(result) 
        return(pitted_bool)
    
    def get_pitting_results(self):
        counter = collections.Counter(self.results_pitting)
        print(counter)

    def check_driver_change(self, team):
        need_driver_change = team.need_driver_change(self.time)
        self.results_driver_change.append(need_driver_change)
        return(need_driver_change)

    def get_driver_change_results(self):
        counter = collections.Counter(self.results_driver_change)
        print(counter)
    
    #' ------- Get Information ------
    #' Get a team using the team number
    def get_team(self, number, myteamslist):
        return_team = None
        for t in myteamslist:
            if t.number == number:
                return_team = t
                break
        return(return_team)
    
    #' Get a team's index in a list by the team number
    def get_team_index(self, number, myteamslist):
        return_index = None
        for t in range(0, len(myteamslist)):
            if myteamslist[t].number == number:
                return_index = t
                break
        return(return_index)
    
    #' Get a team by index or position
    def get_team_byindex(self, i):
        return(self.teams[i])
    
    #' Get a team by the position
    def get_team_byposition(self, i):
        return_team = None
        for t in self.teams:
            if t.position == i:
                return_team = t
                break
        return(return_team)
   
    #' Subset the teams to only be a specific race class
    def filter_teams(self, raceclass):
        new_teams = []
        for t in self.all_teams:
            if t.raceclass == raceclass:
                new_teams.append(t)
        self.teams = new_teams
    
    # ------- Impact of Time --------
    #' Build the probability function used to estimate impact of time
    def build_time_probability(self):
        n_increments = 24 * 60 * 60 # seconds
        time_pdf = st.norm(loc = n_increments/2, scale = n_increments/4)
        # sequence = [ x / (n_increments) for x in  list(sequence) ]
        return(time_pdf)
    
    # Get the probability associated with current time
    def get_time_prob(self, inverse):
        rounded_to_sec = round(self.time,0)
        return_value = self.time_probability.cdf(rounded_to_sec)
        # index_nearest_value = round(time,-1) / 10
        # return_value = self.time_probability[index_nearest_value]
        if (inverse):
            return_value = 1 - return_value
        return(return_value)
    
    # ------- Visualization --------
    def get_position_plot(self):
        vis_df = None
        for team in self.teams:
            temp = pd.DataFrame(team.position_array, columns = ['Time', 'Position'])
            temp['Team'] = team.number 
            
            if vis_df is None:
                vis_df = temp
            else:
                vis_df = pd.concat([vis_df, temp])
        
        vis_df.to_csv("data/positions.csv")

        (
            ggplot(vis_df)
            + aes(x = "Time", y = "Position", group = "Team")
            + geom_line()
        )


