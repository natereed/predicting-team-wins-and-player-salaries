import os
import pandas as pd
import functools

# TODO: Remove unused factor variables LG and Team from each file
# TODO: Reorder columns in output

def drop_columns(df):
    df = df.drop("LG", 1)
    df = df.drop("Team", 1)
    return df

def rename_columns(df, prefix):
    df.columns = list(df.columns[:4]) + [prefix + "_" + column for column in df.columns[4:]]
    # Dropped the first 4 columns?

def clean(df, prefix):
    print(prefix)
    rename_columns(df, prefix)
    # Clean the year column
    df['Year'] = df['Year'].str.extract('([0-9]{4})(\s+\[\-\])*')[0]
    # Replace missing values
    df = df.fillna(0.0)
    # Convert all stats to numeric
    for column in df.columns[5:]:
        #print(column)
        df[column] = pd.to_numeric(df[column], errors='coerce')
    df = df.fillna(0.0)
    df = drop_columns(df)
    #for column in df.columns:
    #    print(column)
    return df

def aggregate(df):
    gb = df.groupby(['Player Id', 'Year']).sum()
    return gb.reset_index()

# Generate Performance.csv
# Read in all player stats and write out to a single table

batting_df = pd.read_csv(os.path.join("..", "data", "db", "batting.csv"))
batting_df = clean(batting_df, "Batting")
batting_df = aggregate(batting_df)

batting_adv1_df = pd.read_csv(os.path.join("..", "data", "db", "batting-advanced1.csv"))
batting_adv1_df = clean(batting_adv1_df, "Advanced_Batting")
batting_adv1_df = aggregate(batting_adv1_df)

fielding_df = pd.read_csv(os.path.join("..", "data", "db", "fielding.csv"))
fielding_df = clean(fielding_df, "Fielding")
fielding_pos = fielding_df['Fielding_POS']
fielding_df = aggregate(fielding_df)
fielding_df['Fielding_POS'] = fielding_pos
for column in fielding_df.columns:
    print(column)

pitching_df = pd.read_csv(os.path.join("..", "data", "db", "pitching.csv"))
pitching_df = clean(pitching_df, "Pitching")
pitching_df = aggregate(pitching_df)

pitching_adv1_df = pd.read_csv(os.path.join("..", "data", "db", "pitching-advanced1.csv"))
pitching_adv1_df = clean(pitching_adv1_df, "Advanced_Pitching")
pitching_adv1_df = aggregate(pitching_adv1_df)

pitching_adv2_df = pd.read_csv(os.path.join("..", "data", "db", "pitching-advanced2.csv"))
pitching_adv2_df = clean(pitching_adv2_df, "Advanced Pitching")
pitching_adv2_df = aggregate(pitching_adv2_df)

#dfs = [batting_df, batting_adv1_df, fielding_df, pitching_df, pitching_adv1, pitching_adv2]
#df = functools.reduce(lambda left, right: pd.merge(left, right, on=["Player Id", "Year"]), dfs)

print("Merging...")
batting_df = pd.merge(batting_df, batting_adv1_df, on=['Player Id', 'Year'])
pitching_df = pd.merge(pitching_df, pitching_adv1_df, on=['Player Id', 'Year'])
pitching_df = pd.merge(pitching_df, pitching_adv2_df, on=['Player Id', 'Year'])
df = pd.merge(batting_df, pitching_df, how='outer', on=['Player Id', 'Year'])

df = pd.merge(df,
              fielding_df,
              how='outer',
              on=['Player Id', 'Year'])

# Replace NaN's introduced by outer join
df = df.fillna(0.0)

df.to_csv(os.path.join("..", "data", "db", "Performance.csv"))
#df = pd.read_csv(os.path.join("..", "db", "Performance.csv"))



