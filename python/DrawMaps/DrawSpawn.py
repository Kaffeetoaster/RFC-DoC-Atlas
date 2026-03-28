from python.consts import *
import config


import os
import csv

from PIL import Image
from pathlib import Path

def get_full_path(path):
	return config.INPUT_PATH / "Assets/Maps" / path


def map_exists(file_path):
	try:
		open(get_full_path(file_path))
	except IOError:
		return False
	
	return True

def is_area(rectangle, exceptions, identifier, tile):
	x, y = tile
	
	(x1, y1), (x2, y2) = rectangle[identifier]
	excluded = exceptions.get(identifier, [])
	
	return x1 <= x <= x2 and y1 <= y <= y2 and (x, y) not in excluded

def iterate_map(file_path):
	full_file_path = get_full_path(file_path)
	
	with open(full_file_path) as file:
		for y, line in enumerate(csv.reader(file)):
			for x, value in enumerate(line):
				if not value:
					yield (x, y), 0
				else:
					yield (x, y), int(value)




def draw_birth_map(iCiv, area, exceptions, folder):

    terrain_values = iterate_map("Export/BaseTerrain.csv")
    name = dCivNames.get(iCiv)
    print(name)
    if area == dBirthArea or area == dCoreArea:
        name_display = f"{name}"
        id = "spawn"
    elif area == dExtendedBirthArea:
        name_display = f"{name} extended"
        id = "spawn_extended"
    elif area == dRespawnArea:
        name_display = f"{name} respawn"
        id = "respawn"
		

    print(f"""        <label class="option"><input type="checkbox" data-target="{id}_{name}">{name_display}</label>""")
    print(f"""   <img id="{id}_{name}" src="{folder}/{name}.png" class="overlay">""")
	    
    image = Image.new("RGBA", (iWorldX, iWorldY), (0, 0, 0, 0))
    pixels = image.load()

    for (x, y), iTerrainValue in terrain_values:
        if iTerrainValue != 0 and is_area(area, exceptions, iCiv, (x, iWorldY-1-y)):
                pixels[x,y] = plot_colors[CORE]

    image = image.resize((iWorldX * 52, iWorldY * 52), resample=Image.Resampling.NEAREST)
	
    image_path = config.OUTPUT_PATH / folder / f"{name}.png"
    #print(image_path)
    image.save(image_path)

