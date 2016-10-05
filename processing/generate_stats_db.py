import csv
import os

players_dir = os.path.join("..", "data", "players")
players = os.listdir(players_dir)

FIELDNAMES = {
    'batting': ['Player Id', 'Year', 'Team', 'LG', 'G', 'AB', 'R', 'H', 'TB', '2B', '3B', 'HR', 'RBI', 'BB', 'IBB', 'SO', 'SB', 'CS', 'AVG', 'OBP', 'SLG', 'OPS', 'GO/AO'],
    'batting-advanced1' : ['Player Id', 'Year', 'Team', 'LG', 'PA', 'TB', 'XBH', 'HBP', 'SAC', 'SF', 'BABIP', 'GIDP', 'GIDPO', 'NP', 'P/PA', 'ROE', 'LOB', 'WO'],
    'pitching' : ['Player Id', 'Year', 'Team', 'LG', 'W', 'L', 'ERA', 'G', 'GS', 'CG', 'SHO', 'SV', 'SVO', 'IP', 'H', 'R', 'ER', 'HR', 'HB', 'BB', 'IBB', 'SO', 'AVG', 'WHIP', 'GO/AO'],
    'pitching-advanced1' : ['Player Id', 'Year', 'Team', 'LG', 'QS', 'GF', 'HLD', '2B', '3B', 'GIDP', 'GIDPO', 'WP', 'BK', 'SB', 'CS', 'PK', 'NP', 'S%', 'P/IP', 'P/PA'],
    'pitching-advanced2' : ['Player Id', 'Year', 'Team', 'LG', 'WPCT', 'RS/9', 'TBF', 'BABIP', 'OBP', 'SLG', 'OPS', 'K/9', 'BB/9', 'HR/9', 'H/9', 'K/BB', 'IR', 'IR_S', 'BQR', 'BQR_S'],
    'fielding' : ['Player Id', 'Year', 'Team', 'LG', 'POS', 'G', 'GS', 'INN', 'TC', 'PO', 'A', 'E', 'DP', 'PB', 'SB', 'CS', 'RF', 'FPCT']
}

# Process each type of stats for each player
for stats_type in FIELDNAMES.keys():
    with open(os.path.join("..", "data", "db", "{}.csv".format(stats_type)), "w") as stats_out:
        writer = csv.DictWriter(stats_out, FIELDNAMES[stats_type])
        writer.writeheader()
        for player_id in players:
            path = os.path.join(players_dir, player_id, "{}.csv".format(stats_type))
            try:
                with open(path, "r") as stats_in:
                    reader = csv.DictReader(stats_in)
                    for row in reader:
                        writer.writerow(row)
            except:
                print("No {} for player {}.".format(stats_type, player_id))


