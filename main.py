import importlib
from python.helper.helper import *
measure(importlib.import_module, "python.consts")
from python.consts import *  # all relevant game data



from python.outline import create_tile_outline
from python.DrawMaps.DrawReligionMaps import *
from python.DrawMaps.DrawMarkers import *
from python.DrawMaps.DrawStabilityMaps import *
from python.DrawMaps.DrawBirthMaps import *
from python.DrawMaps.DrawUHVMaps import *
from python.DrawMaps.DrawGeograpyhMaps import *
from python.DrawMaps.DrawScenarioCultureMaps import *

import config
import json




input_path = config.INPUT_PATH
output_path = config.OUTPUT_PATH

### Entry Point for the map creating Process ###



if __name__ == "__main__":

    start_new_log("Main Process")



### json for about and version info ###
    with open("about/about.json", "r") as f:
        header_info = json.load(f)
    header_info["version"] = f"Mod version: {sModVersion}"
    header_info["last_update"] = f"last Atlas update: {time.strftime('%Y-%m-%d %H:%M')}"
    with open("about/about.json", "w") as f:
        json.dump(header_info, f, indent=2)

### json config file for map layers ###
    layers_config = {
        "Grid": [],
        "Stability and Birth": [],
        "Religion": [],
        "Geography": [],
        "UHV": [],
        "Scenario Culture": []
    }
### json config file for map markers ###
    markers_config ={
        "spawns_and_despawns": []  
    }
    create_tile_outline(
        image_width=4800,
        image_height=2560,
        tiles_x=150,
        tiles_y=80,
        output_path="./maps/tile_outline_cropped.png",
        config = layers_config
    )


### Draw Stab Maps ###
    measure(DrawStabilityMaps, layers_config)

## Draw Religion Maps ###
    measure(DrawReligionMaps, layers_config)

### Draw Birth Maps, extended Birth and Respawn too ### 
    measure(DrawBirthMaps, layers_config)

### Draw Resource and Feature and Terrain Maps ###
    measure(draw_tile_markers, markers_config)

### Draw Geography ###
    measure(DrawGeographyMaps, layers_config)
    
### Draw UHV Maps ###
    measure(DrawUHVMaps, layers_config)

### Draw Scenario Culture Maps ###
    measure(DrawScenarioCultureMaps, layers_config)


### save json config files for layers and markers ###
    with open("json/layers.json", "w") as f:           
        json.dump(layers_config, f, indent = 2)
        
    with open("json/markers.json", "w") as f:
        json.dump(markers_config, f, indent=2)






