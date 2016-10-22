import csv
import os
import pandas as pd

teams_df = pd.read_csv(os.path.join("..", "data", "db", "Teams.csv"))
def lookup_team_abbr(team):
    matches = teams_df[teams_df['Team'].str.contains(team)]
    if len(matches) == 0:
        import sys
        print("No match for " + team)
        sys.exit(-1)
    return matches['Abbreviation'].values[0].strip()

years = [2011, 2012, 2013, 2014, 2015]

def convert_to_numeric(qty):
    qty = qty.replace('$', '')
    qty = qty.replace(',', '')
    return int(float(qty))

with open(os.path.join("..", "data", "db", "TeamPayrolls.csv"), "w") as payroll_out:
    writer = csv.DictWriter(payroll_out,
                            fieldnames=['Year', 'Team (Abbreviated)', 'Team', 'Payroll', 'Average', 'Median'])
    writer.writeheader()
    for year in years:
        print(year)
        with open(os.path.join("..", "data", "{}_payroll.csv".format(year))) as payroll_in:
            reader = csv.DictReader(payroll_in)
            for row in reader:
                output_row = {}
                output_row['Team'] = row['Team']
                team_abbr = lookup_team_abbr(row['Team'])
                output_row['Team (Abbreviated)'] = team_abbr
                output_row['Year'] = year

                payroll = convert_to_numeric(row['Payroll'])
                output_row['Payroll'] = payroll

                if row.get('Average'):
                    avg = convert_to_numeric(row['Average'])
                    output_row['Average'] = avg
                if row.get('Median'):
                    median = convert_to_numeric(row['Median'])
                    output_row['Median'] = median
                writer.writerow(output_row)


