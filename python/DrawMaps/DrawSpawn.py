from python.consts import *
import config


import os
import csv

from PIL import Image
from pathlib import Path


def is_area(rectangle, exceptions, identifier, tile):
	x, y = tile
	
	(x1, y1), (x2, y2) = rectangle[identifier]
	excluded = exceptions.get(identifier, [])
	
	return x1 <= x <= x2 and y1 <= y <= y2 and (x, y) not in excluded



def draw_birth_map(iCiv):

    if iCiv not in dRespawnArea:
        return
    
    name = dCivNames.get(iCiv)
    print(name)
    name_display = f"{name}"
    print(f"""        <label class="option"><input type="checkbox" data-target="spawn_{name}">{name_display}</label>""")
    print(f"""   <img id="spawn_{name}" src="maps/layers/Spawns/{name}.png" class="overlay">""")
	    
    image = Image.new("RGBA", (iWorldX, iWorldY), (0, 0, 0, 0))
    pixels = image.load()

    for x in range(iWorldX):
          for y in range(iWorldY):
            if is_area(dRespawnArea, dRespawnAreaExceptions, iCiv, (x, iWorldY-1-y)):
                    pixels[x,y] = plot_colors[CORE]

    image = image.resize((iWorldX * 52, iWorldY * 52), resample=Image.Resampling.NEAREST)
	
    image_path = config.OUTPUT_PATH / "maps/layers/Spawns" / f"{name}.png"
    #print(image_path)
    image.save(image_path)

def draw_respawn_map(iCiv):

    if iCiv not in dRespawnArea:
        return

    name = dCivNames.get(iCiv)
    print(name)
    name_display = f"{name} respawn"
    print(f"""        <label class="option"><input type="checkbox" data-target="respawn_{name}">{name_display}</label>""")
    print(f"""   <img id="respawn_{name}" src="maps/layers/Spawns/Respawns/{name}.png" class="overlay">""")
	    
    image = Image.new("RGBA", (iWorldX, iWorldY), (0, 0, 0, 0))
    pixels = image.load()

    for x in range(iWorldX):
          for y in range(iWorldY):
            if is_area(dRespawnArea, dRespawnAreaExceptions, iCiv, (x, iWorldY-1-y)):
                    pixels[x,y] = plot_colors[CORE]

    image = image.resize((iWorldX * 52, iWorldY * 52), resample=Image.Resampling.NEAREST)
	
    image_path = config.OUTPUT_PATH / "maps/layers/Spawns/Respawns" / f"{name}.png"
    #print(image_path)
    image.save(image_path)

