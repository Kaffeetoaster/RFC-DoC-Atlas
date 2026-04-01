from multiprocessing import spawn

from python.consts import *
from python.load_resources import *

import config

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json


def create_tile_overlay(coordinates, text, button, spawn):

    img = Image.new('RGBA', (52, 52), (0, 0, 0, 0))
    # Draw the button image onto the tile
    button_img = Image.open(button)
    button_img = button_img.resize((32, 32), Image.LANCZOS)
    img.paste(button_img, (10, 10), button_img)
    # Create a drawing object
    draw = ImageDraw.Draw(img)



    # # Get text size
    bbox = draw.textbbox((0, 0), text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center at point (cx, cy)
    cx, cy = 26, 40
    x = cx - text_width // 2
    ## y = cy - text_height // 2
    x = 10
    y = 40
    for dx in (0,1):
        for dy in (0,1):
            draw.text((x+dx, y+dy), text,fill= "green" if spawn else "red")
    return coordinates, img

### load xml resource infos and convert images to png for web usage
dResourceInfos = extract_all_resource_infos()
#print(dResourceInfos)
convert_resource_images(dResourceInfos)


# generate whole resource spawn layer (deprecated)
# resource_spawn_layer = Image.new('RGBA', (7800,4160 ), (0, 0, 0, 0))
# for coords, event in dResourcesDict.items():
#     (x,y),img = create_tile_overlay(coords, str(event[0]),dResourceInfos[event[1]]["path_art"], True)
#     resource_spawn_layer.paste(img, (x * 52,(iWorldY-1-y)* 52), img)
#     #print(f"Spawned {event[1]} at {coords}")
# resource_spawn_layer.save(config.OUTPUT_PATH / "maps/layers/Resources/resource_spawns_and_despawns.png")


def add_resource_config_entry(config_dict, coords, text, path_art, category, bSpawn):
    entry = {
        "x": coords[0],
        "y": coords[1],
        "display_name": text,
        "source": str(path_art),
        "category": category,
        "spawn": bSpawn # important for color
    }
    if bSpawn:
        config_dict["resource_spawns"].append(entry)
    elif not bSpawn:
        config_dict["resource_despawns"].append(entry)

### generate tooltip infos and json entries for resource spawn ###
markers_config ={
    "resource_spawns": [],
    "resource_despawns": []
}

for coords, event in dResourcesDict.items():
    iresource = event[1]
    year = str(event[0])
    resource_info = dResourceInfos[iresource]
    path_art = resource_info["path_art"]
    old_img = Image.open(path_art)
    if old_img.size == (64,64):
        img = old_img.crop((3,3,60,60))
        img.save(path_art)
    add_resource_config_entry(markers_config, coords, year, Path(path_art).relative_to(config.OUTPUT_PATH), category = "Resource spawns", bSpawn=True)
    


for coords, event in dRemovedResourcesDict.items():
    year = str(event)
    path_art = "resources/Deletion.png"
    old_img = Image.open(path_art)
    if old_img.size == (64,64):
        img = old_img.crop((3,3,60,60))
        img.save(path_art)
    add_resource_config_entry(markers_config, coords, year, Path(path_art), category = "Resource despawns", bSpawn=False)




with open("json/tooltips.json", "w") as f:
    json.dump(markers_config, f, indent=2)






