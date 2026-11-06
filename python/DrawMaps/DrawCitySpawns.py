from python.consts import *
from python.helper.helper import *
import config

from PIL import Image
from pathlib import Path



def drawCityspawn(city, json_config):
    # args
    spawn_year, iCiv, location, City_name = city.get("args")
    # kwargs
    iPopulation = city.get("kwargs").get("iPopulation", 1)
    iUnits = sum([v for k,v in city.get("kwargs").get("units", {}).items()]) 
    conditional = "(conditional!)" if city.get("kwargs").get("condition", False) == None else ""
    civ_name = LCivXML[iCiv].get("ShortDescription")
    
    text = f"{spawn_year}{conditional} \n {City_name} \n {iPopulation} pop, {iUnits} unit(s)"
    
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
    
    