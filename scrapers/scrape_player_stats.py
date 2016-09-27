# Load player urls from data/cleaned
# Use distinct player url's

import csv
import fnmatch
import os
from os import listdir
import re
import subprocess
import sys

if not os.path.exists("player_urls.txt"):
    print("Requires player_urls.txt. Run extract_player_urls.py first.")
    sys.exit(-1)

dir = os.path.join("..", "data", "cleaned")
files = listdir(dir)

season = "2015"
player_urls = []
players_output_dir = os.path.join("..", "data", "players")

with open("player_urls.txt", "r") as f:
    player_urls = [line.strip() for line in f.readlines()]

# Example: http://mlb.mlb.com/team/player.jsp?player_id=453562
def extract_player_id(url):
    m = re.search(r'player_id=(\d+)', url)
    return m.group(1)

def scrape_player_stats(url, stats_type):
    player_id = extract_player_id(url)
    player_dir = os.path.join(players_output_dir, player_id)
    if not os.path.exists(player_dir):
        os.makedirs(player_dir)
    with open(os.path.join(player_dir, "{}.json".format(stats_type)), "w") as outfile:
        print("Scraping " + url + " for " + stats_type + "...")
        subprocess.run(["phantomjs", os.path.join("js", "player_stats.js"), url, stats_type], stdout=outfile)

if not os.path.exists(players_output_dir):
    os.makedirs(players_output_dir)

stats_types = ['pitching', 'batting', 'fielding']
for url in player_urls[:50]:
    for stats_type in stats_types:
        scrape_player_stats(url, stats_type)








