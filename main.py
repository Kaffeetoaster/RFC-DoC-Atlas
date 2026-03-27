from python.consts import *  # all relevant game data
from python.DrawMaps.DrawStabAndReligon import *
import config


input_path = config.INPUT_PATH
output_path = config.OUTPUT_PATH

### Entry Point for the map creating Process ###



if __name__ == "__main__":
    
### Draw Stab Maps ###
    for iCiv in dCivNames:
        draw_stability_map_for_civ(iCiv)
        
        for iPeriod in dCivPeriods.get(iCiv, []):
            if should_draw_for_period(iPeriod):
                draw_stability_map_for_period(iCiv, iPeriod)
### Draw Religion Maps ###
    for iReligion in range(iNumReligions):
        draw_religion_map(iReligion)

### Draw Spawn Maps ### 
    for iCiv in dCivNames:
        draw_birth_map(iCiv)
        draw_respawn_map(iCiv)
        

### Draw Resource Spawn Map ###
 
### Draw UHV Maps ###

### Draw Geography ###
# Regions
# Peak changes

### Draw general Resource Map ###


