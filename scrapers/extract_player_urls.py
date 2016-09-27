# Load player urls from data/cleaned
# Use distinct player url's

import csv
import fnmatch
import os
from os import listdir

dir = os.path.join("..", "data", "cleaned")
files = listdir(dir)

season = "2015"
player_urls = []
players_output_dir = os.path.join("..", "data", "players")

for file in files:
    if fnmatch.fnmatch(file, "*-cleaned.{}.csv".format(season)):
        with open(os.path.join(dir, file), "r") as season_stats:
            reader = csv.DictReader(season_stats)
            for row in reader:
                player_urls.append(row['Player URL'])

print("{} url's".format(len(player_urls)))

s = set(player_urls)
print("{} unique player url's".format(len(s)))

with open("player_urls.txt", "w") as out_file:
    for url in s:
        out_file.write(url)
        out_file.write("\n")