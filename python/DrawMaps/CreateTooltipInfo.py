from python.consts import *
from python.helper.helper import *
import json


def tuple_to_string(tup):
    return f"{tup[0]}_{tup[1]}"

## take dTileMapa nd write content to a json file.
def create_tooltip_info():
    res = {}
    for key, tile_info in dTileMap.items():
        res_tile_info = {}
        for k, v in tile_info.items():
            if k == "terrain":
                res_tile_info[k] = LTerrainXML[v]["Description"]
            elif k == "bonus":
                res_tile_info[k] = LBonusXML[v]["Description"]
            elif k == "feature":
                res_tile_info[k] = LFeatureXML[v]["Description"]
            elif k == "region":
                res_tile_info[k] = dTextXML.get("TXT_KEY_REGION_" + str(v), "").get("English", "")
            elif k == "plot":
                res_tile_info[k] = v[5:].capitalize()  # Remove "PLOT_" prefix and capitalize
        res[tuple_to_string(transform_coordinates(key))] = res_tile_info
        
    with open("json/tooltip_info.json", "w") as f:
        json.dump(res, f, indent=2)


