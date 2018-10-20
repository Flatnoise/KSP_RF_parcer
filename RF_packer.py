"""
This is a simple parcer
It converts specially prepared (by RF_unpacker) ODS table to RealFuels config file
"""

__author__ = 'Snownoise'
__license__ = "GNU GPLv3 "
__version__ = "0.0.1"
__maintainer__ = "Snownoise"
__email__ = "snownoise@gmail.com"

import re
import datetime
import argparse
import pyexcel_ods3
import json
from collections import OrderedDict
from RF_parcer_classes import *


def partException(part, lineNumber):
    """
    # Raise exeption if part is not present
    :param part: 
    :param lineNumber: 
    :return: 
    """
    if part == None: raise Exception("No part for ModuleEngine in line " + str(lineNumber))


# Init and config variables
cfg_inputfile = ""
cfg_outputfile = ""
parced = []

# Parcing arguments here
argParcer = argparse.ArgumentParser(description="Converts data from RealFuels config to ODS file")
argParcer.add_argument('input', type=str, help="Input file in RF config format")
argParcer.add_argument('output', type=str, help="Output file in ODS format")
args = argParcer.parse_args()
cfg_inputfile = args.input
cfg_outputfile = args.output

# Importing data from ODS using pyExcel
importedData = pyexcel_ods3.get_data(cfg_inputfile)
importedData = importedData['RF_CONFIG']

# Main loop. Looping throught all data
lineCount = 0
part = None
engineConfigs = None
engineConfig = None
fuelTank = None

for line in importedData:
    lineCount += 1
    if line[0] == 'C': continue     # Dropping off comments

    # Part import
    elif line[0] == 'P':
        # Raise exeption of line length is wrong
        if len(line) != 6 and len(line) != 7: raise Exception("Syntax error/Wrong length in line " + str(lineCount))

        # Check if previous part exist; If yes, write previous part and its subcomponents to the list of parts
        if part:
            if engineConfig:
                engineConfigs.append(engineConfig)
            if engineConfigs:
                part.moduleEngineConfigsModule.configurations = engineConfigs
            if fuelTank:
                part.moduleFuelTank = fuelTank
            parced.append(part)

        # Clear objects from previous iteration
        engineConfigs = None
        engineConfig = None
        propellant = None
        fuelTank = None

        # Creating values from table string
        partName = line[1]
        partMass = line[2]
        partCost = line[3]
        partEntryCost = line[4]
        partMaxTemp = line[5]
        if len(line) == 7:
            partComment = line[6]
        else:
            partComment = ""

        part = PartClass(partName, partComment, partMass, partCost, partEntryCost, partMaxTemp)


    # ModuleEngine / ModuleEngineRF
    elif line[0] == 'ME':
        partException(part, lineCount)  # Raise exeption if part is not present
        # Raise exeption of line length is wrong
        if len(line) != 8: raise Exception("Syntax error/Wrong length in line " + str(lineCount))

        moduleEngineRF = ModuleEngineClass(atmoCurveKey0 = line[5], atmoCurveKey1 = line[7])
        part.moduleEngine = moduleEngineRF

    # ModuleRCS
    elif line[0] == 'MRCS':
        partException(part, lineCount)  # Raise exeption if part is not present
        # Raise exeption of line length is wrong
        if len(line) != 8: raise Exception("Syntax error/Wrong length in line " + str(lineCount))

        moduleRCS = ModuleRCSClass(atmoCurveKey0 = line[5], atmoCurveKey1 = line[7])
        part.moduleRCS = moduleRCS

    # ModuleEngineConfig, common parameters
    elif line[0] == 'ECMH':
        partException(part, lineCount)  # Raise exeption if part is not present
        # Raise exeption of line length is wrong
        if len(line) != 15: raise Exception("Syntax error/Wrong length in line " + str(lineCount))

        # Creating values from table string
        type = line[2]
        techLevel = line[4]
        origTechLevel = line[6]
        engineType = line[8]
        origMass = line[10]
        defaultConfig = line[14]

        # Special case filtering for boolean value of "Modded"
        tmp = line[12]
        tmp = tmp.lower()
        modded = False
        if tmp == "true": modded = True

        meCommonConfig = ModuleEngineConfigsClass(type, techLevel, origTechLevel, engineType,
                                                  origMass, modded, defaultConfig)
        part.moduleEngineConfigsModule = meCommonConfig
        engineConfigs = []  # Temporary list of engine configuration

    # Engine configuration
    elif line[0] == 'EC':
        lenL = len(line)
        partException(part, lineCount)  # Raise exeption if part is not present
        # Raise exeption of line length is wrong
        if lenL != 15 and lenL != 10: raise Exception("Syntax error/Wrong length in line " + str(lineCount))

        if engineConfig: engineConfigs.append(engineConfig)

        # Creating values from table string
        name = line[3]
        maxThrust = line[4]
        heatProduction = line[5]
        ispSL = line[6]
        ispV = line[7]
        thrusterPower = line[8]
        throttle = line[9]

        engineConfig = EngineConfigClass(name, maxThrust, heatProduction, ispSL, ispV, throttle, thrusterPower)

        # Create values for ModuleEngineIgnitor if present
        if lenL == 15:
            engineConfig.ignitions = line[10]
            engineConfig.ignitorResource = line[13]
            engineConfig.ignitorAmount = line[14]

            # Special case filtering for boolean value of "ullage"
            tmp = str(line[11])
            tmp = tmp.lower()
            engineConfig.ullage = True
            if tmp == "false": engineConfig.ullage = False

            # Special case filtering for boolean value of "pressureFed"
            tmp = str(line[12])
            tmp = tmp.lower()
            engineConfig.pressureFed = False
            if tmp == "true": engineConfig.pressureFed = True

    # Propellant
    elif line[0] == 'PP':
        partException(part, lineCount)  # Raise exeption if part is not present
        # Raise exeption of line length is wrong
        if len(line) != 11: raise Exception("Syntax error/Wrong length in line " + str(lineCount))

        # Creating values from table string
        name = line[5]
        ratio = line[6]
        drawGauge = line[8]
        flowMode = line[10]

        propellant = PropellantClass(name, ratio, drawGauge, flowMode)
        engineConfig.propellants.append(propellant)

    # Fuel tank
    elif line[0] == 'FT':
        partException(part, lineCount)  # Raise exeption if part is not present
        # Raise exeption of line length is wrong
        if len(line) != 9: raise Exception("Syntax error/Wrong length in line " + str(lineCount))

        # Creating values from table string
        basemass = line[4]
        volume = line[6]
        type = line[8]

        fuelTank = ModuleFuelTanksClass(basemass, volume, type)

    # Preloaded fuel in fuel tank
    elif line[0] == 'FL':
        partException(part, lineCount)  # Raise exeption if part is not present
        # Raise exeption of line length is wrong
        if len(line) != 10: raise Exception("Syntax error/Wrong length in line " + str(lineCount))

        if fuelTank:
            # Creating values from table string
            name = line[5]
            amount = line[7]
            maxAmount = line[9]

            tankContent = ModuleFuelTankInternal(name, amount, maxAmount)
            fuelTank.tanks.append(tankContent)

        else:
            raise Exception("Syntax error/No fuel tank in line " + str(lineCount))





# Writing last part to the list of parts
if engineConfigs:
    if engineConfig:
        engineConfigs.append(engineConfig)
    part.moduleEngineConfigsModule.configurations = engineConfigs

if fuelTank:
    part.moduleFuelTank = fuelTank
parced.append(part)



# Append some data to default engine module from list of configurations
for item in parced:
    if item.moduleEngine and item.moduleEngineConfigsModule:
        defaultConfig = item.moduleEngineConfigsModule.defaultConfiguration

        # This loop will find a default config name and adds data from this config to main ModuleEngine block
        for config in item.moduleEngineConfigsModule.configurations:
            if config.name == defaultConfig:
                item.moduleEngine.maxThrust = config.maxThrust
                item.moduleEngine.heatProduction = config.heatProduction

                # If engineIgnitor is present in config, append it to the main part
                if config.moduleEngineIgnitor:
                    item.moduleEngineIgnitor = config.moduleEngineIgnitor

                # If engine ingition parameters are added outside of moduleEngineIgnitor
                if config.ignitions != -1:
                    item.ignitions = config.ignitions
                    item.ullage = config.ullage
                    item.pressureFed = config.pressureFed
                    if config.ignitorAmount != -1:
                        item.ignitorResource = config.ignitorResource
                        item.ignitorAmount = config.ignitorAmount

                # If propellans are present in config, append it to the main part
                if config.propellants:
                    item.moduleEngine.propellants = config.propellants


    elif item.moduleRCS and item.moduleEngineConfigsModule:
        defaultConfig = item.moduleEngineConfigsModule.defaultConfiguration

        # This loop will find a default config name and adds data from this config to main ModuleEngine block
        for config in item.moduleEngineConfigsModule.configurations:
            if config.name == defaultConfig:
                item.moduleRCS.thrusterPower = config.thrusterPower
                item.moduleRCS.heatProduction = config.heatProduction

                # If propellans are present in config, append it to the main part
                if config.propellants:
                    item.moduleRCS.propellants = config.propellants


# Writing RF config
with open(cfg_outputfile, "w") as outputfile:
    for item in parced:
        cfgText = item.export2CFG()
        for line in cfgText:
            # print (line)
            outputfile.write(line + "\n")
