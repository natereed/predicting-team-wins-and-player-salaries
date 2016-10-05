import os
import pandas as pd
import functools

def remove_duplicate_years(df):
    df['Year'] = df.Year.str.extract("^([0-9]{4})")
    multiple_teams_df = df[df.Team.str.contains("teams")]
    for index, row in multiple_teams_df.iterrows():
        df = df[((df['Year'] != row['Year']) | (df['Player Id'] != row['Player Id']))
                                | ((df['Year'] == row['Year']) & (df['Player Id'] == row['Player Id'])
                                   & (df['Team'] == row['Team']))]
    return df

# Generate Performance.csv
# Read in all player stats and write out to a single table
batting_df = remove_duplicate_years(pd.read_csv(os.path.join("..", "data", "db", "batting.csv")))
batting_adv1_df = remove_duplicate_years(pd.read_csv(os.path.join("..", "data", "db", "batting-advanced1.csv")))
fielding_df = remove_duplicate_years(pd.read_csv(os.path.join("..", "data", "db", "fielding.csv")))
pitching_df = remove_duplicate_years(pd.read_csv(os.path.join("..", "data", "db", "pitching.csv")))
pitching_adv1 = remove_duplicate_years(pd.read_csv(os.path.join("..", "data", "db", "pitching-advanced1.csv")))
pitching_adv2 = remove_duplicate_years(pd.read_csv(os.path.join("..", "data", "db", "pitching-advanced2.csv")))

#dfs = [batting_df, batting_adv1_df, fielding_df, pitching_df, pitching_adv1, pitching_adv2]
#df = functools.reduce(lambda left, right: pd.merge(left, right, on=["Player Id", "Year"]), dfs)

batting_df = pd.merge(batting_df, batting_adv1_df, how='outer', on=['Player Id', 'Year'], suffixes=['_Batting', '_Advanced_Batting'])
pitching_df = pd.merge(pitching_df, pitching_adv1, how='outer', on=['Player Id', 'Year'], suffixes=['_Pitching', '_Advanced_Pitching1'])
pitching_df = pd.merge(pitching_df, pitching_adv2, how='outer', on=['Player Id', 'Year'], suffixes=['_Pitching', '_Advanced_Pitching2'])

df = pd.merge(batting_df, pitching_df, suffixes=['_Batting', '_Pitching'], how='outer', on=['Player Id', 'Year'])
df = pd.merge(df, fielding_df, how='outer', on=['Player Id', 'Year'], suffixes=['_Batting_And_Pitching', '_Fielding'])

df.to_csv(os.path.join("..", "data", "db", "Performance.csv"))
#df = pd.read_csv(os.path.join("..", "db", "Performance.csv"))



