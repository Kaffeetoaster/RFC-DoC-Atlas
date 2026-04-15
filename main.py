from python.consts import *  # all relevant game data

from python.DrawMaps.DrawReligionMap import *
from python.DrawMaps.DrawMarkers import *
from python.DrawMaps.DrawStabilityMaps import *
from python.DrawMaps.DrawBirthMap import *
import config

import json

input_path = config.INPUT_PATH
output_path = config.OUTPUT_PATH

### Entry Point for the map creating Process ###



if __name__ == "__main__":
    layers_config = {
        "layers": []
    }
### generate tooltip infos and json entries for resource spawn ###
    markers_config ={
        "spawns_and_despawns": []  
    }
# ### Draw Stab Maps ###
#     for iCiv in dCivNames:
#         draw_stability_map_for_civ(iCiv)
        
#         for iPeriod in dCivPeriods.get(iCiv, []):
#             if should_draw_for_period(iPeriod):
#                 draw_stability_map_for_period(iCiv, iPeriod)
### Draw Religion Maps ###
    # for iReligion in range(iNumReligions):
    #     draw_religion_map(iReligion, layers_config)

### Draw Birth Maps, extended Birth and Respawn too ### 
    for iCiv in range(iNumCivs):
        if iCiv in dBirthArea:
            draw_birth_map(layers_config, iCiv, dBirthArea[iCiv], dBirthAreaExceptions.get(iCiv, []), "temp/maps/layers/Spawns", line_width=3)
        else:
            if iCiv in dCoreArea:
                draw_birth_map(layers_config, iCiv, dCoreArea[iCiv], dCoreAreaExceptions.get(iCiv, []), "temp/maps/layers/Spawns", line_width=3)

        if iCiv in dExtendedBirthArea:
            draw_birth_map(layers_config, iCiv, dExtendedBirthArea[iCiv], dExtendedBirthAreaExceptions.get(iCiv, []), "temp/maps/layers/Spawns/Extended", line_width=5)
        if iCiv in dRespawnArea:
            draw_birth_map(layers_config, iCiv, dRespawnArea[iCiv], dRespawnAreaExceptions.get(iCiv, []), "temp/maps/layers/Spawns/Respawns", line_width=7)



    ### Draw Resource and Feature and Terrain Maps ###
    draw_tile_markers(markers_config)

    ### Draw UHV Maps ###


    ### Draw Geography ###
    # Regions




    with open("json/layers_config.json", "w") as f:           
        json.dump(layers_config, f, indent = 2)
        
    with open("json/tooltips.json", "w") as f:
        json.dump(markers_config, f, indent=2)






