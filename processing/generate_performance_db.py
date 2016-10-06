import os
import pandas as pd
import functools

# TODO: Remove unused factor variables LG and Team from each file
# TODO: Reorder columns in output

def remove_duplicate_years(df):
    df['Year'] = df.Year.str.extract("^([0-9]{4})")
    multiple_teams_df = df[df.Team.str.contains("teams")]
    for index, row in multiple_teams_df.iterrows():
        df = df[((df['Year'] != row['Year']) | (df['Player Id'] != row['Player Id']))
                                | ((df['Year'] == row['Year']) & (df['Player Id'] == row['Player Id'])
                                   & (df['Team'] == row['Team']))]
    return df

def rename_columns(df, prefix):
    df.columns = list(df.columns[:4]) + [prefix + "_" + column for column in df.columns[4:]]

def drop_columns(df):
    df = df.drop("LG", 1)
    return df.drop("Team", 1)

def clean(df, prefix):
    rename_columns(df, prefix)
    return drop_columns(df)

# Generate Performance.csv
# Read in all player stats and write out to a single table

batting_df = remove_duplicate_years(pd.read_csv(os.path.join("..", "data", "db", "batting.csv")))
batting_df = clean(batting_df, "Batting")

batting_adv1_df = remove_duplicate_years(pd.read_csv(os.path.join("..", "data", "db", "batting-advanced1.csv")))
batting_adv1_df = clean(batting_adv1_df, "Advanced_Batting")

fielding_df = remove_duplicate_years(pd.read_csv(os.path.join("..", "data", "db", "fielding.csv")))
fielding_df = clean(fielding_df, "Fielding")

pitching_df = remove_duplicate_years(pd.read_csv(os.path.join("..", "data", "db", "pitching.csv")))
pitching_df = clean(pitching_df, "Pitching")

pitching_adv1_df = remove_duplicate_years(pd.read_csv(os.path.join("..", "data", "db", "pitching-advanced1.csv")))
pitching_adv1_df = clean(pitching_adv1_df, "Advanced_Pitching")

pitching_adv2_df = remove_duplicate_years(pd.read_csv(os.path.join("..", "data", "db", "pitching-advanced2.csv")))
pitching_adv2_df = clean(pitching_adv2_df, "Advanced Pitching")

#dfs = [batting_df, batting_adv1_df, fielding_df, pitching_df, pitching_adv1, pitching_adv2]
#df = functools.reduce(lambda left, right: pd.merge(left, right, on=["Player Id", "Year"]), dfs)

batting_df = pd.merge(batting_df, batting_adv1_df, on=['Player Id', 'Year'])

pitching_df = pd.merge(pitching_df, pitching_adv1_df, on=['Player Id', 'Year'])
pitching_df = pd.merge(pitching_df, pitching_adv2_df, on=['Player Id', 'Year'])

df = pd.merge(batting_df, pitching_df, how='outer', on=['Player Id', 'Year'])

df = pd.merge(df,
              fielding_df,
              how='outer',
              on=['Player Id', 'Year'])

df.to_csv(os.path.join("..", "data", "db", "Performance.csv"))
#df = pd.read_csv(os.path.join("..", "db", "Performance.csv"))



