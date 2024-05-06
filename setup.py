from util import *
from team import team
from driver import driver
from flags import flags
import pandas as pd
import numpy as np

datafolder = "data/modeling/"

def create_teams(new_race):
    data = pd.read_csv(datafolder + "teams_cleaned.csv", dtype=str, keep_default_na=False)
    teams = []
    for r in range(data.shape[0]):
        new_team = team(data.loc[r,'name'], str(data.loc[r,'number']), data.loc[r,'car'], data.loc[r,'class'])
        teams.append(new_team)
        # print(new_team)
    new_race.teams = teams
    return(new_race)

def create_drivers_and_stint_analysis(new_race):
    data = pd.read_csv(datafolder + "stint_analysis_totals_cleaned.csv", dtype = str, keep_default_na=False)
    data.loc[:, 'total_track'] = data[['total_track']].apply(lambda x: string_to_seconds(x['total_track']), axis = 1)
    data.loc[:, 'total_pits'] = data[['total_pits']].apply(lambda x: string_to_seconds(x['total_pits']), axis = 1)
    data.loc[:, 'total_time'] = data[['total_time']].apply(lambda x: string_to_seconds(x['total_time']), axis = 1)

    qs = np.percentile(data.total_pits, [25, 50, 75]).tolist()

    for r in range(data.shape[0]):
        team = new_race.get_team(data.loc[r, 'number'], new_race.teams)
        new_driver = driver(data.loc[r, 'driver'])
        new_driver.total_stints = data.iloc[r, 2:5]
        new_driver.craziness = get_ranking(qs, data.loc[r, 'total_pits'])
        team.add_driver(new_driver)
    
    # data = pd.read_excel(datafolder + "stint_analysis_cleaned.xlsx", sheet = "Sheet1", dtype = str, keep_default_na=False)
    # data.loc[:, 'T.Track'] = data[['T.Track']].apply(lambda x: string_to_seconds(x['T.Track']), axis = 1)
    # data.loc[:, 'Time'] = data[['Time']].apply(lambda x: string_to_seconds(x['Time']), axis = 1)
    # data.loc[:, 'T.Driver'] = data[['T.Driver']].apply(lambda x: string_to_seconds(x['total_time']), axis = 1)
    return(new_race)

def fastest_lap_by_driver(new_race):
    data = pd.read_csv(datafolder + "fastest_lap_by_driver_cleaned.csv", dtype = str, keep_default_na=False)
    data.loc[:, 'Time'] = data[['Time']].apply(lambda x: string_to_seconds(x['Time']), axis = 1)
    qs = np.percentile(data.Time, [25, 50, 75]).tolist()

    for r in range(data.shape[0]):
        team = new_race.get_team(str(data.loc[r, 'Nr']), new_race.teams)
        driver = team.get_driver(data.loc[r, 'Driver'])
        driver.fastest_lap = data.loc[r, 'Time']
        driver.fastest_lap_speed = float(data.loc[r, 'Mph'])
        driver.skill = get_ranking(qs, data.loc[r, 'Time'])

    return(new_race)
        

def flag_analysis():
    data = pd.read_excel(datafolder + "Flag Analysis.xlsx", sheet_name = "Page001", dtype = str, keep_default_na=False)
    # data.loc[:, 'Time'] = data[['Time']].apply(lambda x: string_to_seconds(x['Time']), axis = 1)
    data.loc[:, 'Session Elapsed'] = data[['Session Elapsed']].apply(lambda x: string_to_seconds(x['Session Elapsed']), axis = 1)
    data.loc[:, 'Flag Time'] = data[['Flag Time']].apply(lambda x: string_to_seconds(x['Flag Time']), axis = 1)
    data.loc[:, 'Acum. Flag Time'] = data[['Acum. Flag Time']].apply(lambda x: string_to_seconds(x['Acum. Flag Time']), axis = 1)

    flag = flags()
    flag.build_time_between_pdf(data[data['Flag'] == 'GREEN FLAG'].loc[:, 'Flag Time'])
    flag.build_duration_pdf(data[data['Flag'] == 'FULL COURSE YELLOW'].loc[:, 'Flag Time'])

    return(flag)


