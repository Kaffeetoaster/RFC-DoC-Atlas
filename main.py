from python.extract_data import *
from python.consts import *
from python.DrawMaps.DrawStabAndReligon import *
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
### set some variables ###


    dCivNames = {
        iAmerica: "America",
        iArabia: "Arabia",
        iArgentina: "Argentina",
        iAssyria: "Assyria",
        iAustralia: "Australia",
        iAztecs: "Aztecs",
        iBabylonia: "Babylonia",
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
        iSpain: "Spain",
        iSwahili: "Swahili",
        iSweden: "Sweden",
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

    dPeriodNames = {
        iPeriodPtolemaicEgypt:			"Ptolemaic_Egypt",
        iPeriodMakuria:					"Makuria",
        iPeriodMing:					"Ming",
        iPeriodMaratha:					"Maratha",
        iPeriodModernGreece:			"Modern_Greece",
        iPeriodCarthage:				"Carthage",
        iPeriodInsularCelts:			"Insular_Celts",
        iPeriodVijayanagara:			"Vijayanagara",
        iPeriodByzantineConstantinople:	"Byzantine_Constantinople",
        iPeriodSeljuks:					"Seljuks",
        iPeriodNationalFrance:			"National_France",
        iPeriodMeiji:					"Meiji",
        iPeriodDenmark:					"Denmark",
        iPeriodNorway:					"Norway",
        iPeriodUzbeks:					"Uzbeks",
        iPeriodSaudi:					"Saudi",
        iPeriodMorocco:					"Morocco",
        iPeriodSpain:					"Spain",
        iPeriodAustria:					"Austria",
        iPeriodUnitedKingdom:			"United_Kingdom",
        iPeriodGreatBritain:			"Great_Britain",
        iPeriodYuan:					"Yuan",
        iPeriodPeru:					"Peru",
        iPeriodLateInca:				"Late_Inca",
        iPeriodModernItaly:				"Modern_Italy",
        iPeriodPakistan:				"Pakistan",
        iPeriodOttomanConstantinople:   "Ottoman_Constantinople",
        iPeriodQing:	                "Qing",
        iPeriodModernGermany:			"Modern_Germany",
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



### Draw Stab Maps ###
    for iCiv in dCivNames:
        draw_stability_map_for_civ(iCiv)
        
        for iPeriod in dCivPeriods.get(iCiv, []):
            if should_draw_for_period(iPeriod):
                draw_stability_map_for_period(iCiv, iPeriod)
### Draw Religion Maps ###
    for iReligion in range(iNumReligions):
        draw_religion_map(iReligion)

### Draw Spawn Maps ### 

### Draw Resource Spawn Map ###
 
### Draw UHV Maps ###

### Draw Geography ###
# Regions
# Peak changes

### Draw general Resource Map ###


