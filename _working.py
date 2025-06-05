import csv
import random

name = []
post = {'C':'C', 'L':'W', 'R':'W', 'D':'D', 'G':'G'}
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "British Columbia": "BC",
    "Alberta": "AB",
    "Saskatchewan": "SK",
    "Ontario": "ON",
    "Yukon Territories": "YT",
    "Quebec": "QC",
    "Manitoba": "MB",
    "New Brunswick": "NB",
    "Prince Edward Island": "PE",
    "Newfoundland and Labrador": "NL",
    "Nova Scotia": "NS",
    "Northwest Territories": "NT"
}
state = dict(map(reversed, us_state_to_abbrev.items()))
ctyd = {'AUS':'Austria', 'AUT':'Australia', 'BEL':'Belgium', 'BGR':'Bulgaria', 'BHS':'Bahamas', 'BLR':'Belarus', 'BRA':'Brazil', 'BRN':'Brunei Darussalam', 'CAN':'Canada', 'CZE':'Czech Republic', 'CHE':'Switzerland', 'DEU':'Germany', 'DNK':'Denmark', 'EST':'Estonia', 'FIN':'Finland', "FRA":"France", "GBR":"United Kingdom", "HRV":"Croatia", 'HTI':"Haiti", "IDN":"Indonesia", "ITA":"Italy", "JAM":"Jamaica", "JPN":"Japan", "KAZ":"Kazakhstan", "KOR":"South Korea", "LTU":"Lithuania", "LVA":"Latvia", "NGA":"Nigeria", "NLD":"Netherlands", "NOR":"Norway", "POL":"Poland", "PRY":"Paraguay", "RUS":"Russia", "SVK":"Slovakia", "SVN":"Slovenia", "SWE":"Sweden", "TWN":"Taiwan", "TZA":"Tanzania", "UKR":"Ukraine", "USA":"USA", "UZB":"Uzbekistan", "VEN":"Venezuela", "ZAF":"South Africa"}
outfile = open("TEST.txt", 'w')
with open("Skaters.csv", 'r') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    for row in reader:
# BioInfo
        na = row[0]
        sep = na.split(' ')
        firstname = sep[0]
        lastname = sep[1]
        pos = post[row[2]]
        ht = row[26]
        wt = row[27]
        if wt == '--':
            wt = 0
        dob = row[22]
        sep1 = dob.split('-')
        born = sep1[0]
        if row[24] == '--':
            loc1 = row[23]
        else:
            loc1 = state[row[24]]
        loc2 = ctyd[row[25]]
        loc = loc1 + ', ' + loc2
        deb = row[28]
        draft = deb[:len(deb)//2]

# Ratings
        glk = random.randint(0,10)
        gp = int(row[3])
        g = int(row[4])
        a = int(row[5])
        if row[7] != '--':
            pm = int(row[7])
        else:
            pm = 0
        pim = int(row[8])
        if row[21] != '--' and pos == 'C':
            fo = int(float(row[21])) + 30
            if fo >= 92:
                fo = random.randint(50,99)
        else:
            fo = random.randint(4,49)
        if gp >= 1000:
            end = random.randint(90,100)
        if 500 <= gp < 1000:
            end = random.randint(70,89)
        if 100 <= gp < 500:
            end = random.randint(50,69)
        if gp < 100:
            end = random.randint(9,49)      
        if ((g+a)/gp) >= 1:
            ofa = random.randint(90,100)
        if 0.8 <= ((g+a)/gp) < 1:
            ofa = random.randint(75,89)
        if 0.5 <= ((g+a)/gp) < 0.79:
            ofa = random.randint(60,74)
        if ((g+a)/gp) < 0.5:
            ofa = random.randint(20,54)
        if pos == 'D':
            spd = random.randint(1,49)
            stk = random.randint(1,39)
            blk = random.randint(50,99)
        else:
            spd = random.randint(50,100)
            stk = random.randint(40,90)
            blk = random.randint(10,59)
        if (a/gp) >= 0.8:
            pss = random.randint(85,100)
        if 0.5 <= (a/gp) < 0.79:
            pss = random.randint(60,84)
        if 0.25 <= (a/gp) < 0.49:
            pss = random.randint(30,55)
        if (a/gp) < 0.24:
            pss = random.randint(4,29)
        if (g/gp) >= 0.58 and pos != 'D':
            wst = random.randint(85,100)
            sst = random.randint(60,84)
        if 0.4 <= (g/gp) < 0.57 and pos != 'D':
            wst = random.randint(60,84)
            sst = random.randint(30,59)
        if 0.2 <= (g/gp) < 0.39 and pos != 'D':
            wst = random.randint(30,59)
            sst = random.randint(14,29) 
        if (g/gp) < 0.2 and pos != 'D':
            wst = random.randint(4,29)
            sst = random.randint(1,13)
        if (g/gp) >= 0.28 and pos == 'D':
            sst = random.randint(85,100)
            wst = random.randint(60,84)
        if 0.18 <= (g/gp) < 0.27 and pos == 'D':
            sst = random.randint(60,84)
            wst = random.randint(30,59)
        if 0.08 <= (g/gp) < 0.17 and pos == 'D':
            sst = random.randint(30,59)
            wst = random.randint(14,29) 
        if (g/gp) < 0.08 and pos == 'D':
            sst = random.randint(4,29)
            wst = random.randint(1,13)
        if (pim/gp) >= 3:
            chk = random.randint(85,99)
        if 2.5 <= (pim/gp) < 3:
            chk = random.randint(75,84)
        if 2 <= (pim/gp) < 2.4:
            chk = random.randint(60,74)
        if 1.5 <= (pim/gp) < 2:
            chk = random.randint(50,59)
        if 1 <= (pim/gp) < 1.4:
            chk = random.randint(35,49)
        if 0.5 <= (pim/gp) < 0.9:
            chk = random.randint(25,34)
        if (pim/gp) < 0.49:
            chk = random.randint(1,24)
        if pm >= 0 and pos == 'D':
            dfa = random.randint(70,99)
        if pm < 0 and pos == 'D':
            dfa = random.randint(40,69)
        if pm >= 0 and pos != 'D':
            dfa = random.randint(40,69)
        if pm < 0 and pos != 'D':
            dfa = random.randint(10,39)           
        hgt = int(50 + (((((int(ht)) - 72.6778)/3.14282)) * 10.82))
        stre = int(50 + (((((int(wt)) - 197.878)/15.7763)) * 2.155))
        outfile.write('{\n"born": {"year": ' + born + ',' + '"loc": "' + loc + '"},\n')
        outfile.write('"draft": {"round": 0, "pick": 0, "tid": -1, "originalTid": -1, "year": ' + draft + '},\n')
        outfile.write('"tid": -2, "pos": "' + pos + '",\n')	  
        outfile.write('"firstName": "' + firstname + '", "lastName": "' + lastname + '",\n')
        outfile.write('"hgt": ' + str(ht) + ', "weight": ' + str(wt) + ',\n')
        outfile.write('"imgURL": "/img/logos-secondary/PRO.svg",\n')
        outfile.write('"ratings": [{"season": ' + draft + ', "pos": "' + pos + '",\n')
        outfile.write('"hgt": ' + str(hgt) + ',\n"stre": ' + str(stre) + ',\n')
        outfile.write('"spd": ' + str(spd) + ',\n"endu": ' + str(end) + ',\n')
        outfile.write('"pss": ' + str(pss) + ',\n"wst": ' + str(wst) + ',\n"sst": ' + str(sst) + ',\n')
        outfile.write('"stk": ' + str(stk) + ',\n"oiq": ' + str(ofa) + ',\n"chk": ' + str(chk) + ',\n')
        outfile.write('"blk": ' + str(blk) + ',\n"fcf": ' + str(fo) + ',\n"diq": ' + str(dfa) + ',\n')        
        outfile.write('"glk": ' + str(glk) + '}]},\n')
infile.close()
outfile.close()
