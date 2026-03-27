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


def iterate_map(file_path):
	full_file_path = get_full_path(file_path)
	
	with open(full_file_path) as file:
		for y, line in enumerate(csv.reader(file)):
			for x, value in enumerate(line):
				if not value:
					yield (x, y), 0
				else:
					yield (x, y), int(value)
					
					
def is_area(rectangle, exceptions, identifier, tile):
	x, y = tile
	
	(x1, y1), (x2, y2) = rectangle[identifier]
	excluded = exceptions.get(identifier, [])
	
	return x1 <= x <= x2 and y1 <= y <= y2 and (x, y) not in excluded


def is_core(iCiv, tile):
	return is_area(dCoreArea, dCoreAreaExceptions, iCiv, tile)


def is_period_core(identifier, tile):
	iCiv, iPeriod = identifier
	
	if iPeriod not in dPeriodCoreArea:
		return is_core(iCiv, tile)
	
	return is_area(dPeriodCoreArea, dPeriodCoreAreaExceptions, iPeriod, tile)


def iterate_civ_map(iCiv):
	civ_name = dCivNames[iCiv]

	settler_values = iterate_map(f"Settler/{civ_name}.csv")
	war_values = iterate_map(f"War/{civ_name}.csv")
	
	return iterate_plot_types(iCiv, settler_values, war_values, is_core)


def iterate_period_map(iCiv, iPeriod):
	period_name = dPeriodNames[iPeriod]
	civ_name = dCivNames[iCiv]
	
	settler_map = f"Settler/Period/{period_name}.csv"
	war_map = f"War/Period/{period_name}.csv"
	
	if map_exists(settler_map):
		settler_values = iterate_map(settler_map)
	else:
		settler_values = iterate_map(f"Settler/{civ_name}.csv")
	
	if map_exists(war_map):
		war_values = iterate_map(war_map)
	else:
		war_values = iterate_map(f"War/{civ_name}.csv")
	
	if iPeriod in dPeriodCoreArea:
		core_func = is_period_core
		identifier = (iCiv, iPeriod)
	else:
		core_func = is_core
		identifier = iCiv
	
	return iterate_plot_types(identifier, settler_values, war_values, core_func)


def iterate_plot_types(identifier, settler_values, war_values, core_func):
	terrain_values = iterate_map("Export/BaseTerrain.csv")
	
	for ((x, y), iSettlerValue), (_, iWarValue), (_, iTerrainValue) in zip(settler_values, war_values, terrain_values):
		##if iTerrainValue == 2:
		##	yield (x, y), PEAK
			
		if iTerrainValue != 0 and core_func(identifier, (x, iWorldY-1-y)):
			yield (x, y), CORE
		
		elif iSettlerValue > 0:
			yield (x, y), HISTORICAL
		
		elif iWarValue > 1:
			yield (x, y), CONQUEST
		
		##elif iTerrainValue == 0:
		##	yield (x, y), WATER
		
		##else:
		#	yield (x, y), LAND


def draw_stability_map(name, values):
	print(name)
	name_display = name.replace("Periods/","").replace("_"," -> ")
	#print(f"""        <label class="option"><input type="checkbox" data-target="stability_{name}">{name_display}</label>""")
	#print(f"""   <img id="stability_{name}" src="maps/layers/stability/{name}.png" class="overlay">""")
	
	image = Image.new("RGBA", (iWorldX, iWorldY), (0, 0, 0, 0))
	pixels = image.load()
	
	for (x, y), plot_type in values:
		pixels[x, y] = plot_colors[plot_type]
	
	image = image.resize((iWorldX * 52, iWorldY * 52), resample=Image.Resampling.NEAREST)
	
	image_path = config.OUTPUT_PATH / "maps/layers/Stability" / f"{name}.png"
	print(image_path)
	image.save(image_path)


def draw_stability_map_for_civ(iCiv):
	civ_name = dCivNames[iCiv]
	values = iterate_civ_map(iCiv)
	
	draw_stability_map(civ_name, values)


def draw_stability_map_for_period(iCiv, iPeriod):
	civ_name = dCivNames[iCiv]
	period_name = dPeriodNames[iPeriod]
	values = iterate_period_map(iCiv, iPeriod)
	
	draw_stability_map(f"Periods/{civ_name}_{period_name}", values)


def should_draw_for_period(iPeriod):
	period_name = dPeriodNames[iPeriod]
	
	return map_exists(f"Settler/Period/{period_name}.csv") or map_exists(f"War/Period/{period_name}.csv") or iPeriod in dPeriodCoreArea


def getSpreadFactor(iReligion, iRegion):
	if iRegion < 0: 
		return -1
	
	return next((iFactor for iFactor, lRegions in tSpreadFactors[iReligion].items() if iRegion in lRegions), iNone)


def iterate_religion_spread_factors(iReligion):
	region_values = iterate_map("Regions.csv")
	terrain_values = iterate_map("Export/BaseTerrain.csv")
	
	for ((x, y), iRegion), (_, iTerrain) in zip(region_values, terrain_values):
		iSpreadFactor = getSpreadFactor(iReligion, iRegion)
	
		# if iTerrain == 0:
		# 	yield (x, y), WATER
	
		# elif iTerrain == 2:
		# 	yield (x, y), PEAK
		
		if iSpreadFactor == iCore:
			yield (x, y), CORE
		
		elif iSpreadFactor == iHistorical:
			yield (x, y), HISTORICAL
		
		elif iSpreadFactor == iPeriphery:
			yield (x, y), PERIPHERY
		
		elif iSpreadFactor == iMinority:
			yield (x, y), MINORITY
		
		# else:
		# 	yield (x, y), LAND
			


def draw_religion_map(iReligion):
	print(dReligionNames[iReligion])
	
	image = Image.new("RGBA", (iWorldX, iWorldY), (0, 0, 0, 0))
	pixels = image.load()
	
	for (x, y), spread_factor_type in iterate_religion_spread_factors(iReligion):
		pixels[x, y] = plot_colors[spread_factor_type]
	
	image = image.resize((iWorldX * 52, iWorldY * 52), resample=Image.Resampling.NEAREST)
	
	image_path = config.OUTPUT_PATH / "maps/layers/Religions" / f"{dReligionNames[iReligion]}.png"
	image.save(image_path)

	