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

from db_access import lookup_player, load_players_df
from os import listdir

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
seasons = [2011, 2012, 2013, 2014, 2015]

salaries_df = pd.read_csv(os.path.join("..", "data", "db", "Salaries.csv"))
salaries_df = salaries_df[salaries_df['Year'].isin(seasons)]
players_df = load_players_df()

dir = os.path.join("..", "data", "cleaned")
files = listdir(dir)

scraping_targets = {}
players_output_dir = os.path.join("..", "data", "players")

def get_name(last_and_first_initial):
    names = last_and_first_initial.split(',')
    return "{} {}".format(names[1], names[0])

# Iterate over the 3 files per season (fielding, pitching, batting)
missing_players = []

def is_player_in_salaries(row, salaries_df):
    # Filter out players that are not in Salaries (would be a waste of time to scrape)`
    # row['Player'] matches any salaries_df['Name']
    print("Looking up player info for {}, {},  {}".format(row['Player'], season, row['Team']))
    player = lookup_player(players_df, get_name(row['Player']), season, row['Team'])

    print(player)

    if player is not None:
        player_id = player['Player Id']

    return player_id in salaries_df['Player Id'].values

for season in seasons:
    for file in files:
        if fnmatch.fnmatch(file, "*-cleaned.{}.csv".format(season)):
            stats_type = extract_stats_type(file)
            print(stats_type)
            with open(os.path.join(dir, file), "r") as season_stats:
                reader = csv.DictReader(season_stats)
                for row in reader:
                    external_player_id = extract_external_id(row['Player URL'])

#                    if is_player_in_salaries(row, salaries_df)
                    if True:
                        # Get target if it exists, or create a new one
                        target = scraping_targets.get(external_player_id)
                        if not target:
                            target = {}
                            scraping_targets[external_player_id] = target

                        # Populate with meta-data
                        target['External Player Id'] = external_player_id
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
