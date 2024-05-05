import math
import nashpy as nash
import numpy as np

class pitting_game():

    def __init__(self, race):
        self.initiated = True
        self.race = race

    def pit_position(self, team, pitting_strat, d):
        return_val = 0
        if (pitting_strat[0]) and (not pitting_strat[1]):
            return_val = 1 / (team.position - d)
        elif (not pitting_strat[0]) and (pitting_strat[1]):
            return_val = -1 / team.position
        return(return_val)
            
    def pit_utility(self, team, flag, driver_change, pitting_strat, d):
        #  (1 - flag)*
        # + flag * (len(self.race.teams) + 1)
        u = (1 - self.race.get_time_prob(False)) * team.get_pit_need(self.race.time, driver_change) * self.pit_position(team, pitting_strat, d) 
        return(u)
    
    def pit_matrix(self, team, d = 1, flag = False, driver_change = False):
        m = [[self.pit_utility(team, flag, driver_change, [True, True], d), self.pit_utility(team, flag, driver_change, [True, False], d)],
             [self.pit_utility(team, flag, driver_change, [False, True], d), self.pit_utility(team, flag, driver_change, [False, False], d)]]
        return(m)

    def pit_game(self, team1, team2, d, flag):
        # the pit game
        if (team1 is None) or (team2 is None):
            print("break")
        team1_m = self.pit_matrix(team1, d, flag)
        team2_m = self.pit_matrix(team2, d, flag)
        

        self.game = nash.Game(team1_m, team2_m)
    
    def solve_pit_game(self):
        equilibria = self.game.support_enumeration()
        for eq in equilibria:
            team1_pit = int(eq[0][0])
            team2_pit = int(eq[1][0])
            # results.append((team1_pit, team2_pit))
            results = (team1_pit, team2_pit)
        return(results)

    def check_pit_strategy(self, game, team1_pit, team2_pit):
        team1_strat = np.array([int(team1_pit), int(not team1_pit)])
        team2_strat = np.array([int(team2_pit), int(not team2_pit)])
        result = game.is_best_response(team1_strat, team2_strat)
        return(result[0]) 

    