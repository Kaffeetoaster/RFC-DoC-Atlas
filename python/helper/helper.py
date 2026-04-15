
import time

from PIL import Image, ImageFilter

from python.consts import *

def transform_coordinates(coor, new_width = iWorldX, new_height = iWorldY, offset = (0,0)):
    # assumes coordinates in (x,y) format with (0,0) at bottom left
    # and with Map Width and Height of iWorldX and iWorldY, which are 150 and 80 base values
    # transforms to smaller map with new_Width and new_Height
    x, y = coor
    return (x + offset[0], new_height - 1 - y - offset[1])

def add_layer_config_entry(config, text, category, image_path, image_size, offset = (0,0)):
    entry = {
        "x": offset[0], # offset if needed
        "y": offset[1],
        "display_name": text,
        "source": str(image_path),
        "w": image_size[0],
        "h": image_size[1],
        "category": category,
    }
    config["layers"].append(entry)

def is_in_area(rectangle, exceptions, tile):
    x, y = tile
    exceptions = set(exceptions)
    (x1, y1), (x2, y2) = rectangle
    return x1 <= x <= x2 and y1 <= y <= y2 and (x, y) not in exceptions



def add_terrain_exceptions(tArea, LExceptions, dTileMap):
    
    (x1, y1), (x2, y2) = tArea
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if dTileMap[transform_coordinates((x, y))]["plot"] == "PLOT_OCEAN":
                LExceptions.append((x, y))
    

def measure(func,*args, **kwargs):
    start = time.perf_counter()
    func(*args, **kwargs)
    end = time.perf_counter()
    #print(f"{func.__name__}: {end - start:.6f}s")
    return end - start
