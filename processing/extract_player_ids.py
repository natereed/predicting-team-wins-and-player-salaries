import csv
import fnmatch
import os
import re

# Script to be run before scraping player names. Extracts player id's from the cleaned season stats files.
# The player full names will provide a more accurate lookup method when joining stats with salaries using
# the players database (which also depends on the names).

seasons = range(2011, 2015)
dir = os.path.join("..", "data", "cleaned")
files = os.listdir(os.path.join("..", "data", "cleaned"))

player_ids = []
players_output_dir = os.path.join("..", "data", "players")

def extract_player_id(url):
    m = re.search(r'player_id=([0-9]+)', url)
    return m.group(1)

for season in seasons:
    for file in files:
        if fnmatch.fnmatch(file, "*-cleaned.{}.csv".format(season)):
            with open(os.path.join(dir, file), "r") as season_stats:
                reader = csv.DictReader(season_stats)
                for row in reader:
                    player_ids.append(extract_player_id(row['Player URL']))

player_ids = list(set(player_ids))
print("{} id's".format(len(player_ids)))

with open(os.path.join("..", "data", "player_ids.txt"), "w") as out_file:
    for id in player_ids:
        out_file.write(id)
        out_file.write("\n")
