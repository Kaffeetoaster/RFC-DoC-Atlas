from python.helper.helper import *
from python.consts import *
import config
from PIL import Image
from pathlib import Path

def getSpreadFactor(iReligion, iRegion):
	if iRegion < 0: 
		return -1
	
	return next((iFactor for iFactor, lRegions in tSpreadFactors[iReligion].items() if iRegion in lRegions), iNone)


def iterate_religion_spread_factors(iReligion):
	for (x,y), Tile in dTileMap.items():
		iRegion = Tile.get("region", -1)
		iSpreadFactor = getSpreadFactor(iReligion, iRegion)
		if iSpreadFactor == iCore:
			yield (x, y), CORE
		
		elif iSpreadFactor == iHistorical:
			yield (x, y), HISTORICAL
		
		elif iSpreadFactor == iPeriphery:
			yield (x, y), PERIPHERY
		
		elif iSpreadFactor == iMinority:
			yield (x, y), MINORITY
		

def draw_religion_map(iReligion, json_config):
	display_name = LReligionXML[iReligion].get("Description")
	print(display_name)
	
	image = Image.new("RGBA", (iWorldX, iWorldY), (0, 0, 0, 0))
	pixels = image.load()
	
	for (x, y), spread_factor_type in iterate_religion_spread_factors(iReligion):
		pixels[x, y] = plot_colors[spread_factor_type]
	
	image, offset = crop_image_to_content(image)  # Crop to content
	
	w,h = image.size
	image = image.resize((w * TILE_SIZE, h * TILE_SIZE), resample=Image.Resampling.NEAREST)
	
	image_path = config.OUTPUT_PATH / "maps/layers/Religions" / f"{display_name}.png"
	image.save(image_path)
	add_layer_config_entry(json_config, display_name, "Religion", Path(image_path).relative_to(config.OUTPUT_PATH), image.size, offset)

def DrawReligionMaps(json_config):
    for iReligion in range(iNumReligions):
        draw_religion_map(iReligion, json_config)