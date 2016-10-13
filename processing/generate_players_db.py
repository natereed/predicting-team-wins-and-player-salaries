import csv
import fnmatch
import os
from os import listdir
import re
import nameutils

names = set()
#position,player_id,number,name,full-name,height_and_weight,batting_and_throwing
players = []
with open(os.path.join("..", "data", "downloads", "players.csv"), "r") as players_in:
    reader = csv.DictReader(players_in)
    for row in reader:
        players.append(row)

with open(os.path.join("..", "data", "db", "Players.csv"), "w") as out_file:
    writer = csv.DictWriter(out_file, ['Player Id', 'Jersey Number', 'Position', 'Full Name', 'Name', 'Height and Weight', 'Batting And Throwing', 'External Player Id'])
    writer.writeheader()
    for player in players:
        out_row = {}
        out_row['Full Name'] = player['full-name']
        out_row['Name'] = player['name']
        out_row['Position'] = player['position']
        out_row['External Player Id'] = player['player_id']
        out_row['Player Id'] = nameutils.normalize_first_and_last(player['full-name'])
        out_row['Height and Weight'] = player['height_and_weight']
        out_row['Batting And Throwing'] = player['batting_and_throwing']
        out_row['Jersey Number'] = player['number']
        writer.writerow(out_row)

