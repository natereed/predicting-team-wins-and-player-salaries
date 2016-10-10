import json
import os

import shutil

with open(os.path.join("missing_targets.json")) as f:
    missing_targets = json.load(f)
    for player_id in missing_targets:
        target = missing_targets[player_id]
        ext_player_id = target['External Player Id']
        path = os.path.join("..", "data", "players", ext_player_id)
        if not os.path.exists(path):
            print("{} does not exist. Skipping...".format(path))
            continue
        print("Removing " + path)
        try:
            shutil.rmtree(path)
        except:
            print("Couldn't remove {}.".format(path))




