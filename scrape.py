import time
import csv
import json
import random
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup, Comment
from io import StringIO

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
})

season_url = "https://www.hockey-reference.com/leagues/NHL_2026_skaters.html"
response = session.get(season_url)

# Check if you got through
print(response.status_code)
if response.status_code == 429:
    print("Rate limited, waiting...")
    time.sleep(60)  # wait a full minute before retrying
    response = session.get(season_url)

html = response.text
html = html.replace("<!--", "").replace("-->", "")

soup = BeautifulSoup(html, "lxml")

table = soup.find("table", {"id": "player_stats"})

skater_links = []
goalie_links = []
ranker = "0"
for row in table.tbody.find_all("tr"):
    TM = row.find("th", {"data-stat": "ranker"})
    if TM.get_text() == ranker:
        continue
    else:
        ranker = TM.get_text()
    Goalie = row.find("td", {"data-stat": "pos"})
    player_cell = row.find("td", {"data-stat": "name_display"})
    if player_cell and player_cell.a:
        link = player_cell.a["href"]
        full_url = "https://www.hockey-reference.com" + link
        if Goalie.get_text() == "G":
            goalie_links.append(full_url)
        else:
            skater_links.append(full_url)

print(f"Found {len(skater_links)} skaters + {len(goalie_links)} goalies")

time.sleep(5)

print("Grabbing stats. To avoid getting kicked by Sports Reference, each player page is accessed 2-5s apart. Please be patient...")

post = {'C':'C', 'LW':'W', 'RW':'W', 'D':'D', 'G':'G', 'F':'W'}
seasons = []
statstids = []
glk = random.randint(0,10)
teamnum = {
    "MTL": 0,
    "TRS": 1,
    "TOR": 1,
    "MTW": 2,
    "OTS": 3,
    "STE": 3,
    "HAM": 4,
    "BOS": 5,
    "MTM": 6,
    "PIP": 7,
    "PHQ": 7,
    "NYA": 8,
    "BRO": 8,
    "CBH": 9,
    "CHI": 9,
    "DET": 10,
    "NYR": 11,
    "LAK": 12,
    "OAK": 13,
    "CGS": 13,
    "CLE": 13,
    "PIT": 14,
    "PHI": 15,
    "STL": 16,
    "MNS": 17,
    "DAL": 17,
    "BUF": 18,
    "VAN": 19,
    "ATF": 20,
    "CGY": 20,
    "NYI": 21,
    "CLR": 22,
    "NJD": 22,
    "WSH": 23,
    "EDM": 24,
    "HAR": 25,
    "CAR": 25,
    "QUE": 26,
    "COL": 26,
    "WIN": 27,
    "PHX": 27,
    "ARI": 27,
    "SJS": 28,
    "OTT": 29,
    "TBL": 30,
    "ANA": 31,
    "MDA": 31,
    "FLA": 32,
    "NSH": 33,
    "ATL": 34,
    "WPG": 34,
    "CBJ": 35,
    "MIN": 36,
    "VEG": 37,
    "SEA": 38,
    "UTA": 39
}
skip = {"2TM","3TM","4TM",""}
ywt = 1
poslist = []
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
})
outfile = open("stats.txt", 'w')

for url in skater_links:
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find("script", {"type": "application/ld+json"})
    data = json.loads(script.string)
    if isinstance(data, list):
        data = data[0]
    name = data["name"]
    
    # Find tables by ID using BeautifulSoup
    standard_table = soup.find("table", {"id": "player_stats"})
    playoff_table = soup.find("table", {"id": "player_stats_post"})
    misc_table = soup.find("table", {"id": "stats_misc_plus"})

    # Convert each one to a dataframe
    if standard_table:
        standard_stats = pd.read_html(StringIO(str(standard_table)))[0]
    if playoff_table:
        playoff_stats = pd.read_html(StringIO(str(playoff_table)))[0]
    else:
        cols = standard_stats.columns[5:]
        playoff_stats = pd.DataFrame('', index=range(len(standard_stats)), columns=cols)
    if misc_table:
        misc_stats = pd.read_html(StringIO(str(misc_table)))[0]

    # Remove top and bottom 2 rows
    trimmedst = standard_stats.iloc[0:-2]
    trimmedpo = playoff_stats.iloc[0:-2]
    trimmedmi = misc_stats.iloc[0:-2]

    # Get the first 5 column names
    key_cols = trimmedst.columns[:5].tolist()
    
    # Merge all three together
    combined = trimmedst.merge(trimmedmi, on=key_cols, how="outer",suffixes=('','_misc'))
    if not (trimmedpo.iloc[:, 0] == '').all():
        combined = combined.merge(trimmedpo, on=key_cols, how="outer")
    else:
        combined = pd.concat([combined, trimmedpo], axis=1)

    fox = combined.columns[25]
    foy = combined.columns[72]
    if fox[1] != ('FO%'):
        combined.insert(25,"FO%_x",None)
    if foy[1] != ('FO%'):
        combined.insert(72,"FO%_y",None)
    
    # Save to CSV
    combined.to_csv("stats.csv", index=False)
    
    with open("stats.csv", 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        outfile.write(name + '\n')
        outfile.write('"stats":[\n')
        for row in reader:
            if row[2] in skip:
                continue
            if row[3] != "NHL":
                continue
            sea = row[0]
            yrs = sea.split('-')
            season = str(int(yrs[0])+1)
            seasons = seasons + [season]
            tid = teamnum[row[2]]
            tidlist = [tid]
            if statstids == []:
                ywt = 1
                statstids = statstids + tidlist
            else:
                if tid == statstids[-1]:
                    ywt = ywt+1
                else:
                    statstids = statstids + tidlist
                    ywt = 1
            pos = post[row[4]]
            poslist = poslist + [pos]
            gps = row[5]
            pms = row[9]
            pims = row[10]
            evgs = row[11]
            ppgs = row[12]
            shgs = row[13]
            gwgs = row[14]
            evas = row[15]
            ppas = row[16]
            shas = row[17]
            shs = row[18]
            tsas = row[20]
            if tsas == '':
                tsas = 0
            tois = row[21]
            if tois != '':
                times = tois.split(':')
                mins = int(times[0])+1
            else:
                mins = '1'
            fows = row[23]
            if fows == '':
                fows = 0
            fols = row[24]
            if fols == '':
                fols = 0
            blks = row[26]
            hits = row[27]      
            tks = row[28]
            gvs = row[29]
                
            gc = row[35]
            ops = row[41]
            dps = row[42]
            
            gpp = row[52]
            pmp = row[56]
            pimp = row[57]
            evgp = row[58]
            ppgp = row[59]
            shgp = row[60]
            gwgp = row[61]
            evap = row[62]
            if evap == '':
                evap = [54]
            ppap = row[63]
            if ppap == '':
                ppap = 0
            shap = row[64]
            if shap == '':
                shap = 0
            shp = row[65]
            tsap = row[67]
            if tsap == '':
                tsap = 0
            toip = row[68]
            if toip != '':
                timep = toip.split(':')
                minp = int(timep[0])+1
            else:
                minp = '1'
            fowp = row[70]
            if fowp == '':
                fowp = 0
            folp = row[71]
            if folp == '':
                folp = 0
            blkp = row[73]
            hitp = row[74]     
            tkp = row[75]
            gvp = row[76]
                
            if gps != '':
                outfile.write('{"playoffs": false, "season": ' + season + ',\n')
                outfile.write('"tid": ' + str(tid) + ', "yearsWithTeam":' + str(ywt) + ', "gc": ' + str(gc) + ',\n')
                outfile.write('"ops": ' + str(ops) + ', "dps": ' + str(dps) + ', "gps": 0,\n')
                outfile.write('"gp": ' + str(gps) + ', "gpSkater": ' + str(gps) + ',\n')
                outfile.write('"min": ' + str(mins) + ', "pm": ' + str(pms) + ',\n')
                outfile.write('"pim": ' + str(pims) + ', "evG": ' + str(evgs) + ',\n')
                outfile.write('"ppG": ' + str(ppgs) + ', "shG": ' + str(shgs) + ',\n')
                outfile.write('"gwG": ' + str(gwgs) + ', "evA": ' + str(evas) + ',\n')
                outfile.write('"ppA": ' + str(ppas) + ', "shA": ' + str(shas) + ',\n')
                outfile.write('"gpGoalie":0,"gMin":0,"minAvailable":0,"shft":0,"gwA":0,"ga":0,"sv":0,"gW":0,"gL":0,"gT":0,"gOTL":0,"so":0,"gs":0,"ppMin":0,"shMin":0,\n')
                outfile.write('"fow":'+str(fows)+',"fol":'+str(fols)+',"blk":'+str(blks)+',"hit":'+str(hits)+',\n"tk":'+str(tks)+',"gv":'+str(gvs)+',"tsa":'+str(tsas)+',"s": ' + str(shs) + ',\n')
                outfile.write('"jerseyNumber": "qq"},\n')
            if gpp != '':
                outfile.write('{"playoffs": true, "season": ' + season + ',\n')
                outfile.write('"tid": ' + str(tid) + ',\n')
                outfile.write('"gp": ' + str(gpp) + ', "gpSkater": ' + str(gpp) + ',\n')
                outfile.write('"min": ' + str(minp) + ', "pm": ' + str(pmp) + ',\n')
                outfile.write('"pim": ' + str(pimp) + ', "evG": ' + str(evgp) + ',\n')
                outfile.write('"ppG": ' + str(ppgp) + ', "shG": ' + str(shgp) + ',\n')
                outfile.write('"gwG": ' + str(gwgp) + ', "evA": ' + str(evap) + ',\n')
                outfile.write('"ppA": ' + str(ppap) + ', "shA": ' + str(shap) + ',\n')
                outfile.write('"fow":'+str(fowp)+',"fol":'+str(folp)+',"blk":'+str(blkp)+',"hit":'+str(hitp)+',"tk":'+str(tkp)+',"gv":'+str(gvp)+',"tsa":'+str(tsap)+',\n')
                outfile.write('"s": ' + str(shp) + ', "jerseyNumber": "qq"},\n')
    outfile.write('],\n"ratings":[')
    for x in range(len(seasons)):
        outfile.write('{"season": ' + str(seasons[x]) + ', "pos": "' + poslist[x] + '",\n')
        outfile.write('"hgt": 50,\n"stre": 50,\n')
        outfile.write('"spd": 50,\n"endu": 50,\n')
        outfile.write('"pss": 50,\n"wst": 50,\n"sst": 50,\n')
        outfile.write('"stk": 50,\n"oiq": 50,\n"chk": 50,\n')
        outfile.write('"blk": 50,\n"fcf": 50,\n"diq": 50,\n')
        outfile.write('"glk": ' + str(glk) + '},\n')
    outfile.write('],\n"statsTids":' + str(statstids) + ',\n\n')
    infile.close()
    
    statstids = []
    seasons = []
    poslist = []

    time.sleep(random.uniform(2,5))
    
outfile.close()
print("Skaters Complete! stats.txt")
time.sleep(3)

seasons = []
statstids = []
ywt = 1
outfile = open("statsG.txt", 'w')

for url in goalie_links:
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find("script", {"type": "application/ld+json"})
    data = json.loads(script.string)
    if isinstance(data, list):
        data = data[0]
    name = data["name"]

    # Find tables by ID using BeautifulSoup
    standard_table = soup.find("table", {"id": "goalie_stats"})
    playoff_table = soup.find("table", {"id": "goalie_stats_post"})

    # Convert each one to a dataframe
    if standard_table:
        standard_stats = pd.read_html(StringIO(str(standard_table)))[0]
    if playoff_table:
        playoff_stats = pd.read_html(StringIO(str(playoff_table)))[0]
    else:
        cols = standard_stats.columns[5:]
        playoff_stats = pd.DataFrame('', index=range(len(standard_stats)), columns=cols)

    # Remove top and bottom 2 rows
    trimmedst = standard_stats.iloc[0:-2]
    trimmedpo = playoff_stats.iloc[0:-2]

    # Get the first 5 column names
    key_cols = trimmedst.columns[:5].tolist()

    if not (trimmedpo.iloc[:, 0] == '').all():
        combined = trimmedst.merge(trimmedpo, on=key_cols, how="outer")
    else:
        combined = pd.concat([trimmedst, trimmedpo], axis=1)

    # Save to CSV
    combined.to_csv("stats.csv", index=False)

    with open("stats.csv", 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        outfile.write(name+'\n')
        outfile.write('"stats":[\n')
        for row in reader:
            if row[2] in skip:
                continue
            if row[3] != "NHL":
                continue
            sea = row[0]
            yrs = sea.split('-')
            season = str(int(yrs[0])+1)
            seasons = seasons + [season]
            tid = teamnum[row[2]]
            tidlist = [tid]
            if statstids == []:
                ywt = 1
                statstids = statstids + tidlist
            else:
                if tid == statstids[-1]:
                    ywt = ywt+1
                else:
                    statstids = statstids + tidlist
                    ywt = 1
            gps = row[5]
            gss = row[6]
            if gss == '':
                gss = 0
            gWs = row[7]
            gLs = row[8]
            gOTLs = row[9]
            gas = row[10]
            svs = row[12]
            sos = row[15]
            tois = row[16]
            times = tois.split(':')
            mins = int(times[0])+1
            gpss = row[23]
            gs = row[24]
            if gs == '':
                gs = 0
            ass = row[25]
            if ass == '':
                ass = 0
            pims = row[27]
            
            gpp = row[29]
            gsp = row[30]
            if gsp == '':
                gsp = 0
            gWp = row[31]
            gLp = row[32]
            gOTLp = row[33]
            gap = row[34]
            svp = row[36]
            sop = row[39]
            toip = row[40]
            timep = toip.split(':')
            if toip != '':
                timep = toip.split(':')
                minp = int(timep[0])+1
            else:
                minp = '1'
            gp = row[46]
            if gp == '':
                gp = 0
            asp = row[47]
            if asp == '':
                asp = 0
            pimp = row[49]

            if gps != '':
                outfile.write('{"playoffs": false, "season": ' + season + ',\n')
                outfile.write('"tid": ' + str(tid) + ', "yearsWithTeam":' + str(ywt) + ', "gc": 0,\n')
                outfile.write('"ops": 0, "dps": 0, "gps": ' + str(gpss) + ',\n')
                outfile.write('"gp": ' + str(gps) + ', "gpGoalie": ' + str(gps) + ',\n')
                outfile.write('"min": ' + str(mins) + ', "pm": 0,\n')
                outfile.write('"pim": ' + str(pims) + ', "evG": ' + str(gs) + ',\n')
                outfile.write('"ppG": 0, "shG": 0, "gwG": 0,\n')
                outfile.write('"evA": ' + str(ass) + ',"ppA": 0, "shA": 0,\n')
                outfile.write('"gMin": ' + str(mins) + ',"ga":' + str(gas) + ',"sv":' + str(svs) + ',\n')
                outfile.write('"gpSkater":0,"minAvailable":0,"shft":0,"gwA":0,"tsa":0,\n')
                outfile.write('"gW":' + str(gWs) + ',"gL":' + str(gLs) + ',"gT":0,"gOTL":' + str(gOTLs) + ',\n')
                outfile.write('"so":' + str(sos) + ',"gs":' + str(gss) + ',"ppMin":0,"shMin":0,"fow":0,"fol":0,"blk":0,"hit":0,"tk":0,"gv":0,\n')
                outfile.write('"s": 0, "jerseyNumber": "qq"},\n')
            if gpp != '':
                outfile.write('{"playoffs": true, "season": ' + season + ',\n')
                outfile.write('"tid": ' + str(tid) + ', "gc":0,\n')
                outfile.write('"ops": 0, "dps": 0, "gps": 0,\n')
                outfile.write('"gp": ' + str(gpp) + ', "gpGoalie": ' + str(gpp) + ',\n')
                outfile.write('"min": ' + str(minp) + ', "pm": 0,\n')
                outfile.write('"pim": ' + str(pimp) + ', "evG": ' + str(gp) + ',\n')
                outfile.write('"ppG": 0, "shG": 0, "gwG": 0,\n')
                outfile.write('"evA": ' + str(asp) + ',"ppA": 0, "shA": 0,\n')
                outfile.write('"gMin": ' + str(minp) + ',"ga":' + str(gap) + ',"sv":' + str(svp) + ',\n')
                outfile.write('"gpSkater":0,"minAvailable":0,"shft":0,"gwA":0,"tsa":0,\n')
                outfile.write('"gW":' + str(gWp) + ',"gL":' + str(gLp) + ',"gT":0,"gOTL":' + str(gOTLp) + ',\n')
                outfile.write('"so":' + str(sop) + ',"gs":' + str(gsp) + ',"ppMin":0,"shMin":0,"fow":0,"fol":0,"blk":0,"hit":0,"tk":0,"gv":0,\n')
                outfile.write('"s": 0, "jerseyNumber": "qq"},\n')
    outfile.write('],\n"ratings":[')
    for x in range(len(seasons)):
        outfile.write('{"season": ' + str(seasons[x]) + ', "pos": "G",\n')
        outfile.write('"hgt": 50,\n"stre": 50,\n')
        outfile.write('"spd": 10,\n"endu": 50,\n')
        outfile.write('"pss": 10,\n"wst": 10,\n"sst": 0,\n')
        outfile.write('"stk": 10,\n"oiq": 0,\n"chk": 10,\n')
        outfile.write('"blk": 0,\n"fcf": 0,\n"diq": 10,\n')
        outfile.write('"glk": 50},\n')
    outfile.write('],\n"statsTids":' + str(statstids) + ',\n\n')
    infile.close()
        
    statstids = []
    seasons = []
    poslist = []

    time.sleep(random.uniform(2,5))
    
outfile.close()
print("Goalies Complete! statsG.txt")
