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

from python.helper.helper import *
import config
import json




input_path = config.INPUT_PATH
output_path = config.OUTPUT_PATH

### Entry Point for the map creating Process ###



if __name__ == "__main__":
### json config file for map layers ###
    layers_config = {
        "Grid": [],
        "Stability": [],
        "Birth": [],
        "Religion": []
    }
### json config file for map markers ###
    markers_config ={
        "spawns_and_despawns": []  
    }
    create_tile_outline(
        image_width=7800,
        image_height=4160,
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

### Draw UHV Maps ###
    measure(DrawUHVMaps, layers_config)

### Draw Geography ###
    measure(DrawGeographyMaps, layers_config)
    




    with open("json/layers.json", "w") as f:           
        json.dump(layers_config, f, indent = 2)
        
    with open("json/tooltips.json", "w") as f:
        json.dump(markers_config, f, indent=2)






