import os
import re

def clean_contents(contents):
    contents = contents.replace('\u2593', '')
    contents = contents.replace('\xc2\xa0', '')
    contents = contents.replace('â\u2013', '')
    contents = contents.replace('┬á', '')
    contents = contents.replace('\u00BC', '')
    contents = contents.replace('\u00B2', '')
    return contents

def cleaned_filename(filename):
    match = re.match("([a-z]+)\\.([\\d]{4})\\.csv", filename)
    stat_type = match.group(1)
    year = match.group(2)
    return("{}-cleaned.{}.csv".format(stat_type, year))

cleaned_dir = "../data/cleaned"
if not os.path.exists(cleaned_dir):
    os.makedirs(cleaned_dir)

downloads_dir = "../data/downloads"
downloaded_files = os.listdir(downloads_dir)

for filename in downloaded_files:
    with open("{}/{}".format(downloads_dir, filename), "r") as f:
        contents = f.read()
        contents = clean_contents(contents)

        with open("{}/{}".format(cleaned_dir, cleaned_filename(filename)), "w") as f:
            f.write(contents)


