from python.consts import *
from python.helper.helper import *

from python.helper.DrawHelper import *
import config

from PIL import Image
from pathlib import Path

# Notes:
# Viel zu viele Überschneidungen.
# es wäre angenehmn und sinnvoll, die Terrain exceptions rauszunehmen,
# aber dafür müsste man die Units nach Typ filtern, den es gibt auch schiffe.

# twl sind die Regionen enorm groß.

# ggf. die Spawns nach Zeit gruppierne und dann mehrere subcategories haben.
# maybe i could only show a marker and on hover the spawn area is shown?
# viell die Angabe von 2 Jahreszahlen erlauben und dann werden alle Spawns in diesem Zeitraum gezeigt?




def preprocess_barbarian_spawns(barbarians):
    processed_spawns = barbarians.copy()
    # merge spawns with the same area
    
    # calculate distinct colors
    # num_colors = 10
    # COLORSCHEME = generate_color_scheme(num_colors)[1]
    # for i, spawn in enumerate(processed_spawns):
    #     r,g,b,_ = COLORSCHEME[i % num_colors]
    #     spawn["color"] = (r, g, b, 130)  # Use RGB from color scheme and set alpha to 130 for transparency
    
    return processed_spawns


def drawBarbarianSpawn(BarbarianSpawn, json_config):
    
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

    unit_count = sum([v for k,v in units.items()])
    marker_text = f"{start_year} to {end_year}{conditional}\n{unit_count} Unit(s) \n with Interval: {interval}"
    marker_location = calculate_center_of_area(spawn_area)
    
    era_borders = [-3000,-1200, -1000, -500, 300, 600, 1000, 1200, 1500, 1700, 1800, 2025]
    eras = [(year, era_borders[i+1]) for i, year in enumerate(era_borders[:-1])]
    subcategories = [f"Unit spawns from {start} to {end}" for start, end in eras if (start <= start_year < end) or (start < end_year <= end) or (start_year <= start and end_year >= end)]
    
    subcategories = ["Barbarian Spawns"]
    for subcategory in subcategories:
        add_layer_to_MapObject_config(config_list = json_config,
                            category = "Barbarian Spawns",
                            subcategory = subcategory,
                            time_frame = (start_year, end_year),
                            image_path = Path(image_path).relative_to(config.OUTPUT_PATH),
                            image_size = layer_img.size,
                            offset = offset
                            )
        add_marker_to_MapObject_config(config_list = json_config,
                            coords = marker_location,
                            text = marker_text,             
                            path_art = marker_path,
                            category = "Barbarian Spawns",
                            subcategory = subcategory,
                            time_frame = (start_year, end_year),
                            bSpawn = True
                            )


def drawBarbarianSpawns(json_config):
    
    for BarbarianSpawn in barbarians:
        # print(f"Drawing Barbarian Spawn: {BarbarianSpawn}")
        drawBarbarianSpawn(BarbarianSpawn, json_config)