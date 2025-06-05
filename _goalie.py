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
ctyd = {'AUS':'Australia', 'AUT':'Austria', 'BEL':'Belgium', 'BGR':'Bulgaria', 'BHS':'Bahamas', 'BLR':'Belarus', 'BRA':'Brazil', 'BRN':'Brunei Darussalam', 'CAN':'Canada', 'CZE':'Czech Republic', 'CHE':'Switzerland', 'DEU':'Germany', 'DNK':'Denmark', 'EST':'Estonia', 'FIN':'Finland', "FRA":"France", "GBR":"United Kingdom", "HRV":"Croatia", 'HTI':"Haiti", "IDN":"Indonesia", "ITA":"Italy", "JAM":"Jamaica", "JPN":"Japan", "KAZ":"Kazakhstan", "KOR":"South Korea", "LTU":"Lithuania", "LVA":"Latvia", "NGA":"Nigeria", "NLD":"Netherlands", "NOR":"Norway", "POL":"Poland", "PRY":"Paraguay", "RUS":"Russia", "SVK":"Slovakia", "SVN":"Slovenia", "SWE":"Sweden", "TWN":"Taiwan", "TZA":"Tanzania", "UKR":"Ukraine", "USA":"USA", "UZB":"Uzbekistan", "VEN":"Venezuela", "ZAF":"South Africa"}
outfile = open("TEST.txt", 'w')
with open("Goalies.csv", 'r') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    for row in reader:
# BioInfo
        na = row[0]
        sep = na.split(' ')
        firstname = sep[0]
        lastname = sep[1]
        pos = 'G'
        ht = row[23]
        wt = row[24]
        if wt == '--':
            wt = 0
        dob = row[19]
        sep1 = dob.split('-')
        born = sep1[0]
        if row[21] == '--':
            loc1 = row[20]
        else:
            loc1 = state[row[21]]
        loc2 = ctyd[row[22]]
        loc = loc1 + ', ' + loc2
        deb = row[25]
        draft = deb[:len(deb)//2]

# Ratings
        gp = int(row[2])
        fo = random.randint(0,10)
        if gp >= 1000:
            glk = random.randint(80,90)
            end = random.randint(80,90)
        if 700 <= gp < 1000:
            glk = random.randint(70,89)
            end = random.randint(70,89)
        if 400 <= gp < 700:
            glk = random.randint(50,69)
            end = random.randint(50,69)
        if 100 <= gp < 400:
            glk = random.randint(35,49)
            end = random.randint(35,49)            
        if gp < 100:
            glk = random.randint(20,34)
            end = random.randint(20,34)      
        ofa = random.randint(0,10)
        spd = random.randint(0,10)
        stk = random.randint(0,10)
        blk = random.randint(0,10)
        pss = random.randint(0,10)
        wst = random.randint(0,10)
        sst = random.randint(0,10)
        chk = random.randint(0,10)
        dfa = random.randint(0,10)   
        hgt = int(50 + (((((int(ht)) - 72.6778)/3.14282)) * 10.82))
        stre = int(50 + (((((int(wt)) - 197.878)/15.7763)) * 2.155))
        outfile.write('{\n"born": {"year": ' + born + ',' + '"loc": "' + loc + '"},\n')
        outfile.write('"draft": {"round": 0, "pick": 0, "tid": -1, "originalTid": -1, "year": ' + draft + '},\n')
        outfile.write('"tid": -2, "pos": "G",\n')	  
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
