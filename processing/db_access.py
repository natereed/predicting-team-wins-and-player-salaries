import os
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

#players = load_players()
#player = find_player_by_name('Paul Henry Konerko')
#print(player)

#player = find_player_by_name('Tony Gwynn Jr.')
#print(player)

#player = find_player_by_name('Miguel Alfredo Gonzalez')
#print(player)






