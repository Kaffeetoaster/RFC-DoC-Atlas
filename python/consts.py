from python.Import.extract_python_data import *
from python.Import.load_csv import *
from python.Import.xml_parser import *

import config

from collections import defaultdict
from pathlib import Path
import time


### load and resolve consts from Python files ###
global_context = {}

extract_variables(config.INPUT_PATH /'Assets/Python/Consts.py', global_context)
extract_variables(config.INPUT_PATH /'Assets/Python/Areas.py', global_context)
extract_variables(config.INPUT_PATH /'Assets/Python/Resources.py', global_context)
extract_variables(config.INPUT_PATH /'Assets/Python/RegionMap.py', global_context)
extract_variables(config.INPUT_PATH /'Assets/Python/Locations.py', global_context)
extract_variables(config.INPUT_PATH /'Assets/Python/Periods.py', global_context)

globals().update(global_context)

### consts from Python files loaded and resolved ###


### load tile infos from csv maps ### 
gen_Bonus = iterate_number_map("Earth/Bonus.csv")
gen_BonusVariety = iterate_number_map("Earth/BonusVariety.csv")
gen_Feature = iterate_number_map("Earth/Feature.csv")
gen_FeatureVariety = iterate_number_map("Earth/FeatureVariety.csv")
gen_Plot = iterate_string_map("Earth/Plot.csv")
gen_Terrain = iterate_number_map("Earth/Terrain.csv")
gen_Region = iterate_number_map("Regions.csv")
gen_landmass = iterate_number_map("Earth/Landmass.csv")
gen_Continent = iterate_number_map("Earth/Continent.csv")

gens = [
    ("terrain", gen_Terrain),
    ("bonus", gen_Bonus),
    ("bonus_variety", gen_BonusVariety),
    ("feature", gen_Feature),
    ("feature_variety", gen_FeatureVariety),
    ("plot", gen_Plot),
    ("region", gen_Region),
    ("landmass", gen_landmass),
    ("continent", gen_Continent)
]

dTileMap = defaultdict(dict)

for key, gen in gens:
    for (x, y), value in gen:
        if value is not None:
            dTileMap[(x, y)][key] = value


### tile infos from csv maps loaded ###


### load xml infos ###

## load xml resource infos and convert images to png for web usage
# version
LVersionXML = parse_xml_file(config.INPUT_PATH / "Assets/XML/GlobalDefinesVersion.xml")
print(f"Loaded Version")
sModVersion = LVersionXML[1]
print(sModVersion)
# base Objects
LBonusXML = parse_xml_file(config.INPUT_PATH / "Assets/XML/Terrain/CIV4BonusInfos.xml")
print(f"Loaded {len(LBonusXML)} Bonus XML entries")
LFeatureXML = parse_xml_file(config.INPUT_PATH / "Assets/XML/Terrain/CIV4FeatureInfos.xml")
print(f"Loaded {len(LFeatureXML)} Feature XML entries")
LTerrainXML = parse_xml_file(config.INPUT_PATH / "Assets/XML/Terrain/CIV4TerrainInfos.xml")
print(f"Loaded {len(LTerrainXML)} Terrain XML entries")
LCivXML = parse_xml_file(config.INPUT_PATH / "Assets/XML/Civilizations/CIV4CivilizationInfos.xml")
print(f"Loaded {len(LCivXML)} Civilization XML entries")
LReligionXML = parse_xml_file(config.INPUT_PATH / "Assets/XML/GameInfo/CIV4ReligionInfo.xml")
print(f"Loaded {len(LReligionXML)} Religion XML entries")

# Art
dArtXML = parse_xml_file(config.INPUT_PATH / "Assets/XML/Art/CIV4ArtDefines_Bonus.xml")
print(f"Loaded {len(dArtXML)} Bonus Art XML entries")
dArtXML |= parse_xml_file(config.INPUT_PATH / "Assets/XML/Art/CIV4ArtDefines_Feature.xml")
print(f"Loaded {len(dArtXML)} Feature Art XML entries")
dArtXML |= parse_xml_file(config.INPUT_PATH / "Assets/XML/Art/CIV4ArtDefines_Civilization.xml")
print(f"Loaded {len(dArtXML)} Civilization Art XML entries")
dArtXML |= parse_xml_file(config.INPUT_PATH / "Assets/XML/Art/CIV4ArtDefines_Terrain.xml")
print(f"Loaded {len(dArtXML)} Terrain Art XML entries")

# Colors
dColorXML = parse_xml_file(config.INPUT_PATH / "Assets/XML/Interface/CIV4ColorVals.xml")
dPlayerColorXML = parse_xml_file(config.INPUT_PATH / "Assets/XML/Interface/CIV4PlayerColorInfos.xml")

# Text
dTextXML = parse_xml_file(config.INPUT_PATH.parent.parent.parent / "Assets/XML/Text/CIV4GameTextInfos_Objects.xml")
print(f"Loaded {len(dTextXML)} GameText Object XML entries")
dTextXML_temp = parse_xml_file(config.INPUT_PATH.parent.parent.parent / "Warlords/Assets/XML/Text/CIV4GameText_Warlords.xml")
dTextXML |= dTextXML_temp
print(f"Loaded {len(dTextXML_temp)} Warlords Text XML entries")

dTextXML_temp = parse_xml_file(config.INPUT_PATH / "Assets/XML/Text/Resources.xml")
dTextXML |= dTextXML_temp
print(f"Loaded {len(dTextXML_temp)} Resource Text XML entries")
dTextXML_temp = parse_xml_file(config.INPUT_PATH / "Assets/XML/Text/Features.xml")
dTextXML |= dTextXML_temp
print(f"Loaded {len(dTextXML_temp)} Feature Text XML entries")
dTextXML_temp = parse_xml_file(config.INPUT_PATH / "Assets/XML/Text/Terrain.xml")
dTextXML |= dTextXML_temp
print(f"Loaded {len(dTextXML_temp)} Terrain Text XML entries")
dTextXML_temp = parse_xml_file(config.INPUT_PATH / "Assets/XML/Text/Regions.xml")
dTextXML |= dTextXML_temp
print(f"Loaded {len(dTextXML_temp)} Regions Text XML entries")
dTextXML_temp = parse_xml_file(config.INPUT_PATH / "Assets/XML/Text/Religions.xml")
dTextXML |= dTextXML_temp
print(f"Loaded {len(dTextXML_temp)} Religions Text XML entries")



for file in Path(config.INPUT_PATH / "Assets/XML/Text/DynamicNames").glob("*.xml"):
    dTextXML_temp= parse_xml_file(file)
    dTextXML |= dTextXML_temp
    print(f"Loaded {len(dTextXML_temp)} Dynamic Names Text XML entries from {file.name}")

### load xml resource infos and convert images to png for web usage
update_all_infos(LBonusXML, dArtXML, dTextXML)
update_all_infos(LFeatureXML, dArtXML, dTextXML)
update_all_infos(LTerrainXML, dArtXML, dTextXML)
update_all_infos(LCivXML, dArtXML, dTextXML,dPlayerColorXML, dColorXML)

# Religions dont have an ARTDefineTag, the Path to the Button is in the ReligionXML itself.
update_all_infos(LReligionXML, dArtXML, dTextXML)




### set some variables ###
dCivNames = {
    iAmerica: "America",
    iArabia: "Arabia",
    iArgentina: "Argentina",
    iAssyria: "Assyria",
    iAustralia: "Australia",
    iAztecs: "Aztecs",
    iBabylonia: "Babylonia",
    iBelgium: "Belgium",
    iBrazil: "Brazil",
    iBurma: "Burma",
    iByzantium: "Byzantium",
    iCanada: "Canada",
    iCarthage: "Phoenicia",
    iCelts: "Celts",
    iChina: "China",
    iColombia: "Colombia",
    iDravidia: "Dravidia",
    iEgypt: "Egypt",
    iEngland: "England",
    iEthiopia: "Ethiopia",
    iFrance: "France",
    iGermany: "Germany",
    iGreece: "Greece",
    iHarappa: "Harappa",
    iHittites: "Hittites",
    iHolyRome: "Holy_Rome",
    iInca: "Inca",
    iIndia: "India",
    iIran: "Iran",
    iItaly: "Italy",
    iJapan: "Japan",
    iJava: "Java",
    iKhmer: "Khmer",
    iCongo: "Congo",
    iKorea: "Korea",
    iKushans: "Kushans",
    iMalays: "Malaya",
    iMali: "Mali",
    iManchuria: "Manchuria",
    iMaya: "Maya",
    iMexico: "Mexico",
    iMisr: "Misr",
    iMongols: "Mongolia",
    iMoors: "Moors",
    iMughals: "Mughals",
    iNetherlands: "Netherlands",
    iNorse: "Norse",
    iNubia: "Nubia",
    iOttomans: "Turkey",
    iPersia: "Persia",
    iPoland: "Poland",
    iPolynesia: "Polynesia",
    iPortugal: "Portugal",
    iRome: "Rome",
    iRus: "Ruthenia",
    iRussia: "Russia",
    iSaudis: "Saudis",
    iSpain: "Spain",
    iSwahili: "Swahili",
    iSweden: "Sweden",
    iTatars: "Tartary",
    iThailand: "Thailand",
    iTibet: "Tibet",
    iToltecs: "Toltecs",
    iTurks: "Turkestan",
    iVietnam: "Vietnam",
}

dCivPeriods = {
    iEgypt: [iPeriodPtolemaicEgypt],
    iNubia: [iPeriodMakuria],
    iChina: [iPeriodMing],
    iIndia: [iPeriodMaratha],
    iGreece: [iPeriodModernGreece],
    iCarthage: [iPeriodCarthage],
    iCelts: [iPeriodInsularCelts],
    iDravidia: [iPeriodVijayanagara],
    iByzantium: [iPeriodByzantineConstantinople],
    iTurks: [iPeriodSeljuks, iPeriodUzbeks],
    iFrance: [iPeriodNationalFrance],
    iJapan: [iPeriodMeiji],
    iNorse: [iPeriodDenmark, iPeriodNorway],
    iArabia: [iPeriodSaudi],
    iMoors: [iPeriodMorocco],
    iSpain: [iPeriodSpain],
    iHolyRome: [iPeriodAustria],
    iEngland: [iPeriodUnitedKingdom, iPeriodGreatBritain],
    iMongols: [iPeriodYuan],
    iInca: [iPeriodPeru, iPeriodLateInca],
    iItaly: [iPeriodModernItaly],
    iMughals: [iPeriodPakistan],
    iOttomans: [iPeriodOttomanConstantinople],
    iGermany: [iPeriodModernGermany],
    iManchuria: [iPeriodQing],
}

dReligionNames = {
    iJudaism: "Judaism",
    iOrthodoxy: "Orthodoxy",
    iCatholicism: "Catholicism",
    iProtestantism: "Protestantism",
    iIslam: "Islam",
    iHinduism: "Hinduism",
    iBuddhism: "Buddhism",
    iConfucianism: "Confucianism",
    iTaoism: "Taoism",
    iZoroastrianism: "Zoroastrianism",
}


(LAND, WATER, PEAK, CORE, HISTORICAL, CONQUEST, FOREIGN, MINORITY, PERIPHERY) = range(9)

plot_colors = {
    LAND: (175, 175, 175),
    WATER: (50, 100, 100),
    PEAK: (50, 50, 50),
    CORE: (41, 249, 255, 110),
    HISTORICAL: (8, 179, 69, 110),
    CONQUEST: (250, 184, 56, 110),
    FOREIGN: (240, 64, 102, 110),
    PERIPHERY: (250, 184, 56, 150),
    MINORITY: (255, 220, 115, 150),
}

TILE_SIZE = 32
