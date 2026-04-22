from python.consts import *
from python.helper.helper import *
import config

from PIL import Image, ImageDraw
from pathlib import Path
import json





def update_resource_despawn():
    # updates the resource despawn entries, by getting the reosource, that spawned there before or the starting resource.
    dRemovedResourcesDictExtended = dRemovedResourcesDict
    for (x,y), event in dRemovedResourcesDictExtended.items():
        if (x,y) in dResourcesDict and dResourcesDict[(x,y)][0] < event:
            # maybe a spawned resource will despawn
            iresource = dResourcesDict[(x,y)][1]
            dRemovedResourcesDictExtended[(x,y)] = (event, iresource)
        else:
            # otherwise its just the starting resource that despawns
            dRemovedResourcesDictExtended[(x,y)] = (event, dTileMap[(x, iWorldY-1-y)].get("bonus", None))
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
            dRemovedFeaturesDictExtended[(x,y)] = (event, dTileMap[(x, iWorldY-1-y)].get("feature", None))
    return dRemovedFeaturesDictExtended

def update_Spawnresources():
    dSpawnResourcesDictExtended = dSpawnResourcesDict
    for (x,y), event in dSpawnResourcesDictExtended.items():
        iresource = event[1]
        iCiv = event[0]
        desc = LCivXML[iCiv]['Description'] if LCivXML[iCiv]['ShortDescription'].startswith("TXT_KEY_CIV_") else LCivXML[iCiv]['ShortDescription']
        new_event = f"{dBirth[iCiv]} - {desc} spawn" 
        dSpawnResourcesDictExtended[(x,y)] = (new_event, iresource)
    return dSpawnResourcesDictExtended



#### resource spawns ###
def draw_resource_spawns(json_config):
    for coords, event in dResourcesDict.items():
        year = str(event[0])
        iresource = event[1]
        resource_info = LBonusXML[iresource]
        path_art = resource_info["ArtDefineTag"]
        old_img = Image.open(path_art)
        new_path = config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/" / f"{Path(path_art).stem}_cropped.png"
        if old_img.size == (64,64):
            img = old_img.crop((3,3,60,60))
            img.save(new_path)
        add_marker_config_entry(json_config, coords, year, Path(new_path).relative_to(config.OUTPUT_PATH), category = "Resource spawns", bSpawn=True)
        
### resource despawns ###
def draw_resource_despawns(json_config):
    dRemovedResourcesDictExtended = update_resource_despawn()
    # print(dRemovedResourcesDictExtended)
    for coords, event in dRemovedResourcesDictExtended.items():
        year = str(event[0])
        if event[1] is None:
            new_path = config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/Deletion.png"
        else:
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
        add_marker_config_entry(json_config, coords, year, Path(new_path).relative_to(config.OUTPUT_PATH), category = "Resource despawns", bSpawn=False)

## civ spawn resources
def draw_civ_spawn_resources(json_config):
    dSpawnResourcesDictExtended = update_Spawnresources()
    for (x,y), event in dSpawnResourcesDictExtended.items():
        iresource = event[1]
        text = event[0]
        resource_info = LBonusXML[iresource]
        path_art = resource_info["ArtDefineTag"]
        old_img = Image.open(path_art)
        new_path = config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/" / f"{Path(path_art).stem}_cropped.png"
        if old_img.size == (64,64):
            img = old_img.crop((3,3,60,60))
            img.save(new_path)
        add_marker_config_entry(json_config, (x,y), text, Path(new_path).relative_to(config.OUTPUT_PATH), category = "Civ spawn Resources", bSpawn=True)



### Feature spawns and despawns ###
def draw_feature_spawns(json_config):
    for (x,y), event in dFeaturesDict.items():
        ifeature = event[1]
        year = str(event[0])
        feature_info = LFeatureXML[ifeature]
        text = f"{year} - {feature_info['Description']}"
        path_art = feature_info["ArtDefineTag"]
        old_img = Image.open(path_art)
        new_path = config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/" / f"{Path(path_art).stem}_cropped.png"
        if old_img.size == (64,64):
            img = old_img.crop((3,3,60,60))
            img.save(new_path)
        add_marker_config_entry(json_config, (x,y), text, Path(new_path).relative_to(config.OUTPUT_PATH), category = "Feature spawns and despawns", bSpawn=True)

def draw_feature_despawns(json_config):
    dRemovedFeaturesDictExtended = update_feature_despawn()
    for (x,y), event in dRemovedFeaturesDictExtended.items():
        year = str(event[0])
        if event[1] is None:
            new_path = config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/Deletion.png"
        else:
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
        add_marker_config_entry(json_config, (x,y), text, Path(new_path).relative_to(config.OUTPUT_PATH), category = "Feature spawns and despawns", bSpawn=False)

### Terrain changes ###
def draw_terrain_changes(json_config):
    for (x,y), event in dTerrainsDict.items():
        iterrain = event[1]
        year = str(event[0])
        terrain_info = LTerrainXML[iterrain]
        text = f"{year} - {terrain_info['Description']}"
        path_art = terrain_info["ArtDefineTag"]
        old_img = Image.open(path_art)
        new_path = config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/" / f"{Path(path_art).stem}_cropped.png"
        if old_img.size == (64,64):
            img = old_img.crop((4,4,59,59))
            img.save(new_path)
        add_marker_config_entry(json_config, (x,y), text, Path(new_path).relative_to(config.OUTPUT_PATH), category = "Terrain changes", bSpawn=True)

### Plot changes ###
def draw_plot_changes(json_config):
    for (x,y), event in dConquerorPlotTypesDict.items():
        iCiv = event[0]
        text = f"Inca conquerer spawn" 
        ## be careful only hill spawns are supported right now.
        old_img = load_from_atlas(["Art/Interface/Buttons/BaseTerrain_TerrainFeatures_Atlas.dds",4,1])
        
        if old_img.size == (64,64):
            img = old_img.crop((4,4,59,59))
            img.save(config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/Hill_spawn.png")

        add_marker_config_entry(json_config, (x,y), text, Path(config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/Hill_spawn.png").relative_to(config.OUTPUT_PATH), category = "Plot changes", bSpawn=True)    

### Region based resource spawns ###
def draw_region_based_resource_spawns(json_config):
    for (x,y), event in dCivGroupResourcesDict.items():
        tCivs = event[0]
        iResource = event[1]
        text = f"{event[2]} - {', '.join([LCivXML[iCiv]['ShortDescription'] for iCiv in tCivs])}"
        resource_info = LBonusXML[iResource]
        path_art = resource_info["ArtDefineTag"]
        old_img = Image.open(path_art)
        new_path = config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/" / f"{Path(path_art).stem}_cropped.png"
        if old_img.size == (64,64):
            img = old_img.crop((3,3,60,60))
            img.save(new_path)
        add_marker_config_entry(json_config, (x,y), text, Path(new_path).relative_to(config.OUTPUT_PATH), category = "City in same region", bSpawn=True)


### start resources ###
def draw_start_resources(json_config):
    for (x,y), Tile in dTileMap.items():
        if "bonus" in Tile:
            iResource = Tile["bonus"]
            resource_info = LBonusXML[iResource]
            path_art = resource_info["ArtDefineTag"]
            old_img = Image.open(path_art)
            new_path = config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/" / f"{Path(path_art).stem}_cropped.png"
            if old_img.size == (64,64):
                img = old_img.crop((3,3,60,60))
                img.save(new_path)
            text = ""
            add_marker_config_entry(json_config, (x,iWorldY-1-y), text, Path(new_path).relative_to(config.OUTPUT_PATH), category = "Start resources", bSpawn=True)


def draw_tile_markers(json_config):
    draw_resource_spawns(json_config)
    draw_resource_despawns(json_config)
    draw_civ_spawn_resources(json_config)
    draw_feature_spawns(json_config)
    draw_feature_despawns(json_config)
    draw_terrain_changes(json_config)
    draw_plot_changes(json_config)
    draw_region_based_resource_spawns(json_config)
    draw_start_resources(json_config)








