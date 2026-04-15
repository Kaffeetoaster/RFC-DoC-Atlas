from python.consts import *
from python.helper.helper import *
from python.helper.DrawOutlines import *
import config




def draw_birth_map(json_config, iCiv, area, exceptions, folder,line_width, iPeriod=None):
    add_terrain_exceptions(area, exceptions, dTileMap)
    ## get color from xml and from LCivXML
    color = (round(255), round(255), round(255),round(255))
    name = LCivXML[iCiv].get("ShortDescription")
    if name.startswith("TXT_KEY_CIV_"):
        name = LCivXML[iCiv].get("Description")
    if name.startswith("The Germans"):
        name = "Holy Rome"
    elif name.startswith("The Khmer"):
        name = "Khmer"
    elif name.startswith("The Dutch"):
        name = "Netherlands"
        
    category = "Stability and Birth"
    if iPeriod is not None:
        subcategory = f"{name.replace('_', ' ')} - {dPeriodNames.get(iPeriod, '').replace('_', ' ')}"
        name = f"{name}_{dPeriodNames.get(iPeriod, '')}"

    subcategory = name.replace('_', ' ')
    filename = name
    
    img = draw_outlines_for_area(area, exceptions, color, line_width)
    image_path = config.OUTPUT_PATH / folder / f"{filename}.png"
    img.save(image_path)

    add_layer_config_entry(config = json_config, 
                           text = name, 
                           category = category, 
                           image_path = Path(image_path).relative_to(config.OUTPUT_PATH), 
                           image_size = img.size, 
                           offset = (area[0][0],iWorldY-1-area[0][1]))




