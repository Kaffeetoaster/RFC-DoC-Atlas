from python.consts import *
from python.helper.helper import *

from python.helper.DrawHelper import *
import config

from PIL import Image
from pathlib import Path


def drawBarbarianSpawn(BarbarianSpawn, json_config, spawn_id):
    
    start_year, end_year, units, spawn_area, interval, pattern = BarbarianSpawn.get("args")
    iOwner = BarbarianSpawn.get("kwargs").get("iOwner", iBarbarian)
    target_Area = BarbarianSpawn.get("kwargs").get("target_area", None)
    promotions = BarbarianSpawn.get("kwargs").get("promotions", None)
    conditional = "(conditional!)" if BarbarianSpawn.get("kwargs").get("condition", False) == None else ""
    
    
    
    # color = BarbarianSpawn.get("color", (0, 0, 0, 200))  # Black 
    if iOwner != -1:
        color = LCivXML[iOwner]["Color"].get("ColorTypePrimary", (0, 0, 0, 200))  # Default to black if not found
    line_width = 5
        
    img = Image.new("RGBA", (int(iWorldX * TILE_SIZE), int(iWorldY * TILE_SIZE)), (0, 0, 0, 0))
    # transform coordinates
    area= transform_area_coordinates(spawn_area)
    
    exceptions = []
    # draw hatching, and outline
    draw_fill_in_area(area, exceptions, color, img, Hatching=True)
    color_outline = (color[0], color[1], color[2], 255)  # Full opacity for outline
    draw_outlines_for_area(area, exceptions, color_outline, line_width, img)
    
    layer_img, offset = crop_image_to_content(img)  # Crop to content
    offset = (offset[0] // TILE_SIZE, offset[1] // TILE_SIZE)

    filename = f"maps/layers/Barbarians/{start_year}_{end_year}_{'_'.join([str(x) for x in spawn_area])}_{interval}_{pattern}"
    image_path = config.OUTPUT_PATH / f"{filename}.webp"
    layer_img.save(image_path)
    
    
    # marker img
    marker_path = ""

    unit_text = ", ".join([f"{v}x {LUnitXML[k]['Description']}" for k,v in units.items()])
    promotion_text = ""
    if promotions:
        promotion_text = "\n with "
        promotion_text += ", ".join([f"{LPromotionXML[k]['Description']}" for k in promotions])

    marker_text = f"{start_year} to {end_year}{conditional}\n{unit_text}{promotion_text}\n with Interval: {interval}"
    marker_location = calculate_center_of_area(spawn_area)
    
    
    add_layer_to_MapObject_config(config_list = json_config,
                        category = "Barbarian spawns and City spawns",
                        subcategory = "Barbarian Spawns",
                        time_frame = (start_year, end_year),
                        image_path = Path(image_path).relative_to(config.OUTPUT_PATH),
                        image_size = layer_img.size,
                        offset = offset,
                        id = spawn_id
                        )
    add_marker_to_MapObject_config(config_list = json_config,
                        coords = marker_location,
                        text = marker_text,             
                        path_art = marker_path,
                        category = "Barbarian spawns and City spawns",
                        subcategory = "Barbarian Spawns",
                        time_frame = (start_year, end_year),
                        bSpawn = True,
                        id = spawn_id
                        )


def drawBarbarianSpawns(json_config):
    for i,BarbarianSpawn in enumerate(barbarians):
        drawBarbarianSpawn(BarbarianSpawn,json_config, spawn_id = f"barbarian_spawn_{i}")