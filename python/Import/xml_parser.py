import xml.etree.ElementTree as ET

import config

from PIL import Image
from pathlib import Path

def strip_namespace(tag):
    return tag.split('}', 1)[-1] if '}' in tag else tag

def xml_to_dict(element):
    result = {}
    children = list(element)

    if children:
        child_dict = {}
        for child in children:
            tag = strip_namespace(child.tag)
            child_result = xml_to_dict(child)

            if tag not in child_dict:
                child_dict[tag] = child_result
            else:
                if not isinstance(child_dict[tag], list):
                    child_dict[tag] = [child_dict[tag]]
                child_dict[tag].append(child_result)

        return child_dict
    else:
        return element.text.strip() if element.text else ""

def xml_to_dict(element):
    result = {}
    children = list(element)

    if children:
        child_dict = {}
        for child in children:
            tag = strip_namespace(child.tag)
            child_result = xml_to_dict(child)

            if tag not in child_dict:
                child_dict[tag] = child_result
            else:
                if not isinstance(child_dict[tag], list):
                    child_dict[tag] = [child_dict[tag]]
                child_dict[tag].append(child_result)

        return child_dict
    else:
        return element.text.strip() if element.text else ""

def parse_xml_file(file_path):
    # takes an xml file and returns a parsed representation depending on the root tag
    tree = ET.parse(file_path)
    root = tree.getroot()
    root_tag = strip_namespace(root.tag)

    # Case 1: Civ4GameText -> dict keyed by <Tag>
    if root_tag == "Civ4GameText":
        result = {}
        for text_entry in root:

            entry_dict = xml_to_dict(text_entry)
            key = entry_dict.get("Tag")
            if key:
                result[key] = entry_dict

        return result

    # Case 2: Civ4ArtDefines -> dict keyed by <Type>
    case2 = ["Civ4ArtDefines", "Civ4PlayerColorInfos", "Civ4ColorVals"]
    if root_tag in case2:
        result = {}
        for category in root:
            for art_entry in category:
                entry_dict = xml_to_dict(art_entry)
                key = entry_dict.get("Type")
                if key:
                    result[key] = entry_dict

        return result

    # Case 3: all others -> list of entries, skipping the first two levels
    result = []
    if len(root) > 0:
        container = root[0]
        for item in container:
            result.append(xml_to_dict(item))

    return result


## build file index for loading with unknown capitalization
def build_case_index(root):
    root = Path(root).resolve()
    index = {}
    
    for path in root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(root)
            index[str(rel).lower()] = path
    
    return index

print("Built file index for case-insensitive loading of files.")
index = build_case_index(config.INPUT_PATH / "Assets")
print(f"file index built with {len(index)} entries.")

def get_path(path_str):
    return index.get(path_str.lower(), path_str)

### Resolving XML tags ###


def load_from_atlas(atlas_info):

    #print(f"loading from atlas {atlas_info[0]} with coords {atlas_info[1]}, {atlas_info[2]}")
    if Path(atlas_info[0]).stem == "Unit_Resource_Atlas":
        input_path_part = atlas_info[0]
        input_path_part = Path(input_path_part).parent / Path(input_path_part).name.lower()
        img = Image.open(config.INPUT_PATH / "Assets" / input_path_part)
        img.load()
        return img.crop(((int(atlas_info[1])-1)*64, (int(atlas_info[2])-1)*64, int(atlas_info[1])*64, int(atlas_info[2])*64))
    elif Path(atlas_info[0]).stem == "BaseTerrain_TerrainFeatures_Atlas":
        input_path_part = atlas_info[0]
        input_path_part = Path(input_path_part).parent / Path(input_path_part).name.lower()
        img = Image.open(config.INPUT_PATH / "Assets" / input_path_part)
        img.load()
        return img.crop(((int(atlas_info[1])-1)*64, (int(atlas_info[2])-1)*64, int(atlas_info[1])*64, int(atlas_info[2])*64))
    elif Path(atlas_info[0]).stem == "Beyond the Sword_Atlas":
        input_path_part = atlas_info[0]
        img = Image.open(config.INPUT_PATH / "Assets" / input_path_part)
        img.load()
        return img.crop(((int(atlas_info[1])-1)*64, (int(atlas_info[2])-1)*64, int(atlas_info[1])*64, int(atlas_info[2])*64))
    elif Path(atlas_info[0]).stem == "Beyond_the_Sword_Atlas":
        input_path_part = atlas_info[0]
        img = Image.open(config.INPUT_PATH.parent.parent / "Assets" / input_path_part)
        img.load()
        return img.crop(((int(atlas_info[1])-1)*64, (int(atlas_info[2])-1)*64, int(atlas_info[1])*64, int(atlas_info[2])*64))
    else:

        img = Image.open(config.INPUT_PATH.parent.parent.parent/ "Warlords/Assets" / atlas_info[0])
        img.load()
        return img.crop(((int(atlas_info[1])-1)*64, (int(atlas_info[2])-1)*64, int(atlas_info[1])*64, int(atlas_info[2])*64))
   

def convert_button_image(button_info, new_filename):
    # fix file path, save it on config.OUTPUT_PATH and return the new path
    if button_info == "" or button_info is None:
        #print(f"No button info for {new_filename}, skipping image conversion.")
        return None
    #print(f"Converting button image for {new_filename} with button info {button_info}")
    if type(button_info) is list:
            img = load_from_atlas(button_info)
            input_path_part = button_info[0]
    else:
        input_path_part = button_info
        #print(f"Original input path: {input_path_part}")
        input_path_part = get_path(input_path_part)
        #print(f"Resolved input path: {input_path_part}")
        
        # try open the image from the config.INPUT_PATH
        try:
            img = Image.open(config.INPUT_PATH / "Assets" / input_path_part)
            img.load()

        except Exception:
            # try in base extracted archive
            try:
                img = Image.open(config.INPUT_PATH.parent.parent.parent.parent/ "Art Assets" / input_path_part)
                img.load()
            except Exception as e:
                    print(f"Error occurred while opening {input_path_part}: {e}")
                    return ""
    output_path = config.OUTPUT_PATH / f"Assets/Art/Interface/Buttons/{new_filename}.png"
    img.save(output_path)
    return output_path


## dObjcetXML should be a list of objects eg civs, features, terrains, etc. ggf. a dict with "0", "1", etc. as keys, 
# and the infos as dicts. to keep it consisten with the other xmls?
## dArtXML, should be a dict of ART defines, that uses the "Type" tag as a key, and the infos as a dict.
## dTxtXML should be a dict of text defines, that uses the "tag" tag as a key, and the infos as a dict
## prepping the results of parse_xml should happen in xml_parser.py

### resolving xml tags ###
def update_GameObject_infos(iObject, LGameObjectXML, dArtXML, dTextXML, dPlayerColorXML, dColorXML):

    ## update description in place to english name
    description_tag = LGameObjectXML[iObject]["Description"]
    text_info = dTextXML.get(description_tag, description_tag)
    if text_info == description_tag:
        text = description_tag
    else:
        text = text_info.get("English", description_tag) 
    LGameObjectXML[iObject]["Description"] = text
    
    ## update short description. only civs have short descriptions, so check if it exists first
    if "ShortDescription" in LGameObjectXML[iObject]:
        short_description_tag = LGameObjectXML[iObject]["ShortDescription"]
        short_text_info = dTextXML.get(short_description_tag, short_description_tag)
        if short_text_info == short_description_tag:
            short_text = short_description_tag
        else:
            short_text = short_text_info.get("English", short_description_tag) 
        LGameObjectXML[iObject]["ShortDescription"] = short_text

    # update ArteDefineTag to path of button image
    # Religions dont have an ArtDefineTag, so check if it exists first
    if "ArtDefineTag" in LGameObjectXML[iObject]:
        art_define_tag = LGameObjectXML[iObject]["ArtDefineTag"]
        art_info = dArtXML[art_define_tag]
        value = art_info["Button"].split(',')
        button_info = value[2:] if len(value) > 1 else value[0]
    else: # case Religion
        button_info = LGameObjectXML[iObject].get("Button", "")
    new_path = convert_button_image(button_info, text)
    LGameObjectXML[iObject]["ArtDefineTag"] = new_path

    # update Color
    
    if "DefaultPlayerColor" in LGameObjectXML[iObject]:
        #print(f"Updating color for {LGameObjectXML[iObject]['Description']}")
        color_infos = dPlayerColorXML.get(LGameObjectXML[iObject]["DefaultPlayerColor"])
        color_infos_new = color_infos.copy()

        if color_infos:
            for ColorCategory, color in color_infos.items():
                if ColorCategory != "Type":
                    color_values = dColorXML.get(color, {})
                    R = float(color_values.get("fRed", 0.0))
                    G = float(color_values.get("fGreen", 0.0))
                    B = float(color_values.get("fBlue", 0.0))
                    A = float(color_values.get("fAlpha", 1.0))
                    color_infos_new[ColorCategory] = (round(R*255), round(G*255), round(B*255), round(A*255))
                    
                    #print(f"Updated color for {LGameObjectXML[iObject]['Description']} - {ColorCategory}: {color_infos_new[ColorCategory]}")
        LGameObjectXML[iObject]["Color"] = color_infos_new

    
    
    

def update_all_infos(LGameObjectXML, dArtXML, dTextXML, dPlayerColorXML = None, dColorXML= None):
    # iteriere über alle Objecte (civs, religions, boni, etc.) aus der LGameObjectXML und extrahiere die Infos für alle Objecte
    # das erste object hat die ID 0, die zweite die ID 1 etc.
    for iObject, dObject_info in enumerate(LGameObjectXML):
        update_GameObject_infos(iObject, LGameObjectXML, dArtXML, dTextXML, dPlayerColorXML, dColorXML)
