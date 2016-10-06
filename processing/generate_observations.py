import argparse
import pandas as pd
import os

parser = argparse.ArgumentParser()
parser.add_argument("seasons", type=str)
parser.add_argument("num_prior_years", type=int)
parser.add_argument("include_current_year", type=bool)
args = parser.parse_args()

seasons = [int(season) for season in args.seasons.split(",")]
num_prior_years = args.num_prior_years

# TODO:
# Re-order generated columns. Sort by year and statistic.

salaries_df = pd.read_csv(os.path.join("..", "data", "db", "Salaries.csv"))
salaries_df = salaries_df[salaries_df['Year'].isin(pd.Series(seasons))]
salaries_df.sort(columns=['Year', 'Player Id'], ascending=[0, 1])
performance_df = pd.read_csv(os.path.join("..", "data", "db", "Performance.csv"))

missing_players = []

stats = {}
print(str(len(salaries_df)) + " salaries.")
for index, salary_row in salaries_df.iterrows():
    player_id = salary_row['Player Id']  # short name, like 'bcolon'
    salary_year = salary_row['Year']
    print("Player {} in salary year {}".format(player_id, salary_year))
    #print("Player {} in salary year {}".format(player_id, salary_year))
    subset_ind = (performance_df['Player Id'] == player_id) \
                 & (performance_df['Year'] >= salary_year - num_prior_years)
    if args.include_current_year:
        subset_ind &= (performance_df['Year'] <= salary_year)
    else:
        subset_ind &= (performance_df['Year'] < salary_year)

    player_df = performance_df[subset_ind]
    print(str(len(player_df)) + " entries.")

    # Iterate over performance stats for the given player
    # Each row is for a different year. Assemble all years into a single row.
    # Player Id, Year, Team, LG, Year.G, Year.AB,... Year-1.G, Year-1.AB, etc.
    if len(player_df) > 0:
        stats[player_id] = {'Salary Year': str(salary_year),
                            'Annual Salary': salary_row['Avg Annual']}
        for index, year_row in player_df.iterrows():
            play_year = year_row['Year']
            print("Stats for player {}, year {}".format(player_id, play_year))
            for column in performance_df.columns[3:].values:
                year_diff = salary_year - play_year
                if (year_diff == 0):
                    years_relative = ""
                else:
                    years_relative = "-{}".format(year_diff)
                stat_name = "{}.Year{}".format(column, years_relative)
                stats[player_id][stat_name] = year_row[column]
    else:
        print("No performance stats found.")
        missing_players.append(player_id)

with open("missing_stats.txt", "w") as missing_stats_out:
    for missing_player in missing_players:
        missing_stats_out.write(missing_player + "\n")

import json
with open("stats.json", "w") as stats_out:
    json.dump(stats, stats_out)

#print(stats)

print("Creating data frame...")
cols = []
for player_id in stats.keys():
    d = stats[player_id]
    cols.extend(list(d.keys()))
cols = list(set(cols))
cols.sort()
cols.insert(0, 'Player Id')
cols.remove('Annual Salary')
cols.remove('Salary Year')
cols.insert(1, 'Salary Year')
cols.insert(2, 'Annual Salary')

import csv
with open(os.path.join("..", "data", "db", "Observations.csv"), "w") as obs_out:
    writer = csv.DictWriter(obs_out, cols)
    writer.writeheader()
    for player_id in stats.keys():
        d = stats[player_id]
        d['Player Id'] = player_id
        writer.writerow(d)




