from fileinput import filename

from python.consts import *
from python.helper.helper import *
from python.helper.DrawHelper import *
import config


lAreas = [
    tPhoenicianItaly,
    tHawaii, 
    tNewZealandEast, 
    tNewZealandWest,
    tMarquesas, 
    tEasterIsland,
    tSrivijaya,
    tAndalusia,
    tMalaya,
    tWestAfrica,
    tNile,
    tSudan,
    tDzungaria,
    tScandinavia,
    ((iCanadaWesternBorder, iCanadaSouthernBorder), (iCanadaEasternBorder, 79))
    ]
lExeptions = [
    lPhoenicianItalyExceptions,
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    lNileExceptions,
    lSudanExceptions,
    lDzungariaExceptions,
    lScandinaviaExceptions,
    []
    ]
ldisplayText =[
    "Phoenician Italy",
    "Hawaii for Polynesia",
    "New Zealand east for Polynesia",
    "New Zealand west for Polynesia",
    "Marquesas for Polynesia",
    "Easter Island for Polynesia",
    "Srivijaya for Dravidia",
    "Andalusia for Byzantine",
    "third Malay goal",
    "West Africa for Moors",
    "Nile for Misr",
    "Sudan for Misr",
    "Dzungaria for Manchuria",
    "Scandinavia for Germany",
    "Canada"
    ]
lCiv = [
    iPhoenicia,
    iPolynesia,
    iPolynesia,
    iPolynesia,
    iPolynesia,
    iPolynesia,
    iDravidia,
    iByzantium,
    iMalays,
    iMoors,
    iMisr,
    iMisr,
    iManchuria,
    iGermany,
    iCanada
    ]



def DrawUHVMaps(json_config):
    for i, area in enumerate(lAreas):
        exceptions = lExeptions[i]
        add_terrain_exceptions(area, exceptions, dTileMap)
        display_text = ldisplayText[i]
        iCiv = lCiv[i]

        color = (0, 0, 0, 255)  # Black with full opacity
        color = LCivXML[iCiv]["Color"].get("ColorTypePrimary", color)
        line_width = 5
        category = "UHV"  
           
        img = Image.new("RGBA", (iWorldX * TILE_SIZE, iWorldY * TILE_SIZE), (0, 0, 0, 0))
        # transform coordinates
        area= transform_area_coordinates(area)
        exceptions = [transform_coordinates(coor) for coor in exceptions]
        
        # draw hatching, and outline
        draw_fill_in_area(area, exceptions, color, img, Hatching=True)
        draw_outlines_for_area(area, exceptions, color, line_width, img)
        
        img, offset = crop_image_to_content(img)  # Crop to content
        offset = (offset[0] // TILE_SIZE, offset[1] // TILE_SIZE)

        filename = f"maps/layers/UHV/{display_text.replace(" ", "_")}"
        image_path = config.OUTPUT_PATH / f"{filename}.webp"
        img.save(image_path)

        add_layer_config_entry(config = json_config, 
                            text = display_text, 
                            category = category, 
                            image_path = Path(image_path).relative_to(config.OUTPUT_PATH), 
                            image_size = img.size, 
                            offset = offset
                            )





