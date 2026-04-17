from python.consts import *
from python.helper.helper import *
from python.helper.DrawOutlines import *
import config




def draw_birth_map(json_config, iCiv, area, exceptions, folder,line_width, iPeriod=None, extendedCore = False, respawn = False):
    add_terrain_exceptions(area, exceptions, dTileMap)
    ## get color from xml and from LCivXML
    color = (round(0), round(0), round(0),round(255))

    color = LCivXML[iCiv]["Color"].get("ColorTypePrimary", color)
    


    name = LCivXML[iCiv].get("ShortDescription")
    if iCiv == 40: # Misir
        name = "Misr"
    if name.startswith("TXT_KEY_CIV_"):
        name = LCivXML[iCiv].get("Description")
    if name.startswith("The Germans"):
        name = "Holy Rome"
    elif name.startswith("The Khmer"):
        name = "Khmer"
    elif name.startswith("The Dutch"):
        name = "Netherlands"
    
    filename = name.replace(" ", "_")
    category = "Birth"
    if iPeriod is not None:
        filename = f"{name}_{dPeriodNames.get(iPeriod, '')}".replace(" ", "_")
        name = f"{name.replace('_', ' ')} -> {dPeriodNames.get(iPeriod, '').replace('_', ' ')}"
    elif extendedCore:
        name = f"{name} extended (AI only)"
    elif respawn:
        name = f"{name} respawn"

    
    img = draw_outlines_for_area(area, exceptions, color, line_width)
    image_path = config.OUTPUT_PATH / folder / f"{filename}.png"
    img.save(image_path)

    add_layer_config_entry(config = json_config, 
                           text = name, 
                           category = category, 
                           image_path = Path(image_path).relative_to(config.OUTPUT_PATH), 
                           image_size = img.size, 
                           offset = (area[0][0],area[0][1]))
                            #offset = (area[0][0],iWorldY-1-area[0][1]))


def DrawBirthMaps(layers_config):
    for iCiv in range(iNumCivs):
        if iCiv in dBirthArea:
            draw_birth_map(layers_config, iCiv, dBirthArea[iCiv], dBirthAreaExceptions.get(iCiv, []), "maps/layers/Spawns", line_width=3)
        else:
            if iCiv in dCoreArea:
                draw_birth_map(layers_config, iCiv, dCoreArea[iCiv], dCoreAreaExceptions.get(iCiv, []), "maps/layers/Spawns", line_width=3)
        for iPeriod in dCivPeriods.get(iCiv, []):
            if iPeriod in dPeriodCoreArea:
                draw_birth_map(layers_config, iCiv, dPeriodCoreArea[iPeriod], dPeriodCoreAreaExceptions.get(iPeriod, []), "maps/layers/Spawns/Periods", 3,iPeriod)
            
        if iCiv in dExtendedBirthArea:
            draw_birth_map(layers_config, iCiv, dExtendedBirthArea[iCiv], dExtendedBirthAreaExceptions.get(iCiv, []), "maps/layers/Spawns/Extended", line_width=5,extendedCore=True)
        if iCiv in dRespawnArea:
            draw_birth_map(layers_config, iCiv, dRespawnArea[iCiv], dRespawnAreaExceptions.get(iCiv, []), "maps/layers/Spawns/Respawns", line_width=7, respawn=True)

