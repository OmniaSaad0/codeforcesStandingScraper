import requests
from bs4 import BeautifulSoup
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
            if cnt == 4:
                break
            cnt += 1
            row_data.append(cell.text.strip())
        table_data.append(row_data)

    df = pd.DataFrame(table_data[1:], columns=['Rank', 'Handle', '# of solved problems','Penalty'])

    return df


def merge(contests):
    total = contests[0]
    for i in range(1, len(contests)):
        suffix1 = str(i)
        suffix2 = str(i + 1)
        total = pd.merge(total, contests[i], on='Handle',how= 'outer', suffixes=('', f'_{suffix2}'))

    total.fillna(0, inplace=True)

    total['total solved problems'] = total.filter(like='# of solved problems').sum(axis=1)
    total['total penalty'] = total.filter(like='Penalty').sum(axis=1)

    delete_column = total.filter(like= 'Penalty').columns.tolist()
    total = total.drop(columns=delete_column)

    delete_column = total.filter(like= 'Rank').columns.tolist()
    total = total.drop(columns=delete_column)

    total.sort_values(by = ['total solved problems','total penalty'], inplace=True, ignore_index=True , ascending= [False,True])

    total.to_csv("total.csv", index=False)
    print("Done...")


contest_num = int(input('Enter Number of Contests you want to merge their standing, you should enter at least 2 standing to merge  : '))
while contest_num < 2 :
    contest_num = int(input('Enter Number of Contests you want to merge their standing, you should enter at least 2 standing to merge  : '))

df = []
for i in range(1, contest_num + 1):
    url = input(f"Enter Contest URL {i} : ")
    df.append(standing(url))
    df[i-1]['# of solved problems'] = pd.to_numeric(df[i-1]['# of solved problems'], errors='coerce')
    df[i - 1]['Penalty'] = pd.to_numeric(df[i - 1]['Penalty'], errors='coerce')


merge(df)



