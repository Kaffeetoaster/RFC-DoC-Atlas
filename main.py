from python.extract_data import *
import config


input_path = config.INPUT_PATH
output_path = config.OUTPUT_PATH

### Entry Point for the map creating Process ###

### load files. be careful order is relevant! ###


if __name__ == "__main__":
    
    global_context = {}

    extract_variables(input_path /'Assets/Python/Consts.py', global_context)
    extract_variables(input_path /'Assets/Python/Areas.py', global_context)
    extract_variables(input_path /'Assets/Python/Resources.py', global_context)
    extract_variables(input_path /'Assets/Python/RegionMap.py', global_context)
    extract_variables(input_path /'Assets/Python/Locations.py', global_context)

    globals().update(global_context)


