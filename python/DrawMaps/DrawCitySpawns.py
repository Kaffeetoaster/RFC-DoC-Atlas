from python.consts import *
from python.helper.helper import *
import config

from PIL import Image
from pathlib import Path



def drawCityspawn(city, json_config):

    spawn_year = str(city.get("args")[0])
    location = city.get("args")[2]
    City_name = city.get("args")[3]
    text = f"{spawn_year} - {City_name}"
    
    path_art = config.INPUT_PATH.parent.parent.parent.parent/ "Art Assets/Art/Interface/Buttons/Actions/Foundcity.dds"
    old_img = Image.open(path_art)
    new_path = config.OUTPUT_PATH / "Assets/Art/Interface/Buttons/" / f"{Path(path_art).stem}_cropped.png"
    if old_img.size == (64,64):
        img = old_img.crop((3,3,60,60))
        img.save(new_path)
    
    add_marker_config_entry(json_config, location, text, Path(new_path).relative_to(config.OUTPUT_PATH), "City spawns", True)







def drawCitySpawns(json_config):
    for city in minor_cities:
        drawCityspawn(city, json_config)
    
    