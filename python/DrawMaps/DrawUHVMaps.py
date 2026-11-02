from fileinput import filename

from python.consts import *
from python.helper.helper import *
from python.helper.DrawHelper import *
import config

lLocations = [
    {"DisplayText": "American Congress Claims", 
     "Area": tAmericanClaims, 
     "Exceptions": lAmericanClaimsExceptions, 
     "Civ": iAmerica},
    
    {"DisplayText": "Newfoundland (Congress)", 
     "Area": tNewfoundland, 
     "Exceptions": [], 
     "Civ": iCanada},
    
    # probably doesnt make sense to remove the terrain execptions here, hm.
    {"DisplayText": "Mesoamerican Contact Zone", "Area": tMesoamericanContactZone, "Exceptions": lContactZoneExceptions, "Civ": -1, "ignore_terrain_exceptions": True},
    {"DisplayText": "Andean Contact Zone", "Area": tAndeanContactZone, "Exceptions": lContactZoneExceptions, "Civ": -1, "ignore_terrain_exceptions": True},
    
    # are lists instead of area tuples, maybe write a function that converts this list to an area and (alot of) exceptions
    {"DisplayText": "Macedonian Road", "Area": convert_list_to_area_and_exceptions(lMacedonianRoad)[0], "Exceptions": convert_list_to_area_and_exceptions(lMacedonianRoad)[1], "Civ": -1},
    {"DisplayText": "Silk Route", "Area": convert_list_to_area_and_exceptions(lSilkRoute)[0], "Exceptions": convert_list_to_area_and_exceptions(lSilkRoute)[1], "Civ": -1},
    {"DisplayText": "Kushan Road", "Area": convert_list_to_area_and_exceptions(lKushanRoad)[0], "Exceptions": convert_list_to_area_and_exceptions(lKushanRoad)[1], "Civ": -1},
    {"DisplayText": "Hejaz Road", "Area": convert_list_to_area_and_exceptions(lHejazRoad)[0], "Exceptions": convert_list_to_area_and_exceptions(lHejazRoad)[1], "Civ": -1},
    
    {"DisplayText": "Phoenician Italy", "Area": tPhoenicianItaly, "Exceptions": lPhoenicianItalyExceptions, "Civ": iPhoenicia},
    {"DisplayText": "Hawaii for Polynesia", "Area": tHawaii, "Exceptions": [], "Civ": iPolynesia},
    {"DisplayText": "New Zealand east for Polynesia", "Area": tNewZealandEast, "Exceptions": [], "Civ": iPolynesia},
    {"DisplayText": "New Zealand west for Polynesia", "Area": tNewZealandWest, "Exceptions": [], "Civ": iPolynesia},
    {"DisplayText": "Marquesas for Polynesia", "Area": tMarquesas, "Exceptions": [], "Civ": iPolynesia},
    {"DisplayText": "Easter Island for Polynesia", "Area": tEasterIsland, "Exceptions": [], "Civ": iPolynesia},
    {"DisplayText": "Srivijaya for Tamils", "Area": tSrivijaya, "Exceptions": [], "Civ": iTamils},
    {"DisplayText": "Andalusia for Byzantine", "Area": tAndalusia, "Exceptions": [], "Civ": iByzantium},
    {"DisplayText": "Malaya for Malays", "Area": tMalaya, "Exceptions": [], "Civ": iMalays},
    {"DisplayText": "West Africa for Moors", "Area": tWestAfrica, "Exceptions": [], "Civ": iMoors},
    {"DisplayText": "Nile for Misr", "Area": tNile, "Exceptions": lNileExceptions, "Civ": iMisr},
    {"DisplayText": "Sudan for Misr", "Area": tSudan, "Exceptions": lSudanExceptions, "Civ": iMisr},
    {"DisplayText": "Dzungaria for Manchuria", "Area": tDzungaria, "Exceptions": lDzungariaExceptions, "Civ": iManchuria},
    {"DisplayText": "Scandinavia for Germany", "Area": tScandinavia, "Exceptions": lScandinaviaExceptions, "Civ": iGermany},
    {"DisplayText": "Canada", "Area": ((iCanadaWesternBorder, iCanadaSouthernBorder), (iCanadaEasternBorder, 79)), "Exceptions": [], "Civ": iCanada}
]




def DrawUHVMaps(json_config):
    for location in lLocations:
        area = location.get("Area")
        exceptions = location.get("Exceptions")
        
        if not location.get("ignore_terrain_exceptions", False):
            add_terrain_exceptions(area, exceptions, dTileMap)
        display_text = location.get("DisplayText")
        iCiv = location.get("Civ")

        color = (0, 0, 0, 255)  # Black with full opacity
        if iCiv != -1:
            color = LCivXML[iCiv]["Color"].get("ColorTypePrimary", color)
        line_width = 5
        category = "Locations"  
           
        img = Image.new("RGBA", (int(iWorldX * TILE_SIZE), int(iWorldY * TILE_SIZE)), (0, 0, 0, 0))
        # transform coordinates
        area= transform_area_coordinates(area)
        exceptions = [transform_coordinates(coor) for coor in exceptions]
        
        # draw hatching, and outline
        draw_fill_in_area(area, exceptions, color, img, Hatching=True)
        draw_outlines_for_area(area, exceptions, color, line_width, img)
        
        img, offset = crop_image_to_content(img)  # Crop to content
        offset = (offset[0] // TILE_SIZE, offset[1] // TILE_SIZE)

        filename = f"maps/layers/Locations/{display_text.replace(" ", "_")}"
        image_path = config.OUTPUT_PATH / f"{filename}.webp"
        img.save(image_path)

        add_layer_config_entry(config = json_config, 
                            text = display_text, 
                            category = category, 
                            image_path = Path(image_path).relative_to(config.OUTPUT_PATH), 
                            image_size = img.size, 
                            offset = offset
                            )





