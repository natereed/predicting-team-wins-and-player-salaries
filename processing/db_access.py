import os
import pandas as pd
import csv

#from processing import nameutils

def load_players():
    players = []
    with open(os.path.join("..", "data", "db", "Players.csv"), "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            players.append(row)
    return players

def index_players_by_field(players, field):
    players_by_field = {}
    for player in players:
        value = player[field].strip()
        players_by_field[value] = player
    return players_by_field

def find_player_by_name(players, name):
    players_by_name = index_players_by_field(players, 'Name')
    player = players_by_name.get(name)
    if player:
        return player
    players_by_full_name = index_players_by_field(players, 'Full Name')
    return players_by_full_name.get(name)

def load_players_df():
    return pd.read_csv(os.path.join("..", "data", "db", "Players.csv"), "r",
                       error_bad_lines=False,
                       warn_bad_lines=True,
                       quoting=csv.QUOTE_ALL,
                       quotechar='|',
                       delimiter=',')

def lookup_player_by_name(players_df, player_name):
    # Lookup exact full name
    matches = players_df[players_df['Full Name'].str.contains(player_name)]
    # Assume there is only one match, which should be the case, given the way we have generated player id's
    if len(matches) > 0:
        return matches

    pat = "^{}$".format(player_name.replace(' ', '.*'))
    matches = players_df[players_df['Full Name'].str.contains(pat)]
    if len(matches) > 0:
        return matches

    # Lookup shorter name
    matches = players_df[players_df['Name'].str.contains(pat)]

    if len(matches) == 0:
        return None
    else:
        return matches

def lookup_player(players_df, player_name, season, team):
    print("Looking up player {}, {}, {}".format(player_name, team, season))
    matches_df = lookup_player_by_name(players_df, player_name)

    if matches_df is None or len(matches_df) == 0:
        print("No matches for name " + player_name)
        return None
    else:
        print("Found players matching name " + player_name)

    # If only one player is found, return that player, otherwise we will need to filter on additional criteria
    if matches_df is not None and len(matches_df) == 1:
        print("Found one matching player - returning")
        return matches_df.iloc[0,:]

    print("Found multiple matches: ")
    print(matches_df)

    print("Finding season stats....")
    # Find stats for season
    season_stats_df = pd.read_csv(os.path.join("..", "data", "db", "SeasonStats.csv"))

    # Filter on team and season
    season_stats_df = season_stats_df[season_stats_df['Year'] == season]
    season_stats_df = season_stats_df[season_stats_df['Team'] == team]
    if season_stats_df is not None:
        print("Merging matches with season stats")
        matches_df = pd.merge(matches_df, season_stats_df, on=['Player Id', 'External Player Id'])
    else:
        print("No matches.")
        return None

    if len(matches_df) == 0:
        print("No season stats for player")
        return None

    # If more than one match, we just return the first one
    return matches_df.iloc[0, :]

#players = load_players()
#player = find_player_by_name('Paul Henry Konerko')
#print(player)

#player = find_player_by_name('Tony Gwynn Jr.')
#print(player)

#player = find_player_by_name('Miguel Alfredo Gonzalez')
#print(player)






