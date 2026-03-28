from python.consts import *  # all relevant game data
from python.DrawMaps.DrawStabAndReligon import *
from python.DrawMaps.DrawSpawn import *
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

### Draw Birth Maps, extended Birth and Respawn too ### 
    for iCiv in dCivNames:
        if iCiv in dBirthArea:
            draw_birth_map(iCiv, dBirthArea, dBirthAreaExceptions, "maps/layers/Spawns")
        else:
            draw_birth_map(iCiv, dCoreArea, dCoreAreaExceptions, "maps/layers/Spawns")
        
        for iPeriod in dCivPeriods.get(iCiv, []):
            if should_draw_for_period(iPeriod):
                draw_birth_map(iCiv, iPeriod)

        if iCiv in dExtendedBirthArea:
            draw_birth_map(iCiv, dExtendedBirthArea, dExtendedBirthAreaExceptions, "maps/layers/Spawns/Extended")

        if iCiv in dRespawnArea:
            draw_birth_map(iCiv, dRespawnArea, dRespawnAreaExceptions, "maps/layers/Spawns/Respawns")
            

### Draw Resource Map ###
 
### Draw UHV Maps ###


### Draw Geography ###
# Regions
# Peak changes

### Draw general Resource Map ###


