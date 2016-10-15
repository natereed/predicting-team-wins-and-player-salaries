# Load player urls from data/cleaned
# Use distinct player url's
# Only use the intersection of players with Salaries (No point in downloading
# stats for all players -- just the ones who have salaries).

import csv
import fnmatch
import nameutils
import os
import pandas as pd
import re

from os import listdir

# Function to convert player name to a player id (standardized short name)
# TODO: Rewrite to use player id from Players.csv
def player_id_from_name(name):
    #print(name)
    return nameutils.normalize_last_and_first_initial(name)

def extract_stats_type(filename):
    #print("{}".format(filename))
    m = re.search(r'(\w+)-cleaned.[0-9]{4}.csv', filename)
    stats_type = m.group(1)
    if (stats_type == 'hitting'):
        return 'batting'
    else:
        return stats_type

def extract_external_id(url):
    m = re.search(r'player_id=([0-9]+)', url)
    return m.group(1)

# Change this as needed:
seasons = [2013, 2014, 2015]

salaries_df = pd.read_csv(os.path.join("..", "data", "db", "Salaries.csv"))
salaries_df = salaries_df[salaries_df['Year'].isin(seasons)]

dir = os.path.join("..", "data", "cleaned")
files = listdir(dir)

scraping_targets = {}
players_output_dir = os.path.join("..", "data", "players")

# Iterate over the 3 files per season (fielding, pitching, batting)
for season in seasons:
    for file in files:
        if fnmatch.fnmatch(file, "*-cleaned.{}.csv".format(season)):
            stats_type = extract_stats_type(file)
            print(stats_type)
            with open(os.path.join(dir, file), "r") as season_stats:
                reader = csv.DictReader(season_stats)
                for row in reader:
                    player_id = player_id_from_name(row['Player'])
                    if player_id in salaries_df['Player Id'].values:
                        external_id = extract_external_id(row['Player URL'])

                        # Get target if it exists, or create a new one
                        target = scraping_targets.get(player_id)
                        if not target:
                            target = {}
                            scraping_targets[player_id] = target

                        # Populate with meta-data
                        target['External Player Id'] = external_id
                        target['Player URL'] = row['Player URL']

                        # Get stats_types for target, if exists. If not, create new one.
                        stats_types = target.get('Stats Types')
                        if not stats_types:
                            stats_types = []
                            target['Stats Types'] = stats_types
                        stats_types = set(stats_types)
                        stats_types.add(stats_type)
                        stats_types = list(stats_types)
                        target['Stats Types'] = stats_types
                        #target['Stats Types'] = stats_types
                        #print("{}, {}".format(external_id, stats_type))

print("{} unique player id's to scrape".format(len(scraping_targets.keys())))

import json
with open(os.path.join("..", "data", "scraping_targets.json"), "w") as out_file:
    json.dump(scraping_targets, out_file)
