import csv
import glob
import fnmatch
import os
import re
import json

seasons = [2013, 2014, 2015]

def extract_stats_type(filename):
    print("{}".format(filename))
    m = re.search(r'(\w+)-cleaned.[0-9]{4}.csv', filename)
    return m.group(1)

def extract_player_id(url):
    m = re.search(r'player_id=([0-9]+)', url)
    return m.group(1)

#def get_stats_types_for_player(player_url):

missing_targets = {}
# Read stats index file
#files = os.listdir(os.path.join("..", "data", "cleaned"))

player_urls = []
with open(os.path.join("..", "data", "scraping_targets.json"), "r") as scraping_targets_in:
    scraping_targets = json.load(scraping_targets_in)
    for player_id in scraping_targets:
        print("Validating " + player_id)
        target = scraping_targets[player_id]
        target['Player URL']
        external_player_id = target['External Player Id']
        stats_types = target['Stats Types']
        missing = []
        for stats_type in stats_types:
            if (stats_type == 'hitting'):
                stats_type = 'batting'
            # Check players/{external_player_id}/{stats_type}.json
            path = os.path.join("..", "data", "players", external_player_id, stats_type + ".json")
            if (not os.path.isfile(path) or 0 == os.path.getsize(path)):
                print("Empty or missing file for player {}, stats {}".format(external_player_id, stats_type))
                missing.append(stats_type)
        if (len(missing) > 0):
            target['Stats Types'] = missing
            missing_targets[player_id] = target

import json
print("{} missing players".format(len(missing_targets.keys())))
with open("missing_targets.json", "w") as f:
    json.dump(missing_targets, f)

print("Validated {} players".format(len(scraping_targets.keys())))