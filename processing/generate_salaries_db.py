import argparse
import csv
import os
import pandas as pd

from db_access import lookup_player, load_players_df
from nameutils import normalize_first_and_last

parser = argparse.ArgumentParser(description='Generate salaries database')
parser.add_argument("start_season", type=int)
args = parser.parse_args()

fieldnames = ['Player Id', 'Name', 'Total Value', 'Year', 'Position', 'Contract Years', 'Avg Annual', 'Team']

players_df = load_players_df()
print("Players df: " + str(type(players_df)))

num_salaries = 0
num_missing = 0

salaries_df = pd.read_csv(os.path.join("..", "data", "salaries.csv"))
salaries_df = salaries_df[salaries_df['year'] >= args.start_season]
with open(os.path.join("..", "data", "db", "Salaries.csv"), "w") as salaries_out:
    writer = csv.DictWriter(salaries_out, fieldnames)
    writer.writeheader()
    for i, row in salaries_df.iterrows():
        num_salaries += 1
        out_row = {}
        name = row['name']

        player = lookup_player(players_df, name, row['year'], row['team'])
        if player is not None:
            out_row['Player Id'] = player['Player Id']
            out_row['Name'] = row['name']
            out_row['Total Value'] = row['total_value']
            out_row['Year'] = row['year']
            out_row['Position'] = row['pos']
            out_row['Contract Years'] = row['contract_years']
            out_row['Avg Annual'] = row['avg_annual']
            out_row['Team'] = row['team']
            writer.writerow(out_row)
        else:
            print("Missing " + name)
            num_missing += 1

print("Num salaries: {}".format(num_salaries))
print("Num missing performance data: {}".format(num_missing))
