import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import pandas as pd


def standing(url) :
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    temp = soup.find_all('table', {'class': 'standings'})[0]

    table_data = []
    for row in temp.find_all('tr'):
        row_data = []
        cnt = 0
        for cell in row.find_all('td'):
            if cnt == 3:
                break
            cnt += 1
            row_data.append(cell.text.strip())
        table_data.append(row_data)

    df = pd.DataFrame(table_data[1:], columns=['Rank', 'Handle', '# of solved problems'])

    return df

def merge(con1 , con2):
    total = pd.merge(con1, con2, on='Handle', how='outer', suffixes=('_con1', '_con2'))
    total.fillna(0, inplace=True)
    total['total solved problems'] = total['# of solved problems_con1'].astype('int') + total['# of solved problems_con2'].astype('int')
    total.sort_values('total solved problems', inplace=True, ignore_index=True, ascending=False)
    total = total.drop(columns=['Rank_con1', 'Rank_con2'])
    total.to_csv("total.csv", index=False)
    print("Done...")



url = input("Enter Contest URL 1 : ")
df1 = standing(url)
url = input("Enter Contest URL 2 : ")
df2 = standing(url)
df1['# of solved problems'] = pd.to_numeric(df1['# of solved problems'], errors='coerce')
df2['# of solved problems'] = pd.to_numeric(df2['# of solved problems'], errors='coerce')


merge(df1,df2)



