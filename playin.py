from bs4 import BeautifulSoup, Comment
import requests
import csv
eastteams = {}
westteams = {}
standings_list = []
for year in range(2000, 2021):
    eastteams[year] = []
    westteams[year] = []
    print(year)
    url = "https://www.basketball-reference.com/leagues/NBA_{}.html".format(year)
    r = requests.get(url)
    nocomments = r.text.replace('--!>', '')
    nocomments = nocomments.replace('<!--', '')
    nocomments = nocomments.replace('-->', '')
    nocomments = nocomments.replace('<--', '')
    soup = BeautifulSoup(nocomments, 'html.parser')
    tables = soup.find_all(class_="table_container")
    for table in tables:
        if table.find('table')['id'] == 'divs_standings_E':
            standings_list.append((year, table, 'E'))
        if table.find('table')['id'] == 'divs_standings_W':
            standings_list.append((year, table, 'W'))
print(len(standings_list))
table = standings_list[0][1]


for standing_pair in standings_list:
    teams = []
    wins = []
    conf = standing_pair[2]
    table = standing_pair[1]
    year = standing_pair[0]
    tbody = table.find('tbody')
    tr_body = tbody.find_all('tr')
    th_body = tbody.find_all('th')
    for trb in tr_body:
        for td in trb.find_all('td'):
            # Get case value
            val = (td.get_text())
            # Get data-stat value
            stat = td.get('data-stat')
            if stat == 'wins':
                wins.append(int(val))
    for th in th_body:
        val = (th.get_text())
        if "vision" not in val:
            teams.append(val)
    for i in range(len(teams)):
        if conf == 'W':
            westteams[year].append((teams[i], wins[i]))
        else:
            eastteams[year].append((teams[i], wins[i]))
masterlist = [['Seven Seed', 'Wins', 'Ten Seed', 'Wins', 'Diff', 'Year']]
with open('seeding.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(masterlist)
for year in westteams.keys():
    wlist = westteams[year]
    elist = eastteams[year]
    wlist = sorted(wlist, key=lambda x:x[1], reverse=True)
    elist = sorted(elist, key=lambda x:x[1], reverse=True)
    e7 = elist[6]
    e10 = elist[9]
    w7 = wlist[6]
    w10 = wlist[9]
    wyearlist = [w7[0], w7[1], w10[0], w10[1], w7[1] - w10[1], year]
    eyearlist = [e7[0], e7[1], e10[0], e10[1], e7[1] - e10[1], year]
    masterlist.append(wyearlist)
    masterlist.append(eyearlist)

with open('seeding.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(masterlist)