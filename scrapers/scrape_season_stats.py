import subprocess
import time
import os

PITCHING_URL = "http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+pitching&game_type='R'&season={}&season_type=ANY&league_code='MLB'&sectionType=sp&statType=pitching&page=1&ts={}&playerType=QUALIFIER&sportCode='mlb'&split=&team_id=&active_sw=&position='1'&page_type=SortablePlayer&sortOrder='desc'&sortColumn=avg&results=&perPage=9999999&timeframe=&last_x_days=&extended=0"
HITTING_URL = "http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type='R'&season={}&season_type=ANY&league_code='MLB'&sectionType=sp&statType=hitting&page=1&ts={}&perPage=9999999"
FIELDING_URL = "http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+fielding&game_type='R'&season={}&season_type=ANY&league_code='MLB'&sectionType=sp&statType=fielding&page=1&ts={}&perPage=9999999"

URLS = {'pitching' : PITCHING_URL,
        'hitting' : HITTING_URL,
        'fielding' : FIELDING_URL}

years = range(1988,2016)
stats_types = ['pitching', 'hitting', 'fielding']

downloads_dir = "../data/downloads"
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

for year in years:
    for stats_type in stats_types:
        timestamp = int(time.time() * 1000)
        url = URLS[stats_type].format(year, timestamp)
        print("Scraping...")
        print(url)
        with open("{}/{}.{}.csv".format(downloads_dir, stats_type, str(year)), "w") as outfile:
            subprocess.run(["phantomjs", "js/season_stats.js", url], stdout=outfile)


