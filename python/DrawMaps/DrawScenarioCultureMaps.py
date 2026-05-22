from turtle import color

from python.consts import *
from python.helper.helper import *

import config

def fix_outdated_culture_data():
	for (x, y), tile_info in dTileMap.items():
		for iyear in lScenarioStartYears:
			scenario_name = f"RFC_{str(-iyear)}BC" if iyear < 0 else f"RFC_{iyear}AD"
			culture_key = f"culture_{scenario_name}"
			
			for iCiv in range(62, iNumCivs, -1):
				if tile_info.get(culture_key) == iCiv:
					dTileMap[(x, y)][culture_key] = iCiv + 1
					



def DrawCultureMap(layers_config, scenario_name):
	print(scenario_name)
	display_name = scenario_name.replace("RFC_", "")
	display_name = display_name[:-2] + " " + display_name[-2:] 
	image = Image.new("RGBA", (iWorldX, iWorldY), (0, 0, 0, 0))
	pixels = image.load()
	
	for (x, y), tile_info in dTileMap.items():
		culture_key = f"culture_{scenario_name}"
		## 
		for iCiv in range(iNumCivs - 1, 61, -1):
				if tile_info.get(culture_key) == iCiv:
					tile_info[culture_key] = iCiv + 1
     
		iCiv = tile_info.get(culture_key)
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
	for iyear in lScenarioStartYears:
		if iyear != -3000:  # Skip the -3000 scenario
			scenario_name = f"RFC_{str(-iyear)}BC" if iyear < 0 else f"RFC_{iyear}AD"
			DrawCultureMap(layers_config, scenario_name)