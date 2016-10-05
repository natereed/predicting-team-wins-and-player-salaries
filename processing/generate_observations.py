import pandas as pd
import os

# TODO:
# Re-order generated columns. Sort by year and statistic.

salaries_df = pd.read_csv(os.path.join("..", "data", "db", "Salaries.csv"))
salaries_df = salaries_df[salaries_df['Year'] == 2015]
salaries_df = salaries_df.head(100)
salaries_df.sort(columns=['Year', 'Player Id'], ascending=[0, 1])
performance_df = pd.read_csv(os.path.join("..", "data", "db", "Performance.csv"))

stats = {}
for index, salary_row in salaries_df.iterrows():
    player_id = salary_row['Player Id']  # short name, like 'bcolon'
    salary_year = salary_row['Year']

    #print("Player {} in salary year {}".format(player_id, salary_year))
    player_df = performance_df[(performance_df['Player Id'] == player_id) & (performance_df['Year'] <= salary_year)]

    # Iterate over performance stats for the given player
    # Each row is for a different year. Assemble all years into a single row.
    # Player Id, Year, Team, LG, Year.G, Year.AB,... Year-1.G, Year-1.AB, etc.
    if len(player_df) > 0:
        stats[player_id] = {'Salary Year': str(salary_year),
                            'Annual Salary': salary_row['Avg Annual']}
        for index, year_row in player_df.iterrows():
            play_year = year_row['Year']
            print("Player {}, year {}".format(player_id, play_year))
            for column in performance_df.columns[4:].values:
                year_diff = salary_year - play_year
                if (year_diff == 0):
                    years_relative = ""
                else:
                    years_relative = "-{}".format(year_diff)
                stat_name = "Year{}_{}".format(years_relative, column)
                stats[player_id][stat_name] = year_row[column]

#import json
#with open("stats.json", "w") as stats_out:
#    json.dump(stats, stats_out)

#print(stats)

print("Creating data frame...")
cols = []
for player_id in stats.keys():
    d = stats[player_id]
    cols.extend(list(d.keys()))
cols = list(set(cols))

import csv
with open("Observations.csv", "w") as obs_out:
    writer = csv.DictWriter(obs_out, cols)
    writer.writeheader()
    for player_id in stats.keys():
        d = stats[player_id]
        writer.writerow(d)




