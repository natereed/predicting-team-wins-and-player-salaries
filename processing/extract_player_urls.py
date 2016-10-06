# Load player urls from data/cleaned
# Use distinct player url's
# Only use the intersection of players with Salaries (No point in downloading
# stats for all players -- just the ones who have salaries).

import csv
import fnmatch
import os
import pandas as pd

import nameutils
from os import listdir

# Function to convert player name to a player id (standardized short name)
def player_id_from_name(name):
    print(name)
    return nameutils.normalize_last_and_first_initial(name)

# Change this as needed:
seasons = [2015]

salaries_df = pd.read_csv(os.path.join("..", "data", "db", "Salaries.csv"))
salaries_df = salaries_df[salaries_df['Year'].isin(seasons)]

dir = os.path.join("..", "data", "cleaned")
files = listdir(dir)

player_urls = []
players_output_dir = os.path.join("..", "data", "players")

for season in seasons:
    for file in files:
        if fnmatch.fnmatch(file, "*-cleaned.{}.csv".format(season)):
            with open(os.path.join(dir, file), "r") as season_stats:
                reader = csv.DictReader(season_stats)
                for row in reader:
                    if player_id_from_name(row['Player']) in salaries_df['Player Id'].values:
                        player_urls.append(row['Player URL'])

print("{} url's".format(len(player_urls)))

s = set(player_urls)
print("{} unique player url's".format(len(s)))

with open(os.path.join("..", "data", "player_urls.txt"), "w") as out_file:
    for url in s:
        out_file.write(url)
        out_file.write("\n")
