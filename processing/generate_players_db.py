import csv
import fnmatch
import os
from os import listdir
import re

names = set()

def extract_player_id(url):
    m = re.search(r'player_id=(\d+)', url)
    return m.group(1)

def normalize_name(name):
    m = re.search(r'([\w\s]+),\s+([\w\s]{1})', name)
    last = m.group(1)
    first = m.group(2)
    norm_name = first[0].lower() + last.lower()
    norm_name = norm_name.replace(' ', '')
    return norm_name

dir = os.path.join("..", "data", "cleaned")
files = listdir(dir)

season = 2015
with open(os.path.join("..", "data", "db", "Players.csv"), "w") as out_file:
    writer = csv.DictWriter(out_file, ['Player Id', 'External Player Id', 'Name'])
    writer.writeheader()
    for file in files:
        if fnmatch.fnmatch(file, "*-cleaned.{}.csv".format(season)):
            print("Processing " + file)
            with open(os.path.join("..", "data", "cleaned", file), "r") as in_file:
                reader = csv.DictReader(in_file)
                for row in reader:
                    out_row = {}
                    name = row['Player']
                    out_row['Name'] = name
                    out_row['External Player Id'] = extract_player_id(row['Player URL'])
                    out_row['Player Id'] = normalize_name(name)
                    writer.writerow(out_row)

