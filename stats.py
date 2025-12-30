import csv
import random

post = {'C':'C', 'LW':'W', 'RW':'W', 'D':'D', 'G':'G'}
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
    "VGK": 37,
    "SEA": 38,
    "UTA": 39
}
ywt = 1
poslist = []
outfile = open("stats.txt", 'w')
with open("stats.csv", 'r') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    outfile.write('"stats":[\n')
    for row in reader:
        sea = row[0]
        yrs = sea.split('-')
        season = str(int(yrs[0])+1)
        seasons = seasons + [season]
        tid = teamnum[row[2]]
        tidlist = [tid]
        if statstids == []:
            statstids = statstids + tidlist
        else:
            if tid == statstids[-1]:
                ywt = ywt+1
            else:
                statstids = statstids + tidlist
                ywt = 1
        pos = post[row[4]]
        poslist = poslist + [pos]
        gp = row[5]
        pm = row[9]
        if pm == '':
            pm = 0
        pim = row[10]
        evg = row[11]
        if evg == '':
            evg = row[6]
        ppg = row[12]
        if ppg == '':
            ppg = 0
        shg = row[13]
        if shg == '':
            shg = 0
        gwg = row[14]
        eva = row[15]
        if eva =='':
            eva = row[7]
        ppa = row[16]
        if ppa == '':
            ppa = 0
        sha = row[17]
        if sha == '':
            sha = 0
        sh = row[18]
        if sh == '':
            sh = 0
        toi = row[20]
        if toi != '':
            time = toi.split(':')
            min = str(int(time[0])+1)
        else:
            min = '1'
        gc = row[21]
        ops = row[27]
        dps = row[28]

# outfile
        outfile.write('{"playoffs": false, "season": ' + season + ',\n')
        outfile.write('"tid": ' + str(tid) + ', "yearsWithTeam":' + str(ywt) + ', "gc": ' + str(gc) + ',\n')
        outfile.write('"ops": ' + str(ops) + ', "dps": ' + str(dps) + ', "gps": 0,\n')
        outfile.write('"gp": ' + str(gp) + ', "gpSkater": ' + str(gp) + ',\n')
        outfile.write('"min": ' + str(min) + ', "pm": ' + str(pm) + ',\n')
        outfile.write('"pim": ' + str(pim) + ', "evG": ' + str(evg) + ',\n')
        outfile.write('"ppG": ' + str(ppg) + ', "shG": ' + str(shg) + ',\n')
        outfile.write('"gwG": ' + str(gwg) + ', "evA": ' + str(eva) + ',\n')
        outfile.write('"ppA": ' + str(ppa) + ', "shA": ' + str(sha) + ',\n')
        outfile.write('"gpGoalie":0,"gMin":0,"minAvailable":0,"shft":0,"gwA":0,"tsa":0,"ga":0,"sv":0,"gW":0,"gL":0,"gT":0,"gOTL":0,"so":0,"gs":0,"ppMin":0,"shMin":0,"fow":0,"fol":0,"blk":0,"hit":0,"tk":0,"gv":0,')
        outfile.write('"s": ' + str(sh) + ', "jerseyNumber": "9"},\n')

outfile.write('],\n"ratings":[')
for x in range(len(seasons)):
    outfile.write('{"season": ' + str(seasons[x]) + ', "pos": "' + poslist[x] + '",\n')
    outfile.write('"hgt": 50,\n"stre": 50,\n')
    outfile.write('"spd": 50,\n"endu": 50,\n')
    outfile.write('"pss": 50,\n"wst": 50,\n"sst": 50,\n')
    outfile.write('"stk": 50,\n"oiq": 50,\n"chk": 50,\n')
    outfile.write('"blk": 50,\n"fcf": 50,\n"diq": 50,\n')
    outfile.write('"glk": ' + str(glk) + '},\n')
outfile.write('],\n"statsTids":' + str(statstids) + ', "hof": 1,\n')
outfile.write('"tid": -3, "retiredYear":' + season + '\n')
infile.close()
with open("statsPO.csv", 'r') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    for row in reader:
        sea = row[0]
        yrs = sea.split('-')
        season = str(int(yrs[0])+1)
        tid = teamnum[row[2]]
        pos = post[row[4]]
        gp = row[5]
        pm = row[9]
        if pm == '':
            pm = 0
        pim = row[10]
        evg = row[11]
        if evg == '':
            evg = row[6]
        ppg = row[12]
        if ppg == '':
            ppg = 0
        shg = row[13]
        if shg == '':
            shg = 0
        gwg = row[14]
        if gwg == '':
            gwg = 0
        eva = row[15]
        if eva == '':
            eva = row[7]
        ppa = row[16]
        if ppa == '':
            ppa = 0
        sha = row[17]
        if sha == '':
            sha = 0
        sh = row[18]
        if sh == '':
            sh = 0
        toi = row[20]
        if toi != '':
            time = toi.split(':')
            min = str(int(time[0])+1)
        else:
            min = '1'

# outfile
        outfile.write('{"playoffs": true, "season": ' + season + ',\n')
        outfile.write('"tid": ' + str(tid) + ',\n')
        outfile.write('"gp": ' + str(gp) + ', "gpSkater": ' + str(gp) + ',\n')
        outfile.write('"min": ' + str(min) + ', "pm": ' + str(pm) + ',\n')
        outfile.write('"pim": ' + str(pim) + ', "evG": ' + str(evg) + ',\n')
        outfile.write('"ppG": ' + str(ppg) + ', "shG": ' + str(shg) + ',\n')
        outfile.write('"gwG": ' + str(gwg) + ', "evA": ' + str(eva) + ',\n')
        outfile.write('"ppA": ' + str(ppa) + ', "shA": ' + str(sha) + ',\n')
        outfile.write('"s": ' + str(sh) + ', "jerseyNumber": "9"},\n')
infile.close()
outfile.close()





