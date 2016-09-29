import csv
import os

from nameutils import normalize_first_and_last

fieldnames = ['Player Id', 'Name', 'Total Value', 'Year', 'Position', 'Contract Years', 'Avg Annual', 'Team']
with open(os.path.join("..", "data", "salaries.csv")) as salaries_in:
    reader = csv.DictReader(salaries_in)
    with open(os.path.join("..", "data", "db", "Salaries.csv"), "w") as salaries_out:
        writer = csv.DictWriter(salaries_out, fieldnames)
        writer.writeheader()
        for row in reader:
            out_row = {}
            out_row['Player Id'] = normalize_first_and_last(row['name'])
            out_row['Name'] = row['name']
            out_row['Total Value'] = row['total_value']
            out_row['Year'] = row['year']
            out_row['Position'] = row['pos']
            out_row['Contract Years'] = row['contract_years']
            out_row['Avg Annual'] = row['avg_annual']
            out_row['Team'] = row['team']
            writer.writerow(out_row)



