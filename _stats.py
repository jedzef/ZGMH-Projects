import csv
import random

name = []
post = {'C':'C', 'LW':'W', 'RW':'W', 'D':'D', 'G':'G'}
seasons = []
statstids = []
glk = random.randint(0,10)
teamnum = {
    "MTL": 0,
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
    "WAS": 23,
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
    "VGK": 37,
    "SEA": 38,
    "UTA": 39
}
outfile = open("TEST.txt", 'w') 
with open("gretzky.csv", 'r') as infile:    
    reader = csv.reader(infile)
    header = next(reader)
    outfile.write('"stats":[\n')
    for row in reader:
        lg = row[3]
        if lg != 'NHL':
            next(reader)
        sea = row[0]
          yrs = sea.split('-')
          season = str(int(yrs[0])+1)
          seasonlist = [season]
          seasons = seasons + seasonlist
        tid = teamnum[row[2]]
        tidlist = [tid]
        if tid != statstids[-1]:
            statstids = statstids + tidlist
        pos = post[row[4]]
        gp = row[5]
        pm = row[9]
        pim = row[10]
        evg = row[11]
        ppg = row[12]
        shg = row[13]
        gwg = row[14]
        eva = row[15]
        ppa = row[16]
        sha = row[17]
        sh = row[18]
        toi = row[19]
        if toi != '':
            time = toi.split(':')
            min = str(int(time[0])+1)
        else:
            min = '1'
        gc = row[20]
        ops = row[26]
        dps = row[27]

# outfile
        outfile.write({"playoffs": false, "season": ' + season + ',\n')
        outfile.write('"tid": ' + str(tid) + ', "gc": ' + str(gc) + ',\n')
        outfile.write('"ops": ' + str(ops) + ', "dps": ' + str(dps) + ',\n')
        outfile.write('"gp": ' + str(gp) + ', "gpSkater": ' + str(gp) + ',\n')
        outfile.write('"min": ' + str(min) + ', "pm": ' + str(pm) + ',\n')
        outfile.write('"pim": ' + str(pim) + ', "evG": ' + str(evg) + ',\n')
        outfile.write('"ppG": ' + str(ppg) + ', "shG": ' + str(shg) + ',\n')
        outfile.write('"gwG": ' + str(gwg) + ', "evA": ' + str(eva) + ',\n')
        outfile.write('"ppA": ' + str(ppa) + ', "shA": ' + str(sha) + ',\n')
        outfile.write('"s": ' + str(sh) + ', "jerseyNumber": 99},\n')

outfile.write('],\n"ratings":[')
for x in seasons:
    outfile.write({"season": ' + str(seasons[x]) + ', "pos": "' + pos + '",\n')
    outfile.write('"hgt": 50,\n"stre": 50,\n')
    outfile.write('"spd": 50,\n"endu": 50,\n')
    outfile.write('"pss": 50,\n"wst": 50,\n"sst": 50,\n')
    outfile.write('"stk": 50,\n"oiq": 50,\n"chk": 50,\n')
    outfile.write('"blk": 50,\n"fcf": 50,\n"diq": 50,\n')
    outfile.write('"glk": ' + str(glk) + '},\n')
outfile.write('],\n"statsTids":' + str(statstids) + ', "hof": 1\n')
outfile.write('"tid": -3, "retiredYear":' + season + ', '\n')
infile.close()
outfile.close()






