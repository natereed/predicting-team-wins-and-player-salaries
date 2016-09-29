import os
import pandas as pd
import re

df = pd.read_csv(os.path.join("..", "data", "salaries.csv"))
df = df[df.year == 2015]

def get_short_name(name):
    m = re.search(r'([\w\s]+),\s+([\w\s]{1})', name)
    last = m.group(1)
    first = m.group(2)
    return first[0].lower() + last.lower()

# Take a name in the form "First Last" and convert to
# flast (first initial followed by last name,
def normalize_name(name):
data = []
for row in df.itertuples():
    name = row[2]

    data.append(row)



