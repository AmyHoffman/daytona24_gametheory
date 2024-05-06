import pandas as pd

final_dfs = {}
for n in range(1,25):
    if n >= 10:
        sheet = "Table0" + str(n) + " (Page " + str(n) + ")"
    else:
        sheet = "Table00" + str(n) + " (Page " + str(n) + ")"

    data = pd.read_excel("data/Lap Race Chart.xlsx", sheet_name=sheet, header = None)
    data.columns = data.iloc[1,:].tolist()

    data = data.drop([0,1], axis = 0, inplace = False)
    if n > 1:
        data = data.drop(['Nr', 'Pos'], axis = 1, inplace = False)
    final_dfs[sheet + str(n)] = data

final = pd.concat(final_dfs.values(), axis = 1)
print(final)

final.to_csv("data/lap_chart_processed.csv", index=False)