from python.consts import *  # all relevant game data
from python.helper.helper import *
from python.helper.DrawHelper import *
from python.DrawMaps.DrawBirthMaps import *
from python.DrawMaps.DrawGeograpyhMaps import *
from python.DrawMaps.DrawMarkers import *
from python.DrawMaps.DrawReligionMaps import *
from python.DrawMaps.DrawStabilityMaps import *
from python.DrawMaps.DrawUHVMaps import *
from python.DrawMaps.DrawScenarioCultureMaps import *
from python.DrawMaps.CreateTooltipInfo import *
from python.outline import create_tile_outline
import config
input_path = config.INPUT_PATH
output_path = config.OUTPUT_PATH

### Entry Point for the map creating Process ###
layers_config = {
        "Grid": [],
        "Stability": [],
        "Birth": [],
        "Religion": [],
        "Geography": [],
        "UHV": [],
        "Culture": []
    }
markers_config ={
    "spawns_and_despawns": []  
}


print(LBonusXML[1])
print(LBonusXML[1]["iHappiness"])
draw_start_resources(markers_config)