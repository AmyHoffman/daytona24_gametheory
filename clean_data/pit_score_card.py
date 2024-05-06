import pandas as pd 

# clean the pit score card
sheet_names = ["Table001 (Page 1)", "Table002 (Page 2)", "Table003 (Page 3)", "Table004 (Page 4)", 
               "Table005 (Page 5)", "Table006 (Page 6)", "Table007 (Page 7)", "Table008 (Page 8)", 
               "Table009 (Page 9)", "Table010 (Page 10)", "Table011 (Page 11)", "Table012 (Page 12)",
               "Table013 (Page 13)", "Table014 (Page 14)", "Table015 (Page 15)", "Table016 (Page 16)"]

final_dfs = {}
for sheet in sheet_names:
    print(sheet)
    data = pd.read_excel("data/Pit Score Card.xlsx", sheet_name=sheet, header = None)
    print()
    data.columns = ['c' + str(x) for x in range(1,data.shape[1]+1)]

    for sv in [2,7]:

        if (data.shape[1] > sv + 3):
            clean1 = data['c' + str(sv)].str.extract('^(\d+)\s+([\d:.]+)\s+([^\d]+)$')
            clean1.columns = ['nr', 'intime', 'indriver']

            clean2 = data['c' + str(sv)].str.extract('^(\d+)\s+([\d:.]+)\s+([^0-9]+)\s+([\d:.]+)\s+([^0-9]+)$')
            clean2.columns = ['nr', 'intime', 'indriver', 'outtime', 'outdriver']

            clean3 = data['c' + str(sv+1)].str.extract('^([\d:.]+)\s+([^0-9]+)$')
            clean3.columns = ['outtime', 'outdriver']

            cleaned1 = clean2.combine_first(clean1).combine_first(clean3)
            remaining_fields1 = data[['c' + str(sv+2), 'c' + str(sv+3)]]
            remaining_fields1.columns = ['time', 'cumtime']

            final_dfs[sheet + str(sv)] = pd.concat([cleaned1, remaining_fields1], axis = 1)

final = pd.concat(final_dfs.values(), axis = 0)
final.astype(str)
print(final)

final.to_excel("data/pit_score_card_processed.xlsx", index=False)