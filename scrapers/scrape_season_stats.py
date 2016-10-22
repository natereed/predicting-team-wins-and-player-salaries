import argparse
import os
import subprocess
import time

PITCHING_URL = "http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+pitching&game_type='R'&season={}&season_type=ANY&league_code='MLB'&sectionType=sp&statType=pitching&page={}&ts={}&playerType=ALL&sportCode='mlb'&split=&team_id=&active_sw=&position='1'&page_type=SortablePlayer&sortOrder='desc'&sortColumn=avg&results=&perPage={}&timeframe=&last_x_days=&extended=0"
HITTING_URL = "http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type='R'&season={}&season_type=ANY&league_code='MLB'&sectionType=sp&statType=hitting&page={}&ts={}&perPage={}&playerType=ALL"
FIELDING_URL = "http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+fielding&game_type='R'&season={}&season_type=ANY&league_code='MLB'&sectionType=sp&statType=fielding&page={}&ts={}&perPage={}&playerType=ALL"

def get_url(year, stats_type, page, per_page):
    timestamp = int(time.time() * 1000)

    return URLS[stats_type].format(year, page, timestamp, per_page)

URLS = {'pitching' : PITCHING_URL,
        'hitting' : HITTING_URL,
        'fielding' : FIELDING_URL}

#years = range(1988,2016)
#stats_types = ['pitching', 'hitting', 'fielding']

def scrape_season_stats(seasons, stats_types, page, per_page):
    downloads_dir = os.path.join("..", "data", "downloads")
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)

    max_retries = 3
    for season in seasons:
        for stats_type in stats_types:
            timestamp = int(time.time() * 1000)
            url = URLS[stats_type].format(season, page, timestamp, per_page)
            print("Scraping...")
            print(url)

            num_retries = 0
            while (num_retries < max_retries):
                path = os.path.join(downloads_dir, "{}.{}.csv".format(stats_type, str(season)))
                with open(path, "w") as outfile:
                    subprocess.run(["phantomjs", "js/season_stats.js", url], stdout=outfile)
                if (os.path.getsize(path) > 0):
                    return;
                num_retries += 1
                print("Re-trying...")
            print("Failed to scrape season {} {} data.".format(season, stats_type))

parser = argparse.ArgumentParser()
parser.add_argument("seasons", type=str)
parser.add_argument("stats_types", type=str)
parser.add_argument("page", type=int, default=1)
parser.add_argument("per_page", type=int, default=99999)

args = parser.parse_args()

print("Seasons: " + str(args.seasons))
print("Types: " + str(args.stats_types))

seasons = args.seasons.split(',')
stats_types = args.stats_types.split(',')
scrape_season_stats(seasons, stats_types, args.page, args.per_page)
