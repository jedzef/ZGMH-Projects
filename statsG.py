import csv
import random

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
ywt = 1
outfile = open("stats.txt", 'w')
with open("statsG.csv", 'r') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    outfile.write('"stats":[\n')
    for row in reader:
        sea = row[0]
        yrs = sea.split('-')
        season = str(int(yrs[0])+1)
        seasonlist = [season]
        seasons = seasons + seasonlist
        if row[2] == '2TM':
            next(reader)
        else:
            if row[2] == '3TM':
                next(reader)
            else:
                if row[2] == '4TM':
                    next(reader)
                else:
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
        gp = row[5]
        gw = row[6]
        gL = row[7]
        gOT = row[8]
        if int(season) < 2005:
            gT = gOT
            gOTL = 0
        else:
            gT = 0
            gOTL = gOT
        ga = row[9]
        sv = row[11]
        if sv == '':
            sv = str((int(ga)*10))
        so = row[14]
        toi = row[15]
        if toi != '':
            time = toi.split(':')
            min = str(int(time[0])+1)
        else:
            min = '1'
        gps = row[19]
        g = row[20]
        a = row[21]
        pim = row[23]

# outfile
        outfile.write('{"playoffs": false, "season": ' + season + ',\n')
        outfile.write('"tid": ' + str(tid) + ', "yearsWithTeam":' + str(ywt) + ', "gc": 0,\n')
        outfile.write('"ops": 0, "dps": 0, "gps": ' + str(gps) + ',\n')
        outfile.write('"gp": ' + str(gp) + ', "gpGoalie": ' + str(gp) + ',\n')
        outfile.write('"min": ' + str(min) + ', "pm": 0,\n')
        outfile.write('"pim": ' + str(pim) + ', "evG": ' + str(g) + ',\n')
        outfile.write('"ppG": 0, "shG": 0, "gwG": 0,\n')
        outfile.write('"evA": ' + str(a) + ',"ppA": 0, "shA": 0,\n')
        outfile.write('"gMin": ' + str(min) + ',"ga":' + str(ga) + ',"sv":' + str(sv) + ',\n')
        outfile.write('"gpSkater":0,"minAvailable":0,"shft":0,"gwA":0,"tsa":0,\n')
        outfile.write('"gW":' + str(gw) + ',"gL":' + str(gL) + ',"gT":' + str(gT) + ',"gOTL":' + str(gOTL) + ',\n')
        outfile.write('"so":' + str(so) + ',"gs":0,"ppMin":0,"shMin":0,"fow":0,"fol":0,"blk":0,"hit":0,"tk":0,"gv":0,\n')
        outfile.write('"s": 0, "jerseyNumber": 1},\n')

outfile.write('],\n"ratings":[')
for x in range(len(seasons)):
    outfile.write('{"season": ' + str(seasons[x]) + ', "pos": "G",\n')
    outfile.write('"hgt": 50,\n"stre": 50,\n')
    outfile.write('"spd": 0,\n"endu": 0,\n')
    outfile.write('"pss": 0,\n"wst": 0,\n"sst": 0,\n')
    outfile.write('"stk": 0,\n"oiq": 0,\n"chk": 0,\n')
    outfile.write('"blk": 0,\n"fcf": 0,\n"diq": 0,\n')
    outfile.write('"glk": 50 },\n')
outfile.write('],\n"statsTids":' + str(statstids) + ', "hof": 1,\n')
outfile.write('"tid": -3, "retiredYear":' + season + ', "pos": "G",\n')
infile.close()
with open("statsPOG.csv", 'r') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    for row in reader:
        sea = row[0]
        yrs = sea.split('-')
        season = str(int(yrs[0])+1)
        seasonlist = [season]
        seasons = seasons + seasonlist
        if row[2] == '2TM':
            next(reader)
        else:
            if row[2] == '3TM':
                next(reader)
            else:
                if row[2] == '4TM':
                    next(reader)
                else:
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
        gp = row[5]
        gw = row[6]
        gL = row[7]
        gOT = row[8]
        if int(season) < 2005:
            gT = gOT
            gOTL = 0
        else:
            gT = 0
            gOTL = gOT
        ga = row[9]
        sv = row[11]
        if sv == '':
            sv = str((int(ga)*10))
        so = row[14]
        toi = row[15]
        if toi != '':
            time = toi.split(':')
            min = str(int(time[0])+1)
        else:
            min = '1'
        g = row[18]
        a = row[19]
        pim = row[21]

# outfile
        outfile.write('{"playoffs": true, "season": ' + season + ',\n')
        outfile.write('"tid": ' + str(tid) + ', "yearsWithTeam":' + str(ywt) + ', "gc":0,\n')
        outfile.write('"ops": 0, "dps": 0, "gps": 0,\n')
        outfile.write('"gp": ' + str(gp) + ', "gpGoalie": ' + str(gp) + ',\n')
        outfile.write('"min": ' + str(min) + ', "pm": 0,\n')
        outfile.write('"pim": ' + str(pim) + ', "evG": ' + str(g) + ',\n')
        outfile.write('"ppG": 0, "shG": 0, "gwG": 0,\n')
        outfile.write('"evA": ' + str(a) + ',"ppA": 0, "shA": 0,\n')
        outfile.write('"gMin": ' + str(min) + ',"ga":' + str(ga) + ',"sv":' + str(sv) + ',\n')
        outfile.write('"gpSkater":0,"minAvailable":0,"shft":0,"gwA":0,"tsa":0,\n')
        outfile.write('"gW":' + str(gw) + ',"gL":' + str(gL) + ',"gT":' + str(gT) + ',"gOTL":' + str(gOTL) + ',\n')
        outfile.write('"so":' + str(so) + ',"gs":0,"ppMin":0,"shMin":0,"fow":0,"fol":0,"blk":0,"hit":0,"tk":0,"gv":0,\n')
        outfile.write('"s": 0, "jerseyNumber": 1},\n')
infile.close()
outfile.close()





