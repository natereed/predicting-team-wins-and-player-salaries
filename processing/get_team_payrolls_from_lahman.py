import os
import pandas as pd

salaries_df = pd.read_csv(os.path.join("..", "data", "lahman", "baseballdatabank-master", "core", "Salaries.csv"))
salaries_df = salaries_df.groupby(['teamID', 'yearID']).sum().reset_index()
salaries_df = salaries_df.rename(columns={'yearID' : 'Year', 'salary' : 'Payroll', 'teamID' : 'Team'})
salaries_df.to_csv(os.path.join("..", "data", "db", "TeamPayrolls.csv"))

