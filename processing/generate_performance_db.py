import os
import pandas as pd
import functools
import re

# TODO: Remove unused factor variables LG and Team from each file
# TODO: Reorder columns in output

def recalculate_batting_averages(df):
    df['Batting_AVG'] = df['Batting_H'] / df['Batting_AB']
    df['Batting_SLG'] = df['Batting_TB'] / df['Batting_AB']
    return df

def recalculate_pitching_averages(df):
    df['Pitching_ERA'] = 9 * df['Pitching_ER'] / df['Pitching_IP']
    return df

def recalculate_fielding_percentage(df):
    # (putouts + assists) / (putouts + assists + errors)
    df['Fielding_FPCT'] = (df['Fielding_PO'] + df['Fielding_A']) / (df['Fielding_PO'] + df['Fielding_A'] + df['Fielding_E'])
    return df

def calculate_power_speed_number(df):
    df['Batting_PSN'] = 2 * (df['Batting_HR'] * df['Batting_SB']) / (df['Batting_HR'] + df['Batting_SB'])
    return df

#def drop_columns(df):
#    df = df.drop("LG", 1)
#    df = df.drop("Team", 1)
#    return df

def rename_columns(df, prefix):
    df.columns = list(df.columns[:4]) + [prefix + "_" + column for column in df.columns[4:]]
    # Dropped the first 4 columns?

def clean_fielding(df):
    return clean(df, "Fielding", 5)

def clean(df, prefix, start_column_index=4):
    print(prefix)
    rename_columns(df, prefix)
    # Clean the year column
    df['Year'] = df['Year'].str.extract('([0-9]{4})(\s+\[\-\])*')[0]
    # Convert all stats to numeric (coerce non-numeric to NaN's):
    for column in df.columns[start_column_index:]:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    #df = drop_columns(df)
    return df

def aggregate(df):
    gb = df.groupby(['Player Id', 'Year']).sum()
    return gb.reset_index()

def update_player_team_year_position_info(d, player_id, year, teams, positions=None):
    teams = set([team for team in teams if not re.match(r'[0-9]+ teams', team)])
    info = d.get(player_id)
    if not info:
        info = {}
        d[player_id] = info

    if not info.get(year):
        year_info = {}
        info[year] = year_info
    year_info = info[year]
    year_info['teams'] = teams

    # Positions can be optional. Don't overwrite.
    if positions:
        year_info['positions'] = positions

def data_frame_from_player_team_year_position_info(d):
    rows = []
    for player_id in d.keys():
        for year in d[player_id].keys():
            year_data = d[player_id][year]
            row = {'Player Id': player_id, 'Year': year}
            if year_data.get('teams'):
                teams = year_data['teams']
                for i, team in enumerate(teams):
                    row['Team ' + str(i + 1)] = team
                row['Num Teams'] = len(teams)
            if year_data.get('positions'):
                positions = year_data['positions']
                for i, position in enumerate(positions):
                    row['Fielding_POS.' + str(i + 1)] = position
                row['Num Positions'] = len(positions)
            rows.append(row)

    return pd.DataFrame(rows)

# Generate Performance.csv
# Read in all player stats and write out to a single table

# Keep player team, year, position in a dict since they will be dropped when the data is aggregated.
player_team_year_position_info = {}

# Batting
batting_df = pd.read_csv(os.path.join("..", "data", "db", "batting.csv"))
print("Batting raw has {} rows".format(len(batting_df)))
batting_df = clean(batting_df, "Batting")
#batting_group_by = batting_df.groupby(['Player Id', 'Year'])
#for name, group in batting_group_by:
#    player_id = name[0]
#    year = name[1]
#    teams = set(list(group['Team'].values))
#    update_player_team_year_position_info(player_team_year_position_info, player_id, year, teams)

batting_df = aggregate(batting_df)
batting_df = recalculate_batting_averages(batting_df)
batting_df = calculate_power_speed_number(batting_df)
batting_adv1_df = pd.read_csv(os.path.join("..", "data", "db", "batting-advanced1.csv"))
batting_adv1_df = clean(batting_adv1_df, "Advanced_Batting")
batting_adv1_df = aggregate(batting_adv1_df)

#############################################################################
# Fielding

fielding_df = pd.read_csv(os.path.join("..", "data", "db", "fielding.csv"))
fielding_df = clean_fielding(fielding_df)
#fielding_pos = pd.DataFrame(fielding_df, columns=['Player Id', 'Year', 'Fielding_POS', 'Team'])
fielding_group_by = fielding_df.groupby(['Player Id', 'Year'])
for name, group in fielding_group_by:
    player_id = name[0]
    year = name[1]
    teams = set(list(group['Team'].values))
    positions = set(list(group['Fielding_POS'].values))
    update_player_team_year_position_info(player_team_year_position_info, player_id, year, teams, positions)

fielding_df = aggregate(fielding_df)
#fielding_df['Fielding_POS'] = fielding_pos
fielding_df = recalculate_fielding_percentage(fielding_df)

#############################################################################
# Pitching

pitching_df = pd.read_csv(os.path.join("..", "data", "db", "pitching.csv"))
pitching_df = clean(pitching_df, "Pitching")
pitching_group_by = pitching_df.groupby(['Player Id', 'Year'])

#for name, group in pitching_group_by:
#    player_id = name[0]
#    year = name[1]
#    teams = set(list(group['Team'].values))
#    update_player_team_year_position_info(player_team_year_position_info, player_id, year, teams)

pitching_df = aggregate(pitching_df)
pitching_df = recalculate_pitching_averages(pitching_df)

pitching_adv1_df = pd.read_csv(os.path.join("..", "data", "db", "pitching-advanced1.csv"))
pitching_adv1_df = clean(pitching_adv1_df, "Advanced_Pitching")
pitching_adv1_df = aggregate(pitching_adv1_df)

pitching_adv2_df = pd.read_csv(os.path.join("..", "data", "db", "pitching-advanced2.csv"))
pitching_adv2_df = clean(pitching_adv2_df, "Advanced Pitching")
pitching_adv2_df = aggregate(pitching_adv2_df)

#dfs = [batting_df, batting_adv1_df, fielding_df, pitching_df, pitching_adv1, pitching_adv2]
#df = functools.reduce(lambda left, right: pd.merge(left, right, on=["Player Id", "Year"]), dfs)

print("Merging...")
print("Batting")
print(len(batting_df))
print(len(batting_adv1_df))
batting_df = pd.merge(batting_df, batting_adv1_df, on=['Player Id', 'Year'])
print(len(batting_df))

print("Pitching")
print(len(pitching_df))
print(len(pitching_adv1_df))
print(len(pitching_adv2_df))
pitching_df = pd.merge(pitching_df, pitching_adv1_df, on=['Player Id', 'Year'])
pitching_df = pd.merge(pitching_df, pitching_adv2_df, on=['Player Id', 'Year'])
df = pd.merge(batting_df, pitching_df, how='outer', on=['Player Id', 'Year'])

print(len(df))
#print("Fielding")
#print(fielding_df)
df = pd.merge(df,
              fielding_df,
              how='outer',
              on=['Player Id', 'Year'])
print(len(df))

### Merge with team and position info
team_and_position_info_df = data_frame_from_player_team_year_position_info(player_team_year_position_info)
print(team_and_position_info_df)

#team_and_position_info_df.to_csv(os.path.join("..", "data", "db", "TeamsAndPositions.csv"))
df = pd.merge(df, team_and_position_info_df, on=['Player Id', 'Year'])
df.to_csv(os.path.join("..", "data", "db", "Performance.csv"))



