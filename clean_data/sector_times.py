import pandas as pd
from collections import defaultdict

data = pd.read_excel("data/Sector Times v2.xlsx", 'driver')
data['Sector 1 Driver Num'] = data['Sector 1 Driver'].str.split(" ").str[0]
data['Sector 1 Driver'] = data['Sector 1 Driver'].str.split(" ").str[1:].apply(lambda x: " ".join(x))

data['Sector 2 Driver Num'] = data['Sector 2 Driver'].str.split(" ").str[0]
data['Sector 2 Driver'] = data['Sector 2 Driver'].str.split(" ").str[1:].apply(lambda x: " ".join(x))

data['Sector 3 Driver Num'] = data['Sector 3 Driver'].str.split(" ").str[0]
data['Sector 3 Driver'] = data['Sector 3 Driver'].str.split(" ").str[1:].apply(lambda x: " ".join(x))

data = data[['Pos', 'Sector 1 Driver Num', 'Sector 1 Driver', 'Sector 1 Time', 'Sector 2 Driver Num', 'Sector 2 Driver', 'Sector 2 Time', 'Sector 3 Driver Num', 'Sector 3 Driver', 'Sector 3 Time']]

data.to_excel("data/SectorTimes_Driver_cleaned.xlsx", sheet_name="driver", index = False)


types = defaultdict(str)
data = pd.read_excel("data/Sector Times v2.xlsx", 'team', dtype=types, keep_default_na=False)

data.loc[data['Pos3'] == '', 'Team Num'] = data['Team'].str.split(" ").str[0]
data.loc[data['Pos3'] == '', 'Team'] = data['Team'].str.split(" ").str[1:].apply(lambda x: " ".join(x))
data.loc[data['Pos3'] != '', 'Team Num'] = data['Pos3']
data['Pos'] = data['Pos2']

data = data[['Pos', 'Team Num', 'Team', 'Class', 'Ideal Lap', 'Best Lap Time', 'Best Lap Pos']]

data.to_excel("data/SectorTimes_Team_cleaned.xlsx", sheet_name="team", index = False, )
