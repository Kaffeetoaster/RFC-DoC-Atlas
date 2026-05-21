from turtle import color

from python.consts import *
from python.helper.helper import *

import config


def DrawCultureMap(layers_config, scenario_name):
	print(scenario_name)
	display_name = scenario_name.replace("RFC_", "")
	display_name = display_name[:-2] + " " + display_name[-2:] 
	image = Image.new("RGBA", (iWorldX, iWorldY), (0, 0, 0, 0))
	pixels = image.load()
	
	for (x, y), tile_info in dTileMap.items():
		iCiv = tile_info.get(f"culture_{scenario_name}")
		if iCiv is not None:
			#print(f"Owner for tile {(x, y)}: {iCiv}")
			color = LCivXML[iCiv]["Color"].get("ColorTypePrimary", (0, 0, 0, 255))
			tile_color = color[:3] + (150,) 
			pixels[x, y] = tile_color
            
	
	image, offset = crop_image_to_content(image)  # Crop to content
	
	w,h = image.size
	image = image.resize((int(w * TILE_SIZE), int(h * TILE_SIZE)), resample=Image.Resampling.NEAREST)
	image_path = config.OUTPUT_PATH / "maps/layers/Culture" / f"{scenario_name}.webp"
	image.save(image_path, "WEBP", quality=80, method=6)  # Save as WebP with good compression
	
	add_layer_config_entry(layers_config, display_name, "Scenario Culture", Path(image_path).relative_to(config.OUTPUT_PATH), image.size, offset)

def DrawScenarioCultureMaps(layers_config):
    for file in Path(config.INPUT_PATH / "Assets/Maps/Scenario").glob("*.csv"):
        scenario_name = file.stem
        DrawCultureMap(layers_config, scenario_name)