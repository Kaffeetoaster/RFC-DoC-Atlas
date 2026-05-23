from python.consts import *

import time


def transform_coordinates(coor, new_width = iWorldX, new_height = iWorldY, offset = (0,0)):
    # assumes coordinates in (x,y) format with (0,0) at bottom left
    # and with Map Width and Height of iWorldX and iWorldY, which are 150 and 80 base values
    # transforms to smaller map with new_Width and new_Height
    x, y = coor
    return (x + offset[0], new_height - 1 - y - offset[1])

def transform_area_coordinates(area, new_width = iWorldX, new_height = iWorldY, offset = (0,0)):
    (x_min,y_min), (x_max, y_max) = area
    TL_transformed = transform_coordinates((x_min, y_min), new_width, new_height, offset)
    BR_transformed = transform_coordinates((x_max, y_max), new_width, new_height, offset)
    return ((TL_transformed[0],TL_transformed[1]-(y_max-y_min)),(BR_transformed[0],BR_transformed[1]+(y_max-y_min)))

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
    config[category].append(entry)


def add_marker_config_entry(config_dict, coords, text, path_art, category, bSpawn, bonusType = None):
    entry = {
        "x": coords[0],
        "y": coords[1],
        "text": text,
        "source": str(path_art),
        "category": category,
        "spawn": bSpawn, # important for color
        "bonusType": bonusType
    }
    config_dict["spawns_and_despawns"].append(entry)


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
    print(f"Starting {func.__name__}... ")
    func(*args, **kwargs)
    end = time.perf_counter()
    duration = end - start
    print(f"Finished {func.__name__} in {duration:.6f}s ")

    with open("time.log", "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {func.__name__} | {duration:.6f}s\n")

    return duration

def start_new_log(name):
    with open("time.log", "a", encoding="utf-8") as f:
        f.write("="*50 + "\n")
        f.write(f"New log started at {time.strftime('%Y-%m-%d %H:%M:%S')} for {name}\n")




def crop_image_to_content(image):
    # Get bounding box of non-transparent pixels
    bbox = image.getbbox()
    w,h = image.size
    offset = (bbox[0], h-bbox[3]) if bbox else (0, 0)
    if bbox:
        return image.crop(bbox), offset
    else:
        return image, offset  # Return original if no content found

