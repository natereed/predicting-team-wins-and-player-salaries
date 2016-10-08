import csv
import glob
import fnmatch
import os
import re

seasons = [2015]

def extract_stats_type(filename):
    print("{}".format(filename))
    m = re.search(r'(\w+)-cleaned.[0-9]{4}.csv', filename)
    return m.group(1)

def extract_player_id(url):
    m = re.search(r'player_id=([0-9]+)', url)
    return m.group(1)

def get_stats_types_for_player(player_url):
    
missing = []
# Read stats index file
#files = os.listdir(os.path.join("..", "data", "cleaned"))

player_urls = []
with open(os.path.join("..", "data", "player_urls.txt"), "r") as player_urls_in:
    player_urls = player_urls_in.readlines()
    for player_url in player_urls:
        player_id = extract_player_id(player_url)
        print("Looking for " + player_id)
        try:
            stats_types = get_stats_types_for_player(player_id)
            # Look for the stats types for the player, based on which index files this player appeared in
            # (eg. if fielding-cleaned.2015.csv, then we expect fielding.json to contain data)

            player_files = os.listdir(os.path.join("..", "data", "players", player_id))
            for player_file in player_files:
                if fnmatch.fnmatch(player_file, '{}.json)'.format(stats_type)) and os.path.getsize(player_file) == 0:
                    print("Missing {} for player {}".format(stats_type, player_id))
                    missing.append(player_id)
        except:
            print("No directory for " + player_id)
            missing.append(player_id)

print("{} missing players".format(len(list(set(missing)))))
with open("missing.txt", "w") as f:
    for p in missing:
        f.write(p + "\n")
