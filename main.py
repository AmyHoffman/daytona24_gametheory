from setup import *
from race import race

def main():
    new_race = race()
    new_race = create_teams(new_race)
    new_race = create_drivers_and_stint_analysis(new_race)
    new_race = fastest_lap_by_driver(new_race)
    flag = flag_analysis()
    new_race.all_teams = new_race.teams.copy()
    # new_race.filter_teams("GTD")
    new_race.remove_nonstarters()
    new_race.assign_start_positions()

    new_race.simulate()
    print(new_race.get_overtake_results())
    print(new_race.get_pitting_results())
    print(new_race.get_driver_change_results())
    new_race.get_position_plot()

if __name__ == "__main__":
    main()

# print("PTTING GAME")
# results_pitting = []
# for i in range(0, 100):
#     new_race.time = random.randrange(0,24*60*60)
#     d = 0
#     for t in range(0, len(new_race.teams) - 1):
#         team1 = new_race.get_team_byindex(t)
#         team2 = new_race.get_team_byindex(t+1)
#         pit_game = game.pit_game(team1, team2, d, False)
#         results_pitting = game.solve_pit_game(pit_game, results_pitting)
#         if results_pitting[i*t + t] == (1,1):
#             d += 1
# counter = collections.Counter(results_pitting)
# print(counter)

# print("OVERTAKING GAME")
# results = []
# for i in range(0, 100):
#     new_race.time = random.randrange(0,24*60*60)
#     team1 = random.randrange(0, len(new_race.teams)-1)
#     attacker = new_race.get_team_byindex(team1 + 1)
#     defender = new_race.get_team_byindex(team1)
#     overtake_game = overtake_game.overtake_game(attacker, defender)
#     overtake_game.solve_overtake_game(overtake_game, results)

#     if results[i] == (1,0):
#         attacker.position = attacker.position - 1
#         defender.position = defender.position + 1
#     elif results[i] == (1,1):
#         if overtake_game.success_overtake_prob(attacker, defender) >= 0.5:
#             attacker.position = attacker.position - 1
#             defender.position = defender.position + 1
#     new_race.order_teams()

# counter = collections.Counter(results)
# print(counter)
