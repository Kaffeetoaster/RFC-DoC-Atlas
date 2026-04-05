from python.consts import *

import config

from PIL import Image, ImageDraw
from pathlib import Path
import json




### load xml resource infos and convert images to png for web usage
update_all_infos(LBonusXML, dArtXML, dTextXML)
update_all_infos(LFeatureXML, dArtXML, dTextXML)
update_all_infos(LTerrainXML, dArtXML, dTextXML)
#update_all_infos(LCivXML, dArtXML, dTextXML)
# Religions dont have an ARTDefineTag, the Path to the Button is in the ReligionXML itself.
# update_all_infos(LReligionXML, dArtXML, dTextXML)





def add_resource_config_entry(config_dict, coords, text, path_art, category, bSpawn):
    entry = {
        "x": coords[0],
        "y": coords[1],
        "display_name": text,
        "source": str(path_art),
        "category": category,
        "spawn": bSpawn # important for color
    }
    config_dict["spawns_and_despawns"].append(entry)
    


### -------------------------------------------------------------- refactor to use for features too.
def update_resource_despawn():
    # updates the resource despawn entries, by getting the reosource, that spawned there before or the starting resource.
    dRemovedResourcesDictExtended = dRemovedResourcesDict
    for (x,y), event in dRemovedResourcesDictExtended.items():
        if (x,y) in dResourcesDict:
            # maybe a spawned resource will despawn
            iresource = dResourcesDict[(x,y)][1]
            dRemovedResourcesDictExtended[(x,y)] = (event, iresource)
        else:
            # otherwise its just the starting resource that despawns
            dRemovedResourcesDictExtended[(x,y)] = (event, dTileMap[(x, iWorldY-1-y)]["bonus"])
    return dRemovedResourcesDictExtended

def update_feature_despawn():
    dRemovedFeaturesDictExtended = dRemovedFeaturesDict
    for (x,y), event in dRemovedFeaturesDictExtended.items():
        if (x,y) in dFeaturesDict:
            # maybe a spawned feature will despawn
            ifeature = dFeaturesDict[(x,y)][1]
            dRemovedFeaturesDictExtended[(x,y)] = (event, ifeature)
        else:
            # otherwise its just the starting feature that despawns
            dRemovedFeaturesDictExtended[(x,y)] = (event, dTileMap[(x, iWorldY-1-y)]["feature"])
    return dRemovedFeaturesDictExtended

def update_Spawnresources():
    dSpawnResourcesDictExtended = dSpawnResourcesDict
    for (x,y), event in dSpawnResourcesDictExtended.items():
        iresource = event[1]
        iCiv = event[0]
        new_event = f"{dBirth[iCiv]} - {LCivXML[iCiv]['Description']} spawn" 
        dSpawnResourcesDictExtended[(x,y)] = (new_event, iresource)
    return dSpawnResourcesDictExtended


### generate tooltip infos and json entries for resource spawn ###
markers_config ={
    "spawns_and_despawns": []  
}
#### resource spawns ###
for coords, event in dResourcesDict.items():
    iresource = event[1]
    year = str(event[0])
    resource_info = LBonusXML[iresource]
    path_art = resource_info["ArtDefineTag"]
    old_img = Image.open(path_art)
    if old_img.size == (64,64):
        img = old_img.crop((3,3,60,60))
        img.save(path_art)
    add_resource_config_entry(markers_config, coords, year, Path(path_art).relative_to(config.OUTPUT_PATH), category = "Resource spawns", bSpawn=True)
    
### resource despawns ###
dRemovedResourcesDictExtended = update_resource_despawn()
# print(dRemovedResourcesDictExtended)
for coords, event in dRemovedResourcesDictExtended.items():
    year = str(event[0])
    iresource = event[1]
    resource_info = LBonusXML[iresource]
    path_art = resource_info["ArtDefineTag"]

    new_path = config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/" / f"{Path(path_art).stem}_despawn.png"
    old_img = Image.open(path_art)
    deletion_img = Image.open("Assets/Art/Interface/Buttons/Deletion.png")

    if old_img.size == (64,64):
        old_img = old_img.crop((3,3,60,60))
    old_img.paste(deletion_img, (0,0), deletion_img)
    old_img.save(new_path)
    add_resource_config_entry(markers_config, coords, year, Path(new_path).relative_to(config.OUTPUT_PATH), category = "Resource despawns", bSpawn=False)

## civ spawn resources
dSpawnResourcesDictExtended = update_Spawnresources()
for (x,y), event in dSpawnResourcesDictExtended.items():
    iresource = event[1]
    text = event[0]
    resource_info = LBonusXML[iresource]
    path_art = resource_info["ArtDefineTag"]
    old_img = Image.open(path_art)
    if old_img.size == (64,64):
        img = old_img.crop((3,3,60,60))
        img.save(path_art)
    add_resource_config_entry(markers_config, (x,y), text, Path(path_art).relative_to(config.OUTPUT_PATH), category = "Civ spawn Resources", bSpawn=True)



### Feature spawns ###

for (x,y), event in dFeaturesDict.items():
    ifeature = event[1]
    year = str(event[0])
    feature_info = LFeatureXML[ifeature]
    text = f"{year} - {feature_info['Description']}"
    path_art = feature_info["ArtDefineTag"]
    old_img = Image.open(path_art)
    if old_img.size == (64,64):
        img = old_img.crop((3,3,60,60))
        img.save(path_art)
    add_resource_config_entry(markers_config, (x,y), text, Path(path_art).relative_to(config.OUTPUT_PATH), category = "Feature spawns and despawns", bSpawn=True)


dRemovedFeaturesDictExtended = update_feature_despawn()
for (x,y), event in dRemovedFeaturesDictExtended.items():
    year = str(event[0])
    ifeature = event[1]
    feature_info = LFeatureXML[ifeature]
    path_art = feature_info["ArtDefineTag"]
    text = f"{year} - {feature_info['Description']}"
    new_path = config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/" / f"{Path(path_art).stem}_despawn.png"
    old_img = Image.open(path_art)
    deletion_img = Image.open("Assets/Art/Interface/Buttons/Deletion.png")

    if old_img.size == (64,64):
        old_img = old_img.crop((3,3,60,60))
    old_img.paste(deletion_img, (0,0), deletion_img)
    old_img.save(new_path)
    add_resource_config_entry(markers_config, (x,y), text, Path(new_path).relative_to(config.OUTPUT_PATH), category = "Feature spawns and despawns", bSpawn=False)






with open("json/tooltips.json", "w") as f:
    json.dump(markers_config, f, indent=2)






