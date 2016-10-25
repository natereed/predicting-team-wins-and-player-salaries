import os
import pandas as pd

def data_frame_from_player_team_year_position_info(d):
    rows = []
    for player_id in d.keys():
        for year in d[player_id].keys():
            year_data = d[player_id][year]
            row = {'playerID': player_id, 'yearID': year}
            if year_data.get('teams'):
                teams = year_data['teams']
                for i, team in enumerate(teams):
                    row['teamID ' + str(i + 1)] = team
                row['Num Teams'] = len(teams)
            if year_data.get('positions'):
                positions = year_data['positions']
                for i, position in enumerate(positions):
                    row['Fielding_POS.' + str(i + 1)] = position
                row['Num Positions'] = len(positions)
            rows.append(row)

    return pd.DataFrame(rows)

def update_player_team_year_position_info(d, player_id, year, teams, positions=None):
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

batting_df = pd.read_csv(os.path.join("..", "data", "lahman", "baseballdatabank-master", "core", "Batting.csv"))
pitching_df = pd.read_csv(os.path.join("..", "data", "lahman", "baseballdatabank-master", "core", "Pitching.csv"))
fielding_df = pd.read_csv(os.path.join("..", "data", "lahman", "baseballdatabank-master", "core", "Fielding.csv"))

# Rename stats
batting_df.columns = list(batting_df.columns[:5]) + ["Batting_" + column for column in batting_df.columns[5:]]
print(batting_df.columns)
pitching_df.columns = list(pitching_df.columns[:5]) + ["Pitching_" + column for column in pitching_df.columns[5:]]
print(pitching_df.columns)
fielding_df.columns = list(fielding_df.columns[:5]) + ["Fielding_" + column for column in fielding_df.columns[5:]]
print(fielding_df.columns)

# Drop stint
batting_df.drop('stint', axis=1, inplace=True)
pitching_df.drop('stint', axis=1, inplace=True)
fielding_df.drop('stint', axis=1, inplace=True)

batting_grouped = batting_df.groupby(['playerID', 'yearID']).sum()
batting_df = batting_grouped.reset_index()

pitching_grouped = pitching_df.groupby(['playerID', 'yearID']).sum()
pitching_df = pitching_grouped.reset_index()

player_team_year_position_info = {}
fielding_grouped = fielding_df.groupby(['playerID', 'yearID'])
for name, group in fielding_grouped:
    player_id = name[0]
    year = name[1]
    teams = set(list(group['teamID'].values))
    positions = set(list(group['Fielding_POS'].values))
    update_player_team_year_position_info(player_team_year_position_info, player_id, year, teams, positions)

fielding_grouped = fielding_grouped.sum()
fielding_df = fielding_grouped.reset_index()
performance_df = pd.merge(batting_df, pitching_df, on=['playerID', 'yearID'], how='outer')
performance_df = pd.merge(performance_df, fielding_df, on=['playerID', 'yearID'], how='outer')

def calculate_batting_averages(df):
    df['Batting_AVG'] = df['Batting_H'] / df['Batting_AB']
    df['Batting_SLG'] = df['Batting_TB'] / df['Batting_AB']
    return df

def calculate_pitching_averages(df):
    df['Pitching_ERA'] = 9 * df['Pitching_ER'] / df['Pitching_IP']
    return df

def calculate_fielding_percentage(df):
    # (putouts + assists) / (putouts + assists + errors)
    df['Fielding_FPCT'] = (df['Fielding_PO'] + df['Fielding_A']) / (df['Fielding_PO'] + df['Fielding_A'] + df['Fielding_E'])
    return df

def calculate_power_speed_number(df):
    df['Batting_PSN'] = 2 * (df['Batting_HR'] * df['Batting_SB']) / (df['Batting_HR'] + df['Batting_SB'])
    return df

def calculate_innings_pitched(df):
    df['Pitching_IP'] = df['Pitching_IPouts'] * 3
    return df

def calculate_total_bases(df):
    df['Batting_TB'] = df['Batting_H'] + 2 * df['Batting_2B'] + 3 * df['Batting_3B'] + 4 * df['Batting_HR']
    return df

def calculate_total_chances(df):
    df['Fielding_TC'] = df['Fielding_A'] + df['Fielding_PO'] + df['Fielding_E']
    return df

performance_df = calculate_total_bases(performance_df)
performance_df = calculate_batting_averages(performance_df)
performance_df = calculate_fielding_percentage(performance_df)
performance_df = calculate_total_chances(performance_df)
performance_df = calculate_innings_pitched(performance_df)
performance_df = calculate_pitching_averages(performance_df)
performance_df = calculate_power_speed_number(performance_df)

cols = list(performance_df.columns.values)
cols.sort()
cols.remove('playerID')
cols.remove('yearID')
cols.insert(0, 'playerID')
cols.insert(1, 'yearID')
performance_df.columns = cols
print(performance_df.columns)

team_and_position_info_df = data_frame_from_player_team_year_position_info(player_team_year_position_info)
performance_df = pd.merge(performance_df, team_and_position_info_df, on=['playerID', 'yearID'])
performance_df.to_csv(os.path.join("..", "data", "db", "Performance.csv"))

