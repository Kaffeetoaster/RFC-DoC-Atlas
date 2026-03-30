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

def parse_xml_file(file_path):
    ## takes an xml file and returns a nested dictionary representing the XML structure without namespaces
    tree = ET.parse(file_path)
    root = tree.getroot()
    return {strip_namespace(root.tag): xml_to_dict(root)}




def convert_to_png(input_path, output_path):
    try :
        img = Image.open(input_path)
        img.save(output_path)
    except Exception as e:
        print(f"Error occurred while converting {input_path} to PNG: {e}")




def get_infos(lEntries, tag, name):
    for entry in lEntries:
        if entry[tag] == name:
            return entry
        

def extract_resource_infos(iresource, dBonusXML, dArtXML, dTextXML, dResourceTextXML,dWarlordsTextXML):
    info = dBonusXML["Civ4BonusInfos"]["BonusInfos"]["BonusInfo"][iresource]
    art_define_tag = info["ArtDefineTag"]
    description_tag = info["Description"]
    art_info = get_infos(dArtXML["Civ4ArtDefines"]["BonusArtInfos"]["BonusArtInfo"], "Type", art_define_tag)
    

    value = art_info["Button"].split(',')
    button_info = value[1] if len(value) > 1 else value[0]
    
    text_info = get_infos(dResourceTextXML["Civ4GameText"]["TEXT"],"Tag", description_tag)
    if text_info is None:
        text_info = get_infos(dTextXML["Civ4GameText"]["TEXT"],"Tag", description_tag)
    if text_info is None:
        text_info = get_infos(dWarlordsTextXML["Civ4GameText"]["TEXT"],"Tag", description_tag)
    text = text_info["English"] if text_info else description_tag

    #print(f"description was {description_tag}, text is {text_info}")
    return {
        "text": text,   
        "path_art": button_info
    }

def extract_all_resource_infos():
    # iteriere über alle BonusInfos aus der dBonusXML und extrahiere die Infos für alle Ressourcen
    # die erste Bonusinfo bekommt die ID 0, die zweite die ID 1 etc.
    dBonusXML = parse_xml_file(config.INPUT_PATH / "Assets/XML/Terrain/CIV4BonusInfos.xml")
    dArtXML = parse_xml_file(config.INPUT_PATH / "Assets/XML/Art/CIV4ArtDefines_Bonus.xml")
    dTextXML = parse_xml_file(config.INPUT_PATH.parent.parent.parent / "Assets/XML/Text/CIV4GameTextInfos_Objects.xml")
    dResourceTextXML = parse_xml_file(config.INPUT_PATH / "Assets/XML/Text/Resources.xml")
    dWarlordsTextXML = parse_xml_file(config.INPUT_PATH.parent.parent.parent / "Warlords/Assets/XML/Text/CIV4GameText_Warlords.xml")
    dResourceInfos = {}
    for iresource, bonus_info in enumerate(dBonusXML["Civ4BonusInfos"]["BonusInfos"]["BonusInfo"]):
        
        dResourceInfos[iresource] = extract_resource_infos(iresource, dBonusXML, dArtXML, dTextXML, dResourceTextXML,dWarlordsTextXML)

    return dResourceInfos

#/home/anton/.wine/drive_c/Program Files (x86)/2K Games/Firaxis Games/Art Assets/Art/interface/buttons/worldbuilder
#
def convert_resource_images(dResourceInfos):
    for iresource, resource_info in dResourceInfos.items():
        input_path_part = resource_info["path_art"]

        input_path_lower = Path(input_path_part).parent / Path(input_path_part).name.lower()
        
        # try open the image from the config.INPUT_PATH
        try:
            img = Image.open(config.INPUT_PATH / "Assets" / input_path_part)
            img.load()
        except Exception:
            # Try with lowercase filename
            try:
                img = Image.open(config.INPUT_PATH / "Assets" / input_path_lower)
                img.load()
            except Exception:
                try:
                    img = Image.open(config.INPUT_PATH.parent.parent.parent.parent/ "Art Assets" / input_path_part)
                    img.load()
                except Exception as e:
                        print(f"Error occurred while opening {input_path_part}: {e}")
                        continue

        output_path = config.OUTPUT_PATH / f"resources/{Path(input_path_part).stem}.png"
        img.save(output_path)
        dResourceInfos[iresource]["path_art"] = output_path


 


