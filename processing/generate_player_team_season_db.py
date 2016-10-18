import csv
import fnmatch
import os
import pandas as pd

# Take data from the cleaned season stats files and generate a normalized table
# with the following fields:
# - Player Id (normalized name)
# - Team
# - Season (Year)
# - Position (this is the main position from the rankings we scraped, even though a player can actually
# - External Player Id
# play multiple positions)

# Depends on:
# db/Players.csv
# db/Performance.csv (used for player-team-year association)

dir = os.path.join("..", "data", "cleaned")
files = os.listdir(dir)

player_team_seasons = {}

# Lookup player from Players db and stats (for season)
def lookup_player(player_name, team, season):
    players_df = pd.read_csv(os.path.join("..", "data", "db", "Players.csv"))

    # Lookup exact full name
    matches = players_df[players_df['Full Name'] == player_name]
    if matches:
        return matches.iloc[0, :]

    # Lookup shorter name
    pat = "^{}$".format(player_name.replace(' ', '.*'))
    matches = players_df[players_df['Name'].str.contains(pat)]
    if len(matches) == 1:
        return matches

    # Filter performance team, season, position
    player_stats_df = pd.read_csv(os.path.join("..", "data", "db", "Performance.csv"))
    player_stats_df = pd.merge(matches, player_stats_df, on='Player Id')
    player_stats_df = player_stats_df[((player_stats_df['Team 1'] == team) | (player_stats_df['Team 2'] == team)
                                      | (player_stats_df['Team 3'] == team) | (player_stats_df['Team 4'] == team))
                                      & (player_stats_df['Year'] == season)]

    # If there are multiple, for now we just pick the first one. That's the best I can do right now.
    player_stats = player_stats_df.iloc[0, :]
    return players_df[players_df['Player Id'] == player_stats['Player Id']]


    matching_players = players['Name']
for file in files:
    season = extract_season_from_file(file)
    with open(file, "r") as file_in:
        reader = csv.DictReader()
        for row in reader:
            if fnmatch.fnmatch(file, 'pitching-cleaned.*.csv'):
                pos = 'P'
            else:
                pos = row['Pos']

            # Lookup player from Players db
            player = lookup_player(row['Player'],
                                   row['Team'],
                                   season)
            seasons_list = player_team_seasons.get(player['Player Id'])
            if not seasons_list:
                seasons_list = []
                player_team_seasons['Player Id'] = seasons_list
            seasons_list.append({'season' : season,
                                 'position' : pos,
                                 'team' : row['Team']})





