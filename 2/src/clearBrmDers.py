import pandas as pd


excel_data = pd.read_excel("resources/BrmDers.xls", dtype=str).fillna("0")
fakinList = []
for index, row in excel_data.iterrows():
    if row['KR'] != "0" and row['INSANB'] == "0" and "S&D" not in row['DERSADI'] and "ENGINEERING RESEARCH ON" not in row['DERSADI']:
        fakinList.append((row['DERSADI']))


fakinList = list(dict.fromkeys(fakinList))
fakinList.sort(key=lambda x: x[0], reverse=False)

for i in range(fakinList.__len__()):
    print(fakinList[i])