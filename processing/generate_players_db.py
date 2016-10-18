import csv
import fnmatch
import os
from os import listdir
import re
import nameutils

#position,player_id,number,name,full-name,height_and_weight,batting_and_throwing
players = []
with open(os.path.join("..", "data", "downloads", "players.csv"), "r") as players_in:
    reader = csv.DictReader(players_in)
    for row in reader:
        players.append(row)

names = [nameutils.normalize_first_and_last(player['full-name']) for player in players]
name_counts = {name : names.count(name) for name in names}

unique_normalized_names = {}

multi_name_occurences = {}
for player in players:
    normalized_name = nameutils.normalize_first_and_last(player['full-name'])
    if name_counts[normalized_name] == 1:
        unique_normalized_names[player['player_id']] = normalized_name
    else:
        count = multi_name_occurences.get(normalized_name)
        if not count:
            count = 1
        else:
            count = count + 1
        multi_name_occurences[normalized_name] = count
        unique_normalized_names[player['player_id']] = normalized_name + str(count)

with open(os.path.join("..", "data", "db", "Players.csv"), "w") as out_file:
    writer = csv.DictWriter(out_file,
                            ['Player Id', 'Jersey Number', 'Position', 'Full Name', 'Name', 'Height and Weight', 'Batting And Throwing', 'External Player Id'],
                            quotechar='|', quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for player in players:
        out_row = {}
        out_row['Full Name'] = player['full-name']
        out_row['Name'] = player['name']
        out_row['Position'] = player['position']
        out_row['External Player Id'] = player['player_id']
        out_row['Player Id'] = unique_normalized_names[player['player_id']]
        out_row['Height and Weight'] = player['height_and_weight']
        out_row['Batting And Throwing'] = player['batting_and_throwing']
        out_row['Jersey Number'] = player['number']
        writer.writerow(out_row)

