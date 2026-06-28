import csv
import config
from pathlib import Path

### loads all .csv files with terrain info and returns a dict with "x,y" : {infos}

def iterate_number_map(file_path):
	full_file_path = Path(config.INPUT_PATH / "Assets/Maps" / file_path)
	
	with open(full_file_path) as file:
		for y, line in enumerate(csv.reader(file)):
			for x, value in enumerate(line):
				if not value:
					yield (x, y), 0
				else:
					yield (x, y), int(value)
					
def iterate_string_map(file_path):
	full_file_path = Path(config.INPUT_PATH / "Assets/Maps" / file_path)
	
	with open(full_file_path) as file:
		for y, line in enumerate(csv.reader(file)):
			for x, value in enumerate(line):
				if not value:
					yield (x, y), ""
				else:
					yield (x, y), str(value)

### iterate over all maps. get the values

