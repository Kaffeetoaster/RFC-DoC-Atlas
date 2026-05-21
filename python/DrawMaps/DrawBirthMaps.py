from python.consts import *
from python.helper.helper import *
from python.helper.DrawHelper import *
import config




def draw_birth_map(json_config, iCiv, area, exceptions, folder,line_width, iPeriod=None, extendedCore = False, respawn = False):
    
    add_terrain_exceptions(area, exceptions, dTileMap)
    ## get color from xml and from LCivXML
    color = (round(0), round(0), round(0),round(255))

    color = LCivXML[iCiv]["Color"].get("ColorTypePrimary", color)
    
    name = LCivXML[iCiv].get("ShortDescription")
    if iCiv == 41: # Misir
        name = "Misr"
    if iCiv == 57: # Saudis
        name = "Saudi Arabia"
    if name.startswith("TXT_KEY_CIV_"):
        name = LCivXML[iCiv].get("Description")
    if name.startswith("The Germans"):
        name = "Holy Rome"
    elif name.startswith("The Khmer"):
        name = "Khmer"
    elif name.startswith("The Dutch"):
        name = "Netherlands"
    
    filename = name.replace(" ", "_")
    category = "Birth and Stability"
    Capital_x, Capital_y = dCapitals.get(iCiv, (None, None))
    if iPeriod is not None:
        filename = f"{name}_{dPeriodNames.get(iPeriod, '')}".replace(" ", "_")
        name = f"{name.replace('_', ' ')} -> {dPeriodNames.get(iPeriod, '').replace('_', ' ')}"
        Capital_x, Capital_y = dPeriodCapitals.get(iPeriod, (Capital_x, Capital_y))
    elif extendedCore:
        name = f"{name} extended (AI only)"
    elif respawn:
        name = f"{name} respawn"
        Capital_x, Capital_y = dRespawnCapitals.get(iCiv, (Capital_x, Capital_y))
    
    print(f"Drawing birth map for {name}... ")




    # draw fill in and outlines
    img = Image.new("RGBA", (iWorldX * TILE_SIZE, iWorldY * TILE_SIZE), (0, 0, 0, 0))

    area= transform_area_coordinates(area)
    exceptions = [transform_coordinates(coor) for coor in exceptions]
    Capital_x, Capital_y = transform_coordinates((Capital_x, Capital_y))

    # draw hatching, Capital location and outline
    draw_fill_in_area(area, exceptions, color, img, Hatching=True)
    fill_in_tile(Capital_x, Capital_y, color, img, Hatching=False)
    draw_outlines_for_area(area, exceptions, color, line_width, img)
    
    
    
    img, offset = crop_image_to_content(img)  # Crop to content
    offset = (offset[0] // TILE_SIZE, offset[1] // TILE_SIZE)

    image_path = config.OUTPUT_PATH / folder / f"{filename}.webp"
    img.save(image_path)

    add_layer_config_entry(config = json_config, 
                           text = name, 
                           category = category, 
                           image_path = Path(image_path).relative_to(config.OUTPUT_PATH), 
                           image_size = img.size, 
                           offset = offset
                           )


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

