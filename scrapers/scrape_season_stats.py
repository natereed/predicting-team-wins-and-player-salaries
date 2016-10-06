import argparse
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("seasons", type=str)
parser.add_argument("stats_types", type=str)
args = parser.parse_args()

print("Seasons: " + str(args.seasons))
print("Types: " + str(args.stats_types))

seasons = args.seasons.split(',')
stats_types = args.stats_types.split(',')

PITCHING_URL = "http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+pitching&game_type='R'&season={}&season_type=ANY&league_code='MLB'&sectionType=sp&statType=pitching&page=1&ts={}&playerType=ALL&sportCode='mlb'&split=&team_id=&active_sw=&position='1'&page_type=SortablePlayer&sortOrder='desc'&sortColumn=avg&results=&perPage=9999999&timeframe=&last_x_days=&extended=0"
HITTING_URL = "http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type='R'&season={}&season_type=ANY&league_code='MLB'&sectionType=sp&statType=hitting&page=1&ts={}&perPage=9999999"
FIELDING_URL = "http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+fielding&game_type='R'&season={}&season_type=ANY&league_code='MLB'&sectionType=sp&statType=fielding&page=1&ts={}&perPage=9999999"

def get_url(year, stats_type):
    timestamp = int(time.time() * 1000)
    return URLS[stats_type].format(year, timestamp)

URLS = {'pitching' : PITCHING_URL,
        'hitting' : HITTING_URL,
        'fielding' : FIELDING_URL}

#years = range(1988,2016)
#stats_types = ['pitching', 'hitting', 'fielding']

downloads_dir = "../data/downloads"
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

for season in seasons:
    for stats_type in stats_types:
        timestamp = int(time.time() * 1000)
        url = URLS[stats_type].format(season, timestamp)
        print("Scraping...")
        print(url)
        with open("{}/{}.{}.csv".format(downloads_dir, stats_type, str(season)), "w") as outfile:
            subprocess.run(["phantomjs", "js/season_stats.js", url], stdout=outfile)


