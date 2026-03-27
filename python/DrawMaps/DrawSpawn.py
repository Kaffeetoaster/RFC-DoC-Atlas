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


def draw_extended_birth_map(iCiv):

    if iCiv not in dExtendedBirthArea:
        return
    terrain_values = iterate_map("Export/BaseTerrain.csv")
    name = dCivNames.get(iCiv)
    print(name)
    name_display = f"{name} extended"
    print(f"""        <label class="option"><input type="checkbox" data-target="spawn_extended_{name}">{name_display}</label>""")
    print(f"""   <img id="spawn_extended_{name}" src="maps/layers/Spawns/Extended/{name}.png" class="overlay">""")
	    
    image = Image.new("RGBA", (iWorldX, iWorldY), (0, 0, 0, 0))
    pixels = image.load()

    for (x, y), iTerrainValue in terrain_values:
        if iTerrainValue != 0 and is_area(dExtendedBirthArea, dExtendedBirthAreaExceptions, iCiv, (x, iWorldY-1-y)):
                pixels[x,y] = plot_colors[CORE]

    image = image.resize((iWorldX * 52, iWorldY * 52), resample=Image.Resampling.NEAREST)
	
    image_path = config.OUTPUT_PATH / "maps/layers/Spawns/Extended" / f"{name}.png"
    #print(image_path)
    image.save(image_path)

def draw_birth_map(iCiv):

    if iCiv not in dBirthArea:
        return
    terrain_values = iterate_map("Export/BaseTerrain.csv")
    name = dCivNames.get(iCiv)
    print(name)
    name_display = f"{name}"
    print(f"""        <label class="option"><input type="checkbox" data-target="spawn_{name}">{name_display}</label>""")
    print(f"""   <img id="spawn_{name}" src="maps/layers/Spawns/{name}.png" class="overlay">""")
	    
    image = Image.new("RGBA", (iWorldX, iWorldY), (0, 0, 0, 0))
    pixels = image.load()

    for (x, y), iTerrainValue in terrain_values:
        if iTerrainValue != 0 and is_area(dBirthArea, dBirthAreaExceptions, iCiv, (x, iWorldY-1-y)):
                pixels[x,y] = plot_colors[CORE]

    image = image.resize((iWorldX * 52, iWorldY * 52), resample=Image.Resampling.NEAREST)
	
    image_path = config.OUTPUT_PATH / "maps/layers/Spawns" / f"{name}.png"
    #print(image_path)
    image.save(image_path)

def draw_respawn_map(iCiv):

    if iCiv not in dRespawnArea:
        return

    terrain_values = iterate_map("Export/BaseTerrain.csv")
    name = dCivNames.get(iCiv)
    print(name)
    name_display = f"{name} respawn"
    #print(f"""        <label class="option"><input type="checkbox" data-target="respawn_{name}">{name_display}</label>""")
    #print(f"""   <img id="respawn_{name}" src="maps/layers/Spawns/Respawns/{name}.png" class="overlay">""")
	    
    image = Image.new("RGBA", (iWorldX, iWorldY), (0, 0, 0, 0))
    pixels = image.load()

    for (x, y), iTerrainValue in terrain_values:
        if iTerrainValue != 0 and is_area(dRespawnArea, dRespawnAreaExceptions, iCiv, (x, iWorldY-1-y)):
                pixels[x,y] = plot_colors[CORE]

    image = image.resize((iWorldX * 52, iWorldY * 52), resample=Image.Resampling.NEAREST)
	
    image_path = config.OUTPUT_PATH / "maps/layers/Spawns/Respawns" / f"{name}.png"
    #print(image_path)
    image.save(image_path)

