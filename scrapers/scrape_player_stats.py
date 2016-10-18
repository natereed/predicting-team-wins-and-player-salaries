# Load player urls from data/cleaned
# Use distinct player url's

import os
from os import listdir
import re
import subprocess
import sys

## TODO: Re-write to use scraping targets, instead of indistr
if not os.path.exists(os.path.join("..", "data", "scraping_targets.json")):
    print("Requires scraping_targets.json. Run extract_scraping_targets.py first.")
    sys.exit(-1)

# Example: http://mlb.mlb.com/team/player.jsp?player_id=453562
def extract_external_player_id(url):
    m = re.search(r'player_id=(\d+)', url)
    return m.group(1)

def scrape_player_stats(url, stats_type):
    player_id = extract_external_player_id(url)
    player_dir = os.path.join(os.path.join("..", "data", "players"), player_id)
    if not os.path.exists(player_dir):
        os.makedirs(player_dir)

    file = os.path.join(player_dir, "{}.json".format(stats_type))
    if os.path.exists(file) and os.path.getsize(file) > 0:
        print("Skipping" + file + ". Already exists.")
        return # Stats already exists

    with open(file, "w") as outfile:
        print("Scraping " + url + " for " + stats_type + "...")
        subprocess.run(["phantomjs", os.path.join("js", "player_stats.js"), url, stats_type], stdout=outfile)

players_output_dir = os.path.join("..", "data", "players")
if not os.path.exists(players_output_dir):
    os.makedirs(players_output_dir)

import json

with open(os.path.join("..", "data", "scraping_targets.json"), "r") as f:
    scraping_targets = json.load(f)
    for player_id in scraping_targets.keys():
        target = scraping_targets[player_id]
        for stats_type in target['Stats Types']:
            scrape_player_stats(target['Player URL'], stats_type)







