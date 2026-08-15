import copy
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
response.encoding = "utf-8"

# Check if you got through
print("u/jedzef's NHL stats scraper for ZenGM Hockey roster files!")
if response.status_code == 429:
    print("Rate limited, waiting...")
    time.sleep(60)  # wait a full minute before retrying
    response = session.get(season_url)
    response.encoding = "utf-8"

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

post = {'C':'C', 'LW':'W', 'RW':'W', 'D':'D', 'G':'G', 'F':'W', 'W':'W'}
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


def get_jersey_ranges(soup):
    """Parse the uniform-number icons at the top of a hockey-reference player
    page into a list of (start_year, end_year, jersey_number) tuples, e.g.
    (2013, 2018, '10') for a number worn from the 2013-14 through 2017-18
    seasons."""
    ranges = []
    holder = soup.find("div", class_="uni_holder")
    if not holder:
        return ranges
    for a in holder.find_all("a", class_="poptip"):
        tip = a.get("data-tip", "")
        if "," not in tip:
            continue
        years_part = tip.rsplit(",", 1)[-1].strip()
        m = re.match(r"(\d{4})-(\d{4})", years_part)
        if not m:
            continue
        start, end = int(m.group(1)), int(m.group(2))
        num_match = re.search(r"number=(\d+)", a.get("href", ""))
        if not num_match:
            continue
        ranges.append((start, end, num_match.group(1)))
    return ranges


def jersey_for_season(ranges, season, playoffs=False):
    """season is the ending year of a season, e.g. 2013 for '2012-13'.
    A jersey range (start, end) covers seasons where start < season <= end.
    When a player wore more than one number in the same season (a mid-season
    change), the earliest-listed number is used for the playoff stat line
    and the latest-listed number is used for the regular-season stat line."""
    candidates = [number for start, end, number in ranges if start < season <= end]
    if not candidates:
        return "qq"
    return candidates[0] if playoffs else candidates[-1]


def num(x):
    """Turn a CSV string value into a real JSON-friendly number.
    Mirrors what would happen if the old code's unquoted str(x) had been
    parsed back out of text, but without blowing up on '' or on the
    occasional non-numeric value."""
    if isinstance(x, (int, float, list, dict)):
        return x
    if x is None or x == '':
        return 0
    try:
        return int(x)
    except (ValueError, TypeError):
        try:
            return float(x)
        except (ValueError, TypeError):
            return x


# Every player's {"stats": [...], "ratings": [...], "statsTids": [...]}
# gets collected here, keyed by full player name, instead of being written
# out as hand-formatted text.
players_data = {}

for url in skater_links:
    response = session.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find("script", {"type": "application/ld+json"})
    data = json.loads(script.string)
    if isinstance(data, list):
        data = data[0]
    name = data["name"]
    jersey_ranges = get_jersey_ranges(soup)

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
    combined = trimmedst.merge(trimmedmi, on=key_cols, how="left",suffixes=('','_misc'))
    if not (trimmedpo.iloc[:, 0] == '').all():
        combined = combined.merge(trimmedpo, on=key_cols, how="left")
    else:
        combined = pd.concat([combined, trimmedpo], axis=1)

    fox = combined.columns[25]
    if fox[1] != ('FO%'):
        combined.insert(25,"FO%_x",None)
    sopct = combined.columns[47]
    if sopct[1] != ('Pct'):
        combined.insert(47,"Pct",None)
    popct = combined.columns[66]
    if popct[1] != ('SPCT'):
        combined.insert(66,"SPCT",None)
    foy = combined.columns[72]
    if foy[1] != ('FO%'):
        combined.insert(72,"FO%_y",None)

    # Save to CSV
    combined.to_csv("stats.csv", index=False)

    stats_entries = []
    with open("stats.csv", 'r', encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)
        for row in reader:
            if row[2] in skip:
                continue
            if row[3] != "NHL":
                continue
            sea = row[0]
            yrs = sea.split('-')
            season = int(yrs[0]) + 1
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
                mins = 1
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
                minp = 1
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
                stats_entries.append({
                    "playoffs": False, "season": season,
                    "tid": tid, "yearsWithTeam": ywt, "gc": num(gc),
                    "ops": num(ops), "dps": num(dps), "gps": 0,
                    "gp": num(gps), "gpSkater": num(gps),
                    "min": mins, "pm": num(pms),
                    "pim": num(pims), "evG": num(evgs),
                    "ppG": num(ppgs), "shG": num(shgs),
                    "gwG": num(gwgs), "evA": num(evas),
                    "ppA": num(ppas), "shA": num(shas),
                    "gpGoalie": 0, "gMin": 0, "minAvailable": 0, "shft": 0, "gwA": 0,
                    "ga": 0, "sv": 0, "gW": 0, "gL": 0, "gT": 0, "gOTL": 0, "so": 0,
                    "gs": 0, "ppMin": 0, "shMin": 0,
                    "fow": num(fows), "fol": num(fols), "blk": num(blks), "hit": num(hits),
                    "tk": num(tks), "gv": num(gvs), "tsa": num(tsas), "s": num(shs),
                    "jerseyNumber": jersey_for_season(jersey_ranges, season),
                })
            if gpp != '':
                stats_entries.append({
                    "playoffs": True, "season": season,
                    "tid": tid,
                    "gp": num(gpp), "gpSkater": num(gpp),
                    "min": minp, "pm": num(pmp),
                    "pim": num(pimp), "evG": num(evgp),
                    "ppG": num(ppgp), "shG": num(shgp),
                    "gwG": num(gwgp), "evA": num(evap),
                    "ppA": num(ppap), "shA": num(shap),
                    "fow": num(fowp), "fol": num(folp), "blk": num(blkp), "hit": num(hitp),
                    "tk": num(tkp), "gv": num(gvp), "tsa": num(tsap),
                    "s": num(shp), "jerseyNumber": jersey_for_season(jersey_ranges, season, playoffs=True),
                })

    ratings_entries = []
    seen_seasons = set()
    for x in range(len(seasons)):
        if seasons[x] in seen_seasons:
            continue
        seen_seasons.add(seasons[x])
        ratings_entries.append({
            "season": seasons[x], "pos": poslist[x],
            "hgt": 50, "stre": 50,
            "spd": 50, "endu": 50,
            "pss": 50, "wst": 50, "sst": 50,
            "stk": 50, "oiq": 50, "chk": 50,
            "blk": 50, "fcf": 50, "diq": 50,
            "glk": glk,
        })

    players_data[name] = {
        "stats": stats_entries,
        "ratings": ratings_entries,
        "statsTids": statstids,
    }

    statstids = []
    seasons = []
    poslist = []

    time.sleep(random.uniform(2,5))

print("Skaters Complete!")
time.sleep(3)

seasons = []
statstids = []
ywt = 1

for url in goalie_links:
    response = session.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find("script", {"type": "application/ld+json"})
    data = json.loads(script.string)
    if isinstance(data, list):
        data = data[0]
    name = data["name"]
    jersey_ranges = get_jersey_ranges(soup)

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
        combined = trimmedst.merge(trimmedpo, on=key_cols, how="left")
    else:
        combined = pd.concat([trimmedst, trimmedpo], axis=1)

    # Save to CSV
    combined.to_csv("stats.csv", index=False)

    stats_entries = []
    with open("stats.csv", 'r', encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)
        for row in reader:
            if row[2] in skip:
                continue
            if row[3] != "NHL":
                continue
            sea = row[0]
            yrs = sea.split('-')
            season = int(yrs[0]) + 1
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
            if toip != '':
                timep = toip.split(':')
                minp = int(timep[0])+1
            else:
                minp = 1
            gp = row[46]
            if gp == '':
                gp = 0
            asp = row[47]
            if asp == '':
                asp = 0
            pimp = row[49]

            if gps != '':
                stats_entries.append({
                    "playoffs": False, "season": season,
                    "tid": tid, "yearsWithTeam": ywt, "gc": 0,
                    "ops": 0, "dps": 0, "gps": num(gpss),
                    "gp": num(gps), "gpGoalie": num(gps),
                    "min": mins, "pm": 0,
                    "pim": num(pims), "evG": num(gs),
                    "ppG": 0, "shG": 0, "gwG": 0,
                    "evA": num(ass), "ppA": 0, "shA": 0,
                    "gMin": mins, "ga": num(gas), "sv": num(svs),
                    "gpSkater": 0, "minAvailable": 0, "shft": 0, "gwA": 0, "tsa": 0,
                    "gW": num(gWs), "gL": num(gLs), "gT": 0, "gOTL": num(gOTLs),
                    "so": num(sos), "gs": num(gss), "ppMin": 0, "shMin": 0,
                    "fow": 0, "fol": 0, "blk": 0, "hit": 0, "tk": 0, "gv": 0,
                    "s": 0, "jerseyNumber": jersey_for_season(jersey_ranges, season),
                })
            if gpp != '':
                stats_entries.append({
                    "playoffs": True, "season": season,
                    "tid": tid, "gc": 0,
                    "ops": 0, "dps": 0, "gps": 0,
                    "gp": num(gpp), "gpGoalie": num(gpp),
                    "min": minp, "pm": 0,
                    "pim": num(pimp), "evG": num(gp),
                    "ppG": 0, "shG": 0, "gwG": 0,
                    "evA": num(asp), "ppA": 0, "shA": 0,
                    "gMin": minp, "ga": num(gap), "sv": num(svp),
                    "gpSkater": 0, "minAvailable": 0, "shft": 0, "gwA": 0, "tsa": 0,
                    "gW": num(gWp), "gL": num(gLp), "gT": 0, "gOTL": num(gOTLp),
                    "so": num(sop), "gs": num(gsp), "ppMin": 0, "shMin": 0,
                    "fow": 0, "fol": 0, "blk": 0, "hit": 0, "tk": 0, "gv": 0,
                    "s": 0, "jerseyNumber": jersey_for_season(jersey_ranges, season, playoffs=True),
                })

    ratings_entries = []
    seen_seasons = set()
    for x in range(len(seasons)):
        if seasons[x] in seen_seasons:
            continue
        seen_seasons.add(seasons[x])
        ratings_entries.append({
            "season": seasons[x], "pos": "G",
            "hgt": 50, "stre": 50,
            "spd": 10, "endu": 50,
            "pss": 10, "wst": 10, "sst": 0,
            "stk": 10, "oiq": 0, "chk": 10,
            "blk": 0, "fcf": 0, "diq": 10,
            "glk": 50,
        })

    players_data[name] = {
        "stats": stats_entries,
        "ratings": ratings_entries,
        "statsTids": statstids,
    }

    statstids = []
    seasons = []
    poslist = []

    time.sleep(random.uniform(2,5))

print("Goalies Complete!")


# Write the scraped stats/ratings/statsTids straight to JSON -- no more
# hand-formatted text file and no regex parsing needed to get it back out.
STATS_JSON_FILE = "player_stats.json"
with open(STATS_JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(players_data, f, ensure_ascii=False, indent=2)
print(f"Saved scraped stats to: {STATS_JSON_FILE}")


print("Replacing stats in roster file...")

JSON_FILE = "ZGMH_NHL_25_26_2026_TDL.json"
OUTPUT_FILE = "NHL_26-27_v0.9.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    db = json.load(f)

# Replace fields in NHL json
updated = 0
matched_names = set()

for player in db["players"]:
    full_name = f"{player.get('firstName','')} {player.get('lastName','')}".strip()

    if full_name in players_data:
        player["stats"] = players_data[full_name]["stats"]
        existing_ratings = player.get("ratings", [])
        txt_ratings = [
            rating
            for rating in players_data[full_name]["ratings"]
            if rating["season"] != 2026
        ]
        player["ratings"] = txt_ratings + existing_ratings
        new_ratings = player["ratings"]
        for rating in new_ratings:
            if rating["season"] == 2026:
                rating_2027 = copy.deepcopy(rating)
                rating_2027["season"] = 2027
                player["ratings"].append(rating_2027)
                break
        player["statsTids"] = players_data[full_name]["statsTids"]

        updated += 1
        matched_names.add(full_name)
        print(f"Updated: {full_name}")

print(f"\nUpdated {updated} players")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False)

print(f"Saved: {OUTPUT_FILE}")

# Report players found in the scraped data but not present in the JSON roster file
not_found = sorted(set(players_data.keys()) - matched_names)

if not_found:
    print(f"\n{len(not_found)} player(s) from {STATS_JSON_FILE} were not found in {JSON_FILE}:")
    for name in not_found:
        print(f"  - {name}")
else:
    print(f"\nAll players from {STATS_JSON_FILE} were found in {JSON_FILE}.")
