import math
import nashpy as nash
import numpy as np

class overtake_game():

    def __init__(self, race):
        self.initiated = True
        self.race = race
    
    def success_overtake_prob(self, t1d, t2d):
        p = 0
        if max(t1d.lap_speed, t2d.lap_speed) > 1.0:
            if (max(t1d.lap_speed, t2d.lap_speed) == 0) | (max(t1d.skill, t2d.skill) == 0):
                print("stop")
            p = ((t1d.lap_speed - t2d.lap_speed) / max(t1d.lap_speed, t2d.lap_speed)) + ((t1d.skill - t2d.skill) / max(t1d.skill, t2d.skill))
        return(p)
    
    def crash_prob(self, t1d, t2d):
        p = 0
        if max(t1d.lap_speed, t2d.lap_speed) > 1.0:
            p = self.race.get_time_prob(False) * ((t1d.craziness * t2d.craziness) / math.pow(max(t1d.lap_speed, t2d.lap_speed),2)) + ((t1d.skill * t2d.skill) / math.pow(max(t1d.skill, t2d.skill),2))
        return(p)
    
    def overtake_utility(self, team, donothing):
        u = self.race.get_time_prob(False) * (1 / team.position) * int(donothing == False)
        return(u)
    
    # to match prior work, have to talk about nature, but not sure how to model
    def expected_overtake_utility(self, attacker, defender, donothing, for_attacker):
        t1d = attacker.current_driver
        t2d = defender.current_driver
        p_success = self.success_overtake_prob(t1d, t2d)
        p_crash = self.crash_prob(t1d, t2d)
        u = self.overtake_utility(attacker, donothing)
        return([p_success, p_crash, u])
    
    def overtake_matrices(self, attacker, defender):
        a = self.expected_overtake_utility(attacker, defender, False, True)
        a_m = [[(a[0] + a[1]) * a[2], (a[0] + (1-a[1])) * a[2]],
               [((1-a[0] + a[1])) * a[2], ((1-a[0]) + (1-a[1])) * a[2]]]
        
        d = self.expected_overtake_utility(defender, attacker, False, False)
        d_m = [[(d[0] + d[1]) * d[2], ((1-d[0]) + d[1]) * d[2]],
               [(d[0] + (1-d[1])) * d[2], ((1-d[0]) + (1-d[1])) * d[2]]]
        return([a_m, d_m])

    def overtake_game(self, attacker, defender):
        matrices = self.overtake_matrices(attacker, defender)
        self.game = nash.Game(matrices[0], matrices[1])
    
    def solve_overtake_game(self):
        equilibria = self.game.support_enumeration()
        # print("Overtake Game EQUILIBRIA:")
        for eq in equilibria:
            # print(eq)
            attack = int(eq[0][0])
            defend = int(eq[1][0])
            # results.append((attack, defend))
            results = (attack, defend)
        return(results)

    def check_overtake_strategy(self, game, attacker_attack, defender_defend):
        attacker_strat = np.array([int(attacker_attack), int(not attacker_attack)])
        defender_strat = np.array([int(defender_defend), int(not defender_defend)])
        result = game.is_best_response(attacker_strat, defender_strat)
        return(result[0]) 
