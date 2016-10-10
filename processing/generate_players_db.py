import csv
import fnmatch
import os
from os import listdir
import re
import nameutils

names = set()

def extract_player_id(url):
    m = re.search(r'player_id=(\d+)', url)
    return m.group(1)

dir = os.path.join("..", "data", "cleaned")
files = listdir(dir)

with open(os.path.join("..", "data", "db", "Players.csv"), "w") as out_file:
    writer = csv.DictWriter(out_file, ['Player Id', 'External Player Id', 'Name'])
    writer.writeheader()
    for file in files:
        if fnmatch.fnmatch(file, "*-cleaned.*.csv"):
            print("Processing " + file)
            with open(os.path.join("..", "data", "cleaned", file), "r") as in_file:
                reader = csv.DictReader(in_file)
                for row in reader:
                    out_row = {}
                    name = row['Player']
                    out_row['Name'] = name
                    out_row['External Player Id'] = extract_player_id(row['Player URL'])
                    print("Normalizing " + name)
                    out_row['Player Id'] = nameutils.normalize_last_and_first_initial(name)
                    writer.writerow(out_row)

