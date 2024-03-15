import pandas as pd 
import numpy as np
import csv

from collections import defaultdict
types = defaultdict(str)

data = pd.read_excel("data/Stint Analysis v2.xlsx", sheet_name="Sheet1", dtype=types, keep_default_na=False)


# clean the stint analysis sheet
data.loc[data[data.columns[0]]=='', data.columns[0]] = np.nan
data[data.columns[0]] = data[data.columns[0]].ffill()


for r in range(data.shape[0]):
    if (data.loc[r, 'Start'] == ''):
        data.iloc[r, 2:8] = data.iloc[r, 3:9]
        data.iloc[r,8] = ''
    if (data.loc[r, 'Nr. Driver'] == '') & (data.loc[r, 'Start'] != ''):
        if (len(data.loc[r, 'Start'].split(" ")) > 1):
            data.loc[r, 'Nr. Driver'] = " ".join(data.loc[r, 'Start'].split(" ")[:-1])
            data.loc[r, 'Start'] = data.loc[r, 'Start'].split(" ")[-1]

data.loc[data[data.columns[1]]=='', data.columns[1]] = np.nan
data[data.columns[1]] = data[data.columns[1]].ffill()

data.loc[:,'stint'] = data.loc[:,'Nr. Driver'].str.split(" ").str[0]
data.loc[~(data.stint.str.isnumeric()), 'stint'] = np.nan
data.loc[(data.stint.str.isnumeric()) & ~(data.stint.isna()), 'Nr. Driver'] = data['Nr. Driver'].str.split(" ").str[1:].apply(lambda x: " ".join(x))
data['stint'] = data['stint'].ffill()

data = data.astype('str')
print(data.dtypes)
data.to_excel("data/stint_analysis_v3.xlsx", index = False)

print(data.head())

# data = pd.read_excel("data/Stint Analysis v2.xlsx", sheet_name="Sheet2", dtype=types, keep_default_na=False)

# create and export the team look up table
# teams = data.iloc[:, 0:4]
# teams = teams[teams.iloc[:,1] != '']
# teams.columns = ['number', 'name', 'car', 'class']
# teams.to_csv("data/teams_cleaned.csv", index = False)

# clean the total pit, total track, and total time data set
# data = data.drop(data.columns[[1,2,3,5]], axis = 1)
# data.drop_duplicates()

# data.loc[data[data.columns[0]]=='', data.columns[0]] = np.nan
# data[data.columns[0]] = data[data.columns[0]].ffill()
# data = data.reset_index(drop = True)

# for r in range(data.shape[0]):
#     if (data.loc[r, data.columns[2]] == ''):
#         data.loc[r, data.columns[2]] = data.loc[r, data.columns[3]]
#         data.loc[r, data.columns[3]] = data.loc[r, data.columns[4]]
#         data.loc[r, data.columns[4]] = ''
#     if (data.loc[r, data.columns[4]] == ''):
#         data.loc[r, data.columns[4]] = data.loc[r, data.columns[5]]
#         data.loc[r, data.columns[5]] = ''
#     if (data.loc[r, data.columns[4]] == ''):
#         data.loc[r, data.columns[4]] = data.loc[r, data.columns[6]]
#         data.loc[r, data.columns[6]] = ''

# data = data.drop(data.columns[[5,6]], axis = 1)
# data.columns = ['number', 'driver', 'total_track', 'total_pits', 'total_time']
# data = data[(data['driver'] != '') | (data['total_pits'] != '')]

# data.to_csv("data/stint_analysis_totals_v3.csv", index=False)