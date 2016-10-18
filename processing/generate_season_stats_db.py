import os
import pandas as pd
import re

data_dir = os.path.join("..", "data", "cleaned")
files = os.listdir(data_dir)

stats_df = pd.DataFrame({}, columns=["Player URL","Player","Team","Year"])
for file in files:
    # Get season
    m = re.match(r'^(.*)-cleaned.([0-9]{4}).csv$', file)
    if m:
        stats_type = m.group(1)
        season = m.group(2)
    else:
        continue # Ignore file

    if os.path.getsize(os.path.join(data_dir, file)) == 0:
       continue

    df = pd.read_csv(os.path.join(data_dir, file))

    if (stats_type == 'hitting'):
        prefix = 'Batting'
    else:
        prefix = stats_type[0].upper() + stats_type[1:]

    # Rename all columns starting with #4
    col_start_index = 4
    df.columns = list(df.columns[:col_start_index]) + [prefix + "_" + column for column in df.columns[col_start_index:]]
    df.columns.insert(4, 'Year')
    df['Year'] = season

    stats_df = pd.merge(stats_df, df, how="outer", on=['Player', 'Team', 'Year', 'Player URL'])

import csv
players_df = pd.read_csv(os.path.join("..", "data", "db", "Players.csv"), quotechar="|", quoting=csv.QUOTE_ALL)

# Add External Player Id field
stats_df['External Player Id'] = stats_df['Player URL'].str.extract('player_id=([0-9]+)')
stats_df['External Player Id'] = pd.to_numeric(stats_df['External Player Id'])

# Drop problematic height and weight column (causes parsing issues)
stats_df = stats_df.drop('Height and Weight', axis=1)

print("Merging...")
stats_df = pd.merge(stats_df, players_df, on=['External Player Id'])
stats_df.to_csv(os.path.join("..", "data", "db", "SeasonStats.csv"))


