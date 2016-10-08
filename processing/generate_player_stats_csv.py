import csv
import json
import os

FIELDNAMES = {
    'batting': ['Player Id', 'Year', 'Team', 'LG', 'G', 'AB', 'R', 'H', 'TB', '2B', '3B', 'HR', 'RBI', 'BB', 'IBB', 'SO', 'SB', 'CS', 'AVG', 'OBP', 'SLG', 'OPS', 'GO/AO'],
    'batting_advanced1' : ['Player Id', 'Year', 'Team', 'LG', 'PA', 'TB', 'XBH', 'HBP', 'SAC', 'SF', 'BABIP', 'GIDP', 'GIDPO', 'NP', 'P/PA', 'ROE', 'LOB', 'WO'],
    'pitching' : ['Player Id', 'Year', 'Team', 'LG', 'W', 'L', 'ERA', 'G', 'GS', 'CG', 'SHO', 'SV', 'SVO', 'IP', 'H', 'R', 'ER', 'HR', 'HB', 'BB', 'IBB', 'SO', 'AVG', 'WHIP', 'GO/AO'],
    'pitching_advanced1' : ['Player Id', 'Year', 'Team', 'LG', 'QS', 'GF', 'HLD', '2B', '3B', 'GIDP', 'GIDPO', 'WP', 'BK', 'SB', 'CS', 'PK', 'NP', 'S%', 'P/IP', 'P/PA'],
    'pitching_advanced2' : ['Player Id', 'Year', 'Team', 'LG', 'WPCT', 'RS/9', 'TBF', 'BABIP', 'OBP', 'SLG', 'OPS', 'K/9', 'BB/9', 'HR/9', 'H/9', 'K/BB', 'IR', 'IR_S', 'BQR', 'BQR_S'],
    'fielding' : ['Player Id', 'Year', 'Team', 'LG', 'POS', 'G', 'GS', 'INN', 'TC', 'PO', 'A', 'E', 'DP', 'PB', 'SB', 'CS', 'RF', 'FPCT']
}

#players = {}
#with open(os.path.join("..", "data", "db", "Players.csv"), "r") as in_file:
#    reader = csv.DictReader(in_file)
#    for row in reader:
#        players[row['Player Id']] = row

# Write out the player id and standardized player short name along with the performance stats
# as a CSV file.

def lookup_player(player_id):
    with open(os.path.join("..", "data", "db", "Players.csv")) as players_csv:
        reader = csv.DictReader(players_csv)
        for row in reader:
            if (row['External Player Id'] == player_id):
                return row
    return None

def generate_batting_career_stats_csv(player_dir, player_id, career_data):
    player = lookup_player(player_id)
    if (len(career_data) == 0):
        return # No data

    fieldnames = ['Player Id', 'Year', 'Team', 'LG', 'G', 'AB', 'R', 'H', 'TB', '2B', '3B', 'HR', 'RBI', 'BB', 'IBB', 'SO', 'SB', 'CS', 'AVG', 'OBP', 'SLG', 'OPS', 'GO/AO']
    with open(os.path.join(player_dir, "Batting.csv"), "w") as out_file:
        writer = csv.DictWriter(out_file, fieldnames)
        writer.writeheader()
        for row in career_data:
            row['Player Id'] = player['Player Id']
            writer.writerow(row)

def lookup_fieldnames(stats_type, advanced=None):
    key = stats_type
    if advanced:
        key = key + '_advanced' + str(advanced)
    return FIELDNAMES[key]

def generate_stats_csv(player_id, stats_type):
    print(player_id)
    print("Stats type:" + stats_type)
    player_dir = os.path.join(os.path.join("..", "data", "players"), player_id)
    path = os.path.join(player_dir, "{}.json".format(stats_type))
    try:
        data = json.load(open(path, "r"))
    except:
        print("No data found for {}, {}".format(player_id, stats_type))
        return

    player = lookup_player(player_id)

    # Generate career stats
    with open(os.path.join(player_dir, "{}.csv".format(stats_type)), "w") as out_file:
        writer = csv.DictWriter(out_file, lookup_fieldnames(stats_type))
        writer.writeheader()
        for row in data['career']:
            row['Player Id'] = player['Player Id']
            writer.writerow(row)

    if (stats_type == 'fielding'):
        return

    # Generate advanced stats #1 for pitching and batting
    with open(os.path.join(player_dir, "{}-advanced1.csv".format(stats_type)), "w") as out_file:
        writer = csv.DictWriter(out_file, lookup_fieldnames(stats_type, advanced=1))
        print(lookup_fieldnames(stats_type, advanced=1))
        writer.writeheader()
        for row in data['advancedCareerStats1']:
            row['Player Id'] = player['Player Id']
            writer.writerow(row)

    if (stats_type == 'batting'):
        return

    # Generate advanced #2 for pitching
    with open(os.path.join(player_dir, "{}-advanced2.csv".format(stats_type)), "w") as out_file:
        writer = csv.DictWriter(out_file, lookup_fieldnames(stats_type, advanced=2))
        writer.writeheader()
        for row in data['advancedCareerStats2']:
            row['Player Id'] = player['Player Id']
            writer.writerow(row)

stats_dir = os.path.join("..", "data", "players")
player_ids = os.listdir(stats_dir)
for player_id in player_ids:
    player_dir = os.path.join(stats_dir, player_id)

    print("Generating " + player_id)
    # Generate batting
    for stats_type in ['batting', 'pitching', 'fielding']:
        generate_stats_csv(player_id, stats_type)

