"""
This is a simple parcer
It converts configuration files for RealFuels mod (for Kerbal Space Program)
to ODS human-readable table format
"""
__author__ = 'Snownoise'
__license__ = "GNU GPLv3 "
__version__ = "0.0.3"
__maintainer__ = "Snownoise"
__email__ = "snownoise@gmail.com"

import re
import datetime
import argparse
import pyexcel_ods3
from collections import OrderedDict
from RF_parcer_classes import *

# Init and config variables
cfg_inputfile = ""
cfg_outputfile = ""
main_data = []  # Main text data from config
parced = []     # Parced data
toExport = []   # List with exported data
depth = 0       # Depth

MODE_PART = 1
MODE_MODULEENGINES = 2
MODE_MODULEENGINECONFIGS = 3
MODE_MODULEENGINEIGNITOR = 4
MODE_MODULEENGINE_ATM_CURVE = 5
MODE_PROPELLANT = 6
MODE_CONFIG = 7
MODE_IGNITORRESOURCE = 8
MODE_MODULERCS = 9
MODE_MODULEFUELTANK = 10
MODE_MODULETANKCONTENT = 11
MODE_GENERICMODULE = 99


def parcer(input_data, previous_line, previous_mode):
    global depth, parced
    prev = previous_line
    part = "blankPart"
    mode = 0
    flag_electric_ignitor = False

    # This is module recognition block to determine in which type on module we are in;
    # Executes only once for each block of config's code
    # General PART search block
    if regex_part_name.findall(prev):
        partName = regex_part_name.findall(prev)[0]
        partComment = regex_comment.findall(prev)[0] if regex_comment.findall(prev) else "" # Check for comment existance
        part = PartClass(partName, partComment)
        mode = MODE_PART    # This is PART, not something else

    # @ModuleEngines
    elif regex_moduleEngines.findall(prev):
        mode = MODE_MODULEENGINES
        part = ModuleEngineClass()

    # @ModuleRCS
    elif regex_moduleRCS.findall(prev):
        mode = MODE_MODULERCS
        part = ModuleRCSClass()

    # ModuleEngineIgnitor
    elif (regex_moduleEngineIgnitor.findall(prev) and
         (previous_mode == MODE_PART or previous_mode == MODE_CONFIG)):
        mode = MODE_MODULEENGINEIGNITOR
        part = ModuleEngineIgnitorClass()

    # Ignitor Resouce
    elif regex_ignitorResource.findall(prev):
        mode = MODE_IGNITORRESOURCE
        part = -1.0

    # AtmosphereCurve
    elif (regex_atmosphereCurve.findall(prev) and
         (previous_mode == MODE_MODULEENGINES or previous_mode == MODE_MODULERCS)):
        mode = MODE_MODULEENGINE_ATM_CURVE
        part = {"key0":-1,
                "key1":-1}

    # Propellant section
    elif (regex_propellant.findall(prev) and
         (previous_mode == MODE_MODULEENGINES or previous_mode == MODE_CONFIG)):
        mode = MODE_PROPELLANT
        part = PropellantClass()

    # Generic Module
    elif regex_module.findall(prev): mode = MODE_GENERICMODULE

    # Engine config (CONFIG)
    elif regex_config.findall(prev):
        mode = MODE_CONFIG
        part = EngineConfigClass()

    # Internal tank in ModuleFuelTank (TANK)
    elif regex_tank.findall(prev):
        mode = MODE_MODULETANKCONTENT
        part = ModuleFuelTankInternal()


    # Here are the main loop with most of RegEx'es
    # I'm using while loop, because I need to count lines and moving skip cycles after returning from nested function
    num = 1
    while num<len(input_data)+1:
        line = input_data[num-1]

        # Searching for part's mass
        if regex_mass.findall(line) and mode == MODE_PART:
            mass = regex_mass.findall(line)[0][0]
            part.mass = float(mass)

        # Searching for part's cost
        elif regex_cost.findall(line) and mode == MODE_PART:
            cost = regex_cost.findall(line)[0][0]
            part.cost = int(float(cost))

        # Searching for part's entry cost
        elif regex_entryCost.findall(line) and mode == MODE_PART:
            temp_value = regex_entryCost.findall(line)[0][0]
            part.entryCost = int(float(temp_value))

        # Searching for part's max temp
        elif regex_maxTemp.findall(line) and mode == MODE_PART:
            temp_value = regex_maxTemp.findall(line)[0][0]
            part.maxTemp = int(float(temp_value))

        ### ****************************************************
        ### ModuleEngines / ModuleEnginesRF
        ### ****************************************************

        # maxThrust
        elif regex_maxThrust.findall(line) and mode == MODE_MODULEENGINES:
            temp_value = regex_maxThrust.findall(line)[0][1]
            part.maxThrust = float(temp_value)

        # heatProduction
        elif regex_heatProduction.findall(line) and mode == MODE_MODULEENGINES:
            temp_value = regex_heatProduction.findall(line)[0][1]
            part.heatProduction = float(temp_value)

        # Atmosphere Curve Key0
        elif regex_atmosphereCurveKey0.findall(line) and mode == MODE_MODULEENGINE_ATM_CURVE:
            temp_value = regex_atmosphereCurveKey0.findall(line)[0][0]
            part["key0"] = int(float(temp_value))

        # Atmosphere Curve Key1
        elif regex_atmosphereCurveKey1.findall(line) and mode == MODE_MODULEENGINE_ATM_CURVE:
            temp_value = regex_atmosphereCurveKey1.findall(line)[0][0]
            part["key1"] = int(float(temp_value))


        ### ****************************************************
        ### ModuleRCS
        ### ****************************************************

        # thrusterPower
        elif regex_thrusterPower.findall(line) and mode == MODE_MODULERCS:
            temp_value = regex_thrusterPower.findall(line)[0][1]
            part.thrusterPower = float(temp_value)

        # heatProduction
        elif regex_heatProduction.findall(line) and mode == MODE_MODULERCS:
            temp_value = regex_heatProduction.findall(line)[0][1]
            part.heatProduction = float(temp_value)

        # Atmosphere Curve Key0
        elif regex_atmosphereCurveKey0.findall(line) and mode == MODE_MODULEENGINE_ATM_CURVE:
            temp_value = regex_atmosphereCurveKey0.findall(line)[0][0]
            part["key0"] = int(float(temp_value))

        # Atmosphere Curve Key1
        elif regex_atmosphereCurveKey1.findall(line) and mode == MODE_MODULEENGINE_ATM_CURVE:
            temp_value = regex_atmosphereCurveKey1.findall(line)[0][0]
            part["key1"] = int(float(temp_value))


        ### ****************************************************
        ### ModuleEngineIgnitor
        ### ****************************************************
        # ignitionsAvailable
        elif regex_ignitionsAvailable.findall(line) and mode == MODE_MODULEENGINEIGNITOR:
            temp_value = regex_ignitionsAvailable.findall(line)[0][0]
            part.ignitionsAvailable = int(float(temp_value))

        # autoIgnitionTemperature
        elif regex_autoIgnitionTemperature.findall(line) and mode == MODE_MODULEENGINEIGNITOR:
            temp_value = regex_autoIgnitionTemperature.findall(line)[0][0]
            part.autoIgnitionTemperature = int(float(temp_value))

        # useUllageSimulation
        elif regex_useUllageSimulation.findall(line) and mode == MODE_MODULEENGINEIGNITOR:
            temp_value = regex_useUllageSimulation.findall(line)[0]
            part.useUllageSimulation = str(temp_value)

        ### ****************************************************
        ### Ignitor Resouce (resource amount)
        ### ****************************************************
        elif regex_name.findall(line) and mode == MODE_IGNITORRESOURCE:
            temp_value = regex_name.findall(line)[0][0]
            temp_value = temp_value.strip()
            temp_value = temp_value.lower()
            if temp_value == "electriccharge": flag_electric_ignitor = True

        elif regex_ECamount.findall(line) and mode == MODE_IGNITORRESOURCE and flag_electric_ignitor:
            temp_value = regex_ECamount.findall(line)[0][0]
            part = float(temp_value)

        ### ****************************************************
        ### Propellant
        ### ****************************************************
        # Name
        elif regex_name.findall(line) and mode == MODE_PROPELLANT:
            temp_value = regex_name.findall(line)[0][0]
            part.name = str(temp_value)

        # Ratio
        elif regex_prop_ratio.findall(line) and mode == MODE_PROPELLANT:
            temp_value = regex_prop_ratio.findall(line)[0][0]
            part.ratio = float(temp_value)

        # DrawGauge
        elif regex_prop_drawGauge.findall(line) and mode == MODE_PROPELLANT:
            temp_value = regex_prop_drawGauge.findall(line)[0]
            part.drawGauge = temp_value

        # FlowMode
        elif regex_prop_flow.findall(line) and mode == MODE_PROPELLANT:
            temp_value = regex_prop_flow.findall(line)[0][1]
            part.flowMode = str(temp_value)

        ### ****************************************************
        ### Generic module parsing
        ### This segment should execute only once, until appropriate module definition is found
        ### ****************************************************
        elif regex_name.findall(line) and mode == MODE_GENERICMODULE:
            temp_value = regex_name.findall(line)[0][0]
            temp_value = temp_value.strip()
            temp_value = temp_value.lower()
            if temp_value == "moduleengineconfigs":
                mode = MODE_MODULEENGINECONFIGS
                part = ModuleEngineConfigsClass()
            elif temp_value == "moduleengineignitor":
                mode = MODE_MODULEENGINEIGNITOR
                part = ModuleEngineIgnitorClass()
            elif temp_value == "modulefueltanks":
                mode = MODE_MODULEFUELTANK
                part = ModuleFuelTanksClass()

        ### ****************************************************
        ### ModuleFuelTank
        ### ****************************************************
        # baseMass
        elif regex_basemass.findall(line) and mode == MODE_MODULEFUELTANK:
            temp_value = regex_basemass.findall(line)[0][0]
            part.basemass = int(float(temp_value))

        # volume
        elif regex_volume.findall(line) and mode == MODE_MODULEFUELTANK:
            temp_value = regex_volume.findall(line)[0][0]
            part.volume = int(float(temp_value))

        # amount
        elif regex_amount.findall(line) and mode == MODE_MODULETANKCONTENT:
            temp_value = regex_amount.findall(line)[0]
            part.amount = str(temp_value)

        # maxAmount
        elif regex_maxAmount.findall(line) and mode == MODE_MODULETANKCONTENT:
            temp_value = regex_maxAmount.findall(line)[0][0]
            part.maxAmount = float(temp_value)

        ### ****************************************************
        ### ModuleEngineConfigs
        ### ****************************************************
        # techLevel
        elif regex_techlevel.findall(line) and mode == MODE_MODULEENGINECONFIGS:
            temp_value = regex_techlevel.findall(line)[0][0]
            part.techLevel = int(float(temp_value))

        # origTechLevel
        elif regex_origTechLevel.findall(line) and mode == MODE_MODULEENGINECONFIGS:
            temp_value = regex_origTechLevel.findall(line)[0][0]
            part.origTechLevel = int(float(temp_value))

        # type (type of ModuleEngine section, not engineType!)
        elif (regex_type.findall(line) and
             (mode == MODE_MODULEENGINECONFIGS or mode == MODE_MODULEFUELTANK)):
            temp_value = regex_type.findall(line)[0][0]
            part.type = str(temp_value)

        # engineType
        elif regex_engineType.findall(line) and mode == MODE_MODULEENGINECONFIGS:
            temp_value = regex_engineType.findall(line)[0]
            part.engineType = str(temp_value)

        # origMass
        elif regex_origMass.findall(line) and mode == MODE_MODULEENGINECONFIGS:
            temp_value = regex_origMass.findall(line)[0][0]
            part.origMass = float(temp_value)

        # default configuration
        elif regex_configuration.findall(line) and mode == MODE_MODULEENGINECONFIGS:
            temp_value = regex_configuration.findall(line)[0][0]
            part.defaultConfiguration = str(temp_value)

        # modded flag
        elif regex_modded.findall(line) and mode == MODE_MODULEENGINECONFIGS:
            temp_value = regex_modded.findall(line)[0]
            part.modded = str(temp_value)


        ### ****************************************************
        ### CONFIG
        ### ****************************************************
        # Name
        elif (regex_name.findall(line) and
             (mode == MODE_CONFIG or mode == MODE_MODULETANKCONTENT)):
            temp_value = regex_name.findall(line)[0][0]
            part.name = str(temp_value)

        # maxThrust
        elif regex_maxThrust.findall(line) and mode == MODE_CONFIG:
            temp_value = regex_maxThrust.findall(line)[0][1]
            part.maxThrust = float(temp_value)

        # heatProduction
        elif regex_heatProduction.findall(line) and mode == MODE_CONFIG:
            temp_value = regex_heatProduction.findall(line)[0][1]
            part.heatProduction = float(temp_value)

        # IspSL
        elif regex_IspSL.findall(line) and mode == MODE_CONFIG:
            temp_value = regex_IspSL.findall(line)[0][0]
            part.ispSL = float(temp_value)

        # IspV
        elif regex_IspV.findall(line) and mode == MODE_CONFIG:
            temp_value = regex_IspV.findall(line)[0][0]
            part.ispV = float(temp_value)

        # Throttle
        elif regex_throttle.findall(line) and mode == MODE_CONFIG:
            temp_value = regex_throttle.findall(line)[0][0]
            part.throttle = float(temp_value)

        # thrusterPower
        elif regex_thrusterPower.findall(line) and mode == MODE_CONFIG:
            temp_value = regex_thrusterPower.findall(line)[0][1]
            part.thrusterPower = float(temp_value)

        # Placeholder
        # elif regex_.findall(line) and mode == MODE_:
        #     temp_value = regex_.findall(line)[0][0]
        #     part. = float(temp_value)

        # Diving deeper into the loop
        elif line == "{":
            depth += 1
            tmp_num, subpart, subtype = parcer(input_data[(num):], prev, mode)  # Execute main parcer function for deeper level
            num += tmp_num

            # This will execute AFTER returning from deeper loop
            # It will assign returned object to appropriate property of parent (current) object
            if subtype == MODE_PART: parced.append(subpart)                         # Add current part to general list of parts
            elif subtype == MODE_MODULEENGINES: part.moduleEngine = subpart         # Add returned EngineModule to part
            elif subtype == MODE_MODULERCS: part.moduleRCS = subpart         # Add returned EngineModule to part
            elif subtype == MODE_MODULEENGINEIGNITOR: part.moduleEngineIgnitor = subpart  # Add returned EngineIgnitor to part
            elif subtype == MODE_MODULEENGINE_ATM_CURVE:                            # Add Atmospheric curve settings to EngineModule
                part.atmoCurveKey0 = subpart["key0"]
                part.atmoCurveKey1 = subpart["key1"]
            elif subtype == MODE_PROPELLANT: part.propellants.append(subpart)       # Add propellant to list of propellants
            elif subtype == MODE_MODULEENGINECONFIGS: part.moduleEngineConfigsModule = subpart # Add ModuleEngineConfigs to part
            elif subtype == MODE_CONFIG: part.configurations.append(subpart)        # Add CONFIG to list of configuratons
            elif subtype == MODE_IGNITORRESOURCE: part.ignitorElectricChargeAmount = float(subpart)    # Add electric charge for ignition to ignitor object
            elif subtype == MODE_MODULEFUELTANK: part.moduleFuelTank = subpart      # Add ModuleFuelTank to part
            elif subtype == MODE_MODULETANKCONTENT: part.tanks.append(subpart)      # Add internal tank definition to ModuleFuelTank

        # Raising up (back) from the loop
        elif line == "}":
            depth -= 1
            return num, part, mode

        else:
            pass
        prev = line
        num += 1


# Compiling regex'es for later use
# Names are self-explanatory
regex_part_name = re.compile(r'^@PART\[([a-zA-Z0-9_-]+)\]', re.IGNORECASE)
regex_comment = re.compile(r'^@PART\[\w+\].*//(.*)', re.IGNORECASE)
regex_mass = re.compile(r'^[@|%]mass\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)
regex_cost = re.compile(r'^[@|%]cost\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)
regex_entryCost = re.compile(r'^[@|%]entryCost\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)
regex_maxTemp = re.compile(r'^[@|%]maxTemp\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)

regex_moduleEngines = re.compile(r'^@Module\[ModuleEngine[s|\*]\]', re.IGNORECASE)
regex_moduleRCS = re.compile(r'^@Module\[ModuleRCS\*?\]', re.IGNORECASE)
regex_maxThrust = re.compile(r'^([@|%])?maxThrust\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)
regex_heatProduction = re.compile(r'^([@|%])?heatProduction\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)

regex_atmosphereCurve = re.compile(r'^[@|%]atmosphereCurve$', re.IGNORECASE)
regex_atmosphereCurveKey0 = re.compile(r'^[@|%]key,0\s?=\s?0\s?(\d+(\.\d*)?)', re.IGNORECASE)
regex_atmosphereCurveKey1 = re.compile(r'^[@|%]key,1\s?=\s?1\s?(\d+(\.\d*)?)', re.IGNORECASE)

regex_propellant = re.compile(r'^PROPELLANT$', re.IGNORECASE)
regex_prop_ratio = re.compile(r'^ratio\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)
regex_prop_drawGauge = re.compile(r'^DrawGauge\s?=\s?(True$|False$)', re.IGNORECASE)
regex_prop_flow = re.compile(r'^[@|%](resourceFlowMode|flowMode)\s?=\s(\w+)', re.IGNORECASE)

regex_moduleEngineIgnitor = re.compile(r'^ModuleEngineIgnitor$', re.IGNORECASE)
regex_ignitionsAvailable = re.compile(r'ignitionsAvailable\s?=\s?(\d+?)', re.IGNORECASE)
regex_autoIgnitionTemperature = re.compile(r'autoIgnitionTemperature\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)
regex_useUllageSimulation = re.compile(r'useUllageSimulation\s?=\s(true$|false$)', re.IGNORECASE)
regex_ignitorResource = re.compile(r'^IGNITOR_RESOURCE$', re.IGNORECASE)
regex_ECamount = re.compile(r'^amount\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)

regex_name = re.compile(r'^name\s?=\s?(\w+(\s?\+\s?\w+)?)', re.IGNORECASE)
regex_type = re.compile(r'^type\s?=\s?(\w+(\s?\+\s?\w+)?)', re.IGNORECASE)
regex_module = re.compile(r'^MODULE$', re.IGNORECASE)
regex_config = re.compile(r'^CONFIG$', re.IGNORECASE)
regex_tank = re.compile(r'^TANK$', re.IGNORECASE)

regex_techlevel = re.compile(r'^techLevel\s?=\s?(\d)', re.IGNORECASE)
regex_origTechLevel = re.compile(r'^origTechLevel\s?=\s?(\d)', re.IGNORECASE)
regex_engineType = re.compile(r'^engineType\s?=\s?(.{1,2})', re.IGNORECASE)
regex_origMass = re.compile(r'^origMass\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)
regex_configuration = re.compile(r'^configuration\s?=\s?(\w+(\s?\+\s?\w+)?)', re.IGNORECASE)
regex_thrusterPower = re.compile(r'^([@|%])?thrusterPower\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)
regex_modded = re.compile(r'^modded\s?=\s(true$|false$)', re.IGNORECASE)

regex_IspSL = re.compile(r'^IspSL\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)
regex_IspV = re.compile(r'^IspV\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)
regex_throttle = re.compile(r'^throttle\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)

regex_basemass = re.compile(r'^baseMass\s?=\s?(-?\d+(\.\d*)?)', re.IGNORECASE)
regex_volume = re.compile(r'^volume\s?=\s?(\d+(\.\d*)?)', re.IGNORECASE)
regex_amount = re.compile(r'^amount\s?=\s?(\w+)', re.IGNORECASE)
regex_maxAmount = re.compile(r'^maxAmount\s?=\s?(\d+(\.\d*)?)%$', re.IGNORECASE)


# Parcing arguments here
argParcer = argparse.ArgumentParser(description="Converts data from RealFuels config to ODS file")
argParcer.add_argument('input', type=str, help="Input file in RF config format")
argParcer.add_argument('output', type=str, help="Output file in ODS format")
args = argParcer.parse_args()
cfg_inputfile = args.input
cfg_outputfile = args.output

# Reading raw RF config
with open(cfg_inputfile, "r") as inputfile:
    raw_data = inputfile.readlines()
    for line in raw_data:
        tmp_line = line.strip()
        if tmp_line != "":
            main_data.append(tmp_line)

# Main loop
previous = ""
someNum = parcer(main_data, previous, 0)

# Table header
now = datetime.datetime.now()
toExport.append(["C", "This file is generated by RF_unpacker ver" + __version__])
toExport.append(["C", "Converter is written by " + __author__])
toExport.append(["C", now.strftime("%Y-%m-%d %H:%M")])
toExport.append(["C", "Source file: " + cfg_inputfile])
toExport.append(["C", ""])
toExport.append(["C", "How to use it:"])
toExport.append(["C", "First column is indicator for later parsing"])
toExport.append(["C", " 'H' means header, or comment. This lines will be ignored"])
toExport.append(["C", " 'PRT' means 'PART'. Main part parameters are here"])
toExport.append(["C", " 'ME' = 'ModuleEngine', you don't need to change anything here"])
toExport.append(["C", " 'MRCS' = 'ModuleRCS, same as ModuleEngine"])
toExport.append(["C", " 'ECMH' - Header for ModuleEngineConfigs, with common parameters"])
toExport.append(["C", " 'EC' - Engine configuration"])
toExport.append(["C", " 'PP' - Propellant"])
toExport.append(["C", " 'FT' - Fuel tank"])
toExport.append(["C", " 'FL' - preloaded fuel in fuel tank (rarely used)"])
toExport.append(["C", " '-1' in most parameters mean 'not used'"])
toExport.append(["C", "      only exception is basemass parameter in ModularFuelTanks"])
toExport.append(["C", ""])
toExport.append(["C", ""])
toExport.append(["C", ""])
toExport.append(["C", ""])
toExport.append(["C", ""])
toExport.append(["C", "name", "mass", "cost", "entryCost", "maxTemp", "comment"])


# Creating list to export, line by line
# See functions for this operation in modules classes
for part in parced:
    line = part.exportList()
    for subline in line:
        toExport.append(subline)

# Write data to ODS file
# Make sure that file is not opened
# Note: file will be rewrited!
exportedData = OrderedDict() # from collections import OrderedDict
exportedData.update({"RF_CONFIG": toExport})
pyexcel_ods3.save_data(cfg_outputfile, exportedData)

