import os
import pandas as pd
import functools

df = pd.read_csv(os.path.join("..", "data", "db", "Performance.csv"))

# Get rid of entries for multiple teams, replace with the aggregated (roll-up) entry provided
# with team = "n teams".

df['Year'] = df.Year.str.extract("^([0-9]{4})")

# Find the "2 team" entries, replace the year with a valid numeric entry, and delete the other
# individual team entries
# multiple_teams_df = batting_df[batting_df.Year.str.contains("[-]")]
multiple_teams_df = df[df.Team.str.contains("teams")]
for index, row in multiple_teams_df.iterrows():
    print("Year: " + row['Year'])
    print("Player: " + row['Player Id'])
    print("Team: " + row['Team'])
    # row['Year] and row['Player Id'] are the ones to keep

    batting_df = batting_df[((batting_df['Year'] != row['Year']) | (batting_df['Player Id'] != row['Player Id']))
                            | ((batting_df['Year'] == row['Year']) & (batting_df['Player Id'] == row['Player Id'])
                               & (batting_df['Team'] == row['Team']))]

batting_df['Year'] = pd.to_numeric(batting_df['Year'])






