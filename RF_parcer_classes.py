"""
Common classes and functions for RF_packer and RF_unpacker
"""
__author__ = 'Snownoise'
__license__ = "GNU GPLv3 "
__version__ = "0.0.1"
__maintainer__ = "Snownoise"
__email__ = "snownoise@gmail.com"

class ModuleEngineIgnitorClass:
    """
    ModuleEngineIgnitor generic configuration class (for engine's default configuration)
    """

    def __init__(self, ignitionsAvailable = -1, autoIgnitionTemperature = -1,
                 useUllageSimulation=False, ignitorType = "Electric", ignitorElectricChargeAmount = -1):
        self.ignitionsAvailable = ignitionsAvailable
        self.autoIgnitionTemperature = autoIgnitionTemperature
        self.useUllageSimulation = useUllageSimulation
        self.ignitorType = ignitorType
        self.ignitorElectricChargeAmount = ignitorElectricChargeAmount

    def __str__(self):
        seq = ("\t *** MODULE_ENGINE_IGNITOR ***",
               "\t\t\tignitionsAvailable = " + str(self.ignitionsAvailable),
               "\t\t\tautoIgnitionTemperature = " + str(self.autoIgnitionTemperature),
               "\t\t\tuseUllageSimulation = " + str(self.useUllageSimulation),
               "\t\t\tignitorType = " + str(self.ignitorType),
               "\t\t\tignitorElectricChargeAmount = " + str(self.ignitorElectricChargeAmount))

        return '\n'.join(seq)

    def export2CFG(self):
        """
        Will write part's data in KSP/RF standart configuration patch format
        """
        cfgData = [
            "ModuleEngineIgnitor",
            "{",
            "  ignitionsAvailable = " + str(self.ignitionsAvailable)]
        if str(self.useUllageSimulation).lower() == "false":
            cfgData.append("  useUllageSimulation = False")
        else:
            cfgData.append("  useUllageSimulation = True")
        if self.autoIgnitionTemperature != -1:
            cfgData.append("  autoIgnitionTemperature = " + str(self.autoIgnitionTemperature))
        cfgData.append("  ignitorType = " + str(self.ignitorType))
        if self.ignitorElectricChargeAmount != -1:
            cfgData.extend([
                "  IGNITOR_RESOURCE",
                "  {",
                "    name = ElectricCharge",
                "    amount = " + str(self.ignitorElectricChargeAmount),
                "  }"])

        cfgData.append("}")
        return cfgData


class ModuleFuelTanksClass:
    """
    RealFuels ModuleFuelTanks configuration class
    """

    def __init__(self, basemass = -1024, volume = -1, type = "Default"):
        self.basemass = basemass   # I usually use -1 to signal that parameter is absent in config, but in this case -1 is an actual parameter used by RF
        self.volume = volume
        self.type = type
        self.tanks = []

    def __str__(self):
        seq = ["\t *** MODULE_FUEL_TANKS ***",
               "\t\tbasemass = " + str(self.basemass),
               "\t\tvolume = " + str(self.volume),
               "\t\ttype = " + str(self.type)]
        for tank in self.tanks:
            seq.append(str(tank))
        return '\n'.join(seq)

    def export2CFG(self):
        """
        Will write part's data in KSP/RF standart configuration patch format
        """
        cfgData = [
            "MODULE",
            "{",
            "  name = ModuleFuelTanks",
            "  type = " + str(self.type)]
        if self.basemass != -1024: cfgData.append("  basemass = " + str(self.basemass))
        if self.volume != -1: cfgData.append("  volume = " + str(self.volume))
        if self.tanks:
            for tank in self.tanks:
                append2cfg(cfgData, tank)
        cfgData.append("}")
        return cfgData

    def export2ODS(self):
        # Export all data in formatted list
        data = [["FT","","Fuel tank",
                 "Basemass",self.basemass,
                 "Volume",self.volume,
                 "Tank type",self.type]]
        for tank in self.tanks:
            line = ["FL","","","",
                    "Name>",tank.name,
                    "Amount>",tank.amount,
                    "maxAmount>",tank.maxAmount]
            data.append(line)
        return data


class ModuleFuelTankInternal:
    """
    Definition for internal 'TANK' submodule in ModuleFuelTanks
    """

    def __init__(self, name = "", amount = "", maxAmount = 0.0):
        self.name = name
        self.amount = amount
        self.maxAmount = maxAmount    # This is percentage! % sign should be added to final config

    def __str__(self):
        seq = ("\t\t\tname = " + str(self.name),
               "\t\t\tamount = " + str(self.amount),
               "\t\t\tmaxAmount = " + str(self.maxAmount))
        return '\n'.join(seq)

    def export2CFG(self):
        """
        Will write part's data in KSP/RF standart configuration patch format
        """
        cfgData = [
            "TANK",
            "{",
            "  name = " + str(self.name),
            "  amount = " + str(self.amount),
            "  maxAmount = " + str(self.maxAmount) + "%",
            "}"]
        return cfgData


class ModuleEngineClass:
    """
    RealFuels ModuleEngine / ModuleEngineRF configuration class
    """

    def __init__(self, maxThrust = -1.0, heatProduction = -1,
                 atmoCurveKey0 = -1, atmoCurveKey1 = -1):
        self.maxThrust = maxThrust
        self.heatProduction = heatProduction
        self.atmoCurveKey0 = atmoCurveKey0
        self.atmoCurveKey1 = atmoCurveKey1
        self.propellants = []


    def export2CFG(self):
        """
        Will write part's data in KSP/RF standart configuration patch format
        """
        cfgData = [
            " ",
            "@MODULE[ModuleEngine*]",
            "{",
            "  @name = ModuleEnginesRF"]
        if self.maxThrust != -1: cfgData.append("  @maxThrust = " + str(self.maxThrust))
        if self.heatProduction != -1: cfgData.append("  @heatProduction = " + str(self.heatProduction))
        cfgData.extend([
            "  @atmosphereCurve",
            "  {",
            "    @key,0 = 0 " + str(self.atmoCurveKey0),
            "    @key,1 = 1 " + str(self.atmoCurveKey1),
            "  }"])
        if self.propellants:
            cfgData.extend([
            "  !PROPELLANT[LiquidFuel] {}",
            "  !PROPELLANT[Oxidizer] {}",
            "  !PROPELLANT[MonoPropellant] {}"])
            for propellant in self.propellants:
                append2cfg(cfgData, propellant)
        cfgData.append("}")

        return cfgData

    def __str__(self):
        seq = ["\t *** MODULE_ENGINE_RF ***",
               "\t\tmaxThrust = " + str(self.maxThrust),
               "\t\theatProduction = " + str(self.heatProduction),
               "\t\t\tkey0 = " + str(self.atmoCurveKey0),
               "\t\t\tkey1 = " + str(self.atmoCurveKey1)]
        for propellant in self.propellants:
            seq.append(str(propellant))
        return '\n'.join(seq)


class PropellantClass:
    """
    RealFuels propellant class
    """

    def __init__(self, name = "none", ratio = -1.0, drawGauge = False, flowMode = "none"):
        self.name = name
        self.ratio = ratio
        self.drawGauge = drawGauge
        self.flowMode = flowMode

    def __str__(self):
        seq = ("\t\t *** PROPELLANT ***",
               "\t\t\t\tname = " + str(self.name),
               "\t\t\t\tratio = " + str(self.ratio),
               "\t\t\t\tdrawGauge = " + str(self.drawGauge),
               "\t\t\t\tflowMode = " + str(self.flowMode))
        return '\n'.join(seq)

    def export2ODS(self):
        # Export all data in formatted list
        data = ["PP","","","","Propellant>",
                self.name,
                self.ratio,
                "Draw gauge>", self.drawGauge,
                "Flow>", self.flowMode]
        return data

    def export2CFG(self):
        """
        Will write part's data in KSP/RF standart configuration patch format
        """
        cfgData = [
            "PROPELLANT",
            "{",
            "  name = " + self.name,
            "  ratio = " + str(self.ratio)]

        if str(self.drawGauge).lower() == "true": cfgData.append("  DrawGauge = True")
        if self.flowMode != "none": cfgData.append("  %resourceFlowMode = " + self.flowMode)
        cfgData.append("}")
        return cfgData


class ModuleRCSClass:
    """
    Modification of stock Squad ModuleRCS in configs
    """

    def __init__(self, thrusterPower = -1.0, heatProduction = -1,
                 atmoCurveKey0 = -1, atmoCurveKey1 = -1):
        self.thrusterPower = thrusterPower
        self.heatProduction = heatProduction
        self.atmoCurveKey0 = atmoCurveKey0
        self.atmoCurveKey1 = atmoCurveKey1
        self.propellants = []

    def export2CFG(self):
        """
        Will write part's data in KSP/RF standart configuration patch format
        """
        cfgData = [
            " ",
            "@MODULE[ModuleRCS*]",
            "{"]
        if self.thrusterPower != -1: cfgData.append("  @thrusterPower = " + str(self.thrusterPower))
        if self.heatProduction != -1: cfgData.append("  @heatProduction = " + str(self.heatProduction))
        cfgData.extend([
            "  @atmosphereCurve",
            "  {",
            "    @key,0 = 0 " + str(self.atmoCurveKey0),
            "    @key,1 = 1 " + str(self.atmoCurveKey1),
            "  }"])
        if self.propellants:
            cfgData.extend([
            "  !PROPELLANT[LiquidFuel] {}",
            "  !PROPELLANT[Oxidizer] {}",
            "  !PROPELLANT[MonoPropellant] {}"])
            for propellant in self.propellants:
                propellantData = propellant.export2CFG()
                for item in propellantData:
                    cfgData.append("  " + item)
        cfgData.append("}")

        return cfgData

    def __str__(self):
        seq = ["\t *** MODULE_RCS ***",
               "\t\tthrusterPower = " + str(self.thrusterPower),
               "\t\theatProduction = " + str(self.heatProduction),
               "\t\t\tkey0 = " + str(self.atmoCurveKey0),
               "\t\t\tkey1 = " + str(self.atmoCurveKey1)]
        for propellant in self.propellants: seq.append(str(propellant))
        return '\n'.join(seq)


class ModuleEngineConfigsClass:
    """
    RealFuels ModuleEngineConfigs class definition
    """

    def __init__(self, type = "ModuleEnginesRF", techLevel = -1, origTechLevel = -1, engineType = "None",
                 origMass = -1.0, modded = False, defaultConfiguration = "None"):
        self.techLevel = techLevel
        self.origTechLevel = origTechLevel
        self.type = type
        self.engineType = engineType
        self.origMass = origMass
        self.defaultConfiguration = defaultConfiguration
        self.modded = modded
        self.configurations = []

    def __str__(self):
        seq = ["\t *** MODULE_ENGINE_CONFIGS ***",
               "\t\ttechLevel = " + str(self.techLevel),
               "\t\torigTechLevel = " + str(self.origTechLevel),
               "\t\ttype = " + str(self.type),
               "\t\tengineType = " + str(self.engineType),
               "\t\torigMass = " + str(self.origMass),
               "\t\tdefaultConfiguration = " + str(self.defaultConfiguration),
               "\t\tmodded = " + str(self.modded)]
        for configuration in self.configurations:
            seq.append(str(configuration))
        return '\n'.join(seq)

    def export2ODS(self):
        # Export all data in formatted list
        data = [["ECMH","",
                 self.type,
                 "Tech level>", self.techLevel,
                 "Orig techlevel>", self.origTechLevel,
                 "Engine type>", self.engineType,
                 "Orig mass>", self.origMass,
                 "Modded>", self.modded,
                 "Def.config>", self.defaultConfiguration],
                ["C","","","Config Name", "Max thrust", "Heat prod", "IspSL", "IspV", "Thruster power", "Throttle",
                 "Ignitions", "Ullage", "Pressure fed", "Ignitor resource", "Ignitor amount"]]

        for configuration in self.configurations:
            tmpData = configuration.export2ODS()
            for line in tmpData:
                data.append(line)

        return data

    def export2CFG(self):
        """
        Will write part's data in KSP/RF standart configuration patch format
        """
        cfgData = [
            " ","MODULE",
            "{",
            "  name = ModuleEngineConfigs",
            "  type = " + str(self.type)]

        if self.techLevel != -1: cfgData.append("  techLevel = " + str(self.techLevel))
        if self.origTechLevel != -1: cfgData.append("  origTechLevel = " + str(self.origTechLevel))
        if self.engineType != "": cfgData.append("  engineType = " + self.engineType)
        if self.origMass != -1: cfgData.append("  origMass = " + str(self.origMass))
        if self.defaultConfiguration != "": cfgData.append("  configuration = " + self.defaultConfiguration)
        if self.modded != "": cfgData.append("  modded = " + str(self.modded))

        for configuration in self.configurations:
            append2cfg(cfgData, configuration)

        cfgData.append("}")
        return cfgData

class EngineConfigClass():
    """
    Engine config (CONFIG module) class
    """

    def __init__(self, name = "none", maxThrust = -1.0, heatProduction = -1, ispSL = -1.0, ispV = -1.0,
                 throttle = -1, thrusterPower = -1, ignitions = -1, ullage = True, pressureFed = False,
                 ignitorResource = "None", ignitorAmount = -1):
        self.name = name
        self.maxThrust = maxThrust
        self.heatProduction = heatProduction
        self.ispSL = ispSL
        self.ispV = ispV
        self.throttle = throttle
        self.thrusterPower = thrusterPower
        self.propellants = []
        self.ignitions = ignitions
        self.ullage = ullage
        self.pressureFed = pressureFed
        self.ignitorResource = ignitorResource
        self.ignitorAmount = ignitorAmount
        self.moduleEngineIgnitor = None

    def __str__(self):
        seq = ["\t *** ENGINE CONFIG ***",
               "\t\t\tName = " + str(self.name),
               "\t\t\tmaxThrust = " + str(self.maxThrust),
               "\t\t\theatProduction = " + str(self.heatProduction),
               "\t\t\tIspSL = " + str(self.ispSL),
               "\t\t\tIspV = " + str(self.ispV),
               "\t\t\tthrusterPower = " + str(self.thrusterPower),
               "\t\t\tthrottle = " + str(self.throttle),
               "\t\t\tignitions = " + str(self.ignitions),
               "\t\t\tullage = " + str(self.ullage),
               "\t\t\tpressureFed = " + str(self.pressureFed),
               "\t\t\t\tignitorResource = " + str(self.ignitorResource),
               "\t\t\t\tamount = " + str(self.ignitorAmount)]

        for propellant in self.propellants:
            seq.append(str(propellant))
        if self.moduleEngineIgnitor: seq.append(str(self.moduleEngineIgnitor))
        return '\n'.join(seq)

    def export2ODS(self):
        # Export all data in formatted list
        tmpData = ["EC","","",
                 self.name,
                 self.maxThrust,
                 self.heatProduction,
                 self.ispSL,
                 self.ispV,
                 self.thrusterPower,
                 self.throttle]

        # Add ignitor's parameters to config line
        if self.moduleEngineIgnitor:
            tmpData.append(self.moduleEngineIgnitor.ignitionsAvailable)
            tmpData.append(self.moduleEngineIgnitor.useUllageSimulation)
            tmpData.append("False")
            tmpData.append(self.moduleEngineIgnitor.ignitorType)
            tmpData.append(self.moduleEngineIgnitor.ignitorElectricChargeAmount)
        else:
            tmpData.extend([
                self.ignitions,
                self.ullage,
                self.pressureFed,
                self.ignitorResource,
                self.ignitorAmount])


        data = []
        data.append(tmpData)

        # Add propellants, in separate lines
        for propellant in self.propellants:
            data.append(propellant.export2ODS())
        return data

    def export2CFG(self):
        """
        Will write part's data in KSP/RF standart configuration patch format
        """
        cfgData = [
            " ","CONFIG",
            "{",
            "  name = " + self.name]
        if self.maxThrust != -1: cfgData.append("  maxThrust = " + str(self.maxThrust))
        if self.thrusterPower != -1: cfgData.append("  thrusterPower = " + str(self.thrusterPower))
        if self.heatProduction != -1: cfgData.append("  heatProduction = " + str(self.heatProduction))
        if self.propellants:
            for propellant in self.propellants:
                append2cfg(cfgData, propellant)
        if self.ispSL != -1: cfgData.append("  IspSL = " + str(self.ispSL))
        if self.ispV != -1: cfgData.append("  IspV = " + str(self.ispV))
        if self.throttle != -1: cfgData.append("  throttle = " + str(self.throttle))
        if self.ignitions != -1:
            cfgData.append("  ignitions = " + str(self.ignitions))
            if str(self.ullage).lower() == "true":
                cfgData.append("  ullage = True")
            else:
                cfgData.append("  ullage = False")
            if str(self.pressureFed).lower() == "true":
                cfgData.append("  pressureFed = True")
            else:
                cfgData.append("  pressureFed = False")
            if self.ignitorAmount != -1:
                cfgData.extend([
                    "  IGNITOR_RESOURCE",
                    "  {",
                    "    name = " + self.ignitorResource,
                    "    amount = " + str(self.ignitorAmount),
                    "  }"])

        # if self.moduleEngineIgnitor: append2cfg(cfgData, self.moduleEngineIgnitor)


        cfgData.append("}")
        return cfgData


class PartClass:
    """
    Main class for generic parts
    """

    def __init__(self, name = "none", comment = "", mass = -1, cost = -1, entryCost = -1, maxTemp = -1,
                 ignitions = -1, ullage = True, pressureFed = False):
        self.name = name
        self.comment = comment
        self.mass = mass
        self.cost = cost
        self.entryCost = entryCost
        self.maxTemp = maxTemp
        self.ignitions = ignitions
        self.ullage = ullage
        self.pressureFed = pressureFed
        self.ignitorResource = "none"
        self.ignitorAmount = -1
        self.moduleEngine = None
        self.moduleRCS = None
        self.moduleEngineConfigsModule = None
        self.moduleEngineIgnitor = None
        self.moduleFuelTank = None

    def __str__(self):
        seq = ["\n\n*** PART PART PART ***",
               "name = " + str(self.name),
               "\tcomment = " + str(self.comment),
               "\tmass = " + str(self.mass),
               "\tcost = " + str(self.cost),
               "\tentryCost = " + str(self.entryCost),
               "\tmaxTemp = " + str(self.maxTemp),
               "\tignitions = " + str(self.ignitions),
               "\tullage = " + str(self.ullage),
               "\tpressureFed = " + str(self.pressureFed)]
        if self.moduleEngine: seq.append(str(self.moduleEngine))
        if self.moduleRCS: seq.append(str(self.moduleRCS))
        if self.moduleEngineConfigsModule: seq.append(str(self.moduleEngineConfigsModule))
        if self.moduleEngineIgnitor: seq.append(str(self.moduleEngineIgnitor))
        if self.moduleFuelTank: seq.append(str(self.moduleFuelTank))

        return '\n'.join(seq)

    def export2CFG(self):
        """
        Will write part's data in KSP/RF standart configuration patch format
        """
        cfgData = ["@PART[" + self.name + "]:FOR[RealFuels] // " + self.comment, "{"]
        if self.mass != -1: cfgData.append("  @mass = " + str(self.mass))
        if self.cost != -1: cfgData.append("  @cost = " + str(self.cost))
        if self.entryCost != -1: cfgData.append("  %entryCost = " + str(self.entryCost))
        if self.maxTemp != -1: cfgData.append("  @maxTemp = " + str(self.maxTemp))

        if self.moduleEngine: append2cfg(cfgData, self.moduleEngine)
        if self.moduleRCS: append2cfg(cfgData, self.moduleRCS)
        if self.moduleEngineConfigsModule: append2cfg(cfgData, self.moduleEngineConfigsModule)
        if self.ignitions != -1:
            cfgData.append("  ignitions = " + str(self.ignitions))
            if str(self.ullage).lower() == "true":
                cfgData.append("  ullage = True")
            else:
                cfgData.append("  ullage = False")
            if str(self.pressureFed).lower() == "true":
                cfgData.append("  pressureFed = True")
            else:
                cfgData.append("  pressureFed = False")
            if self.ignitorAmount != -1:
                cfgData.extend([
                    "  IGNITOR_RESOURCE",
                    "  {",
                    "    name = " + self.ignitorResource,
                    "    amount = " + str(self.ignitorAmount),
                    "  }"])
        # if self.moduleEngineIgnitor:
        #     cfgData.append("  !MODULE[ModuleEngineIgnitor] {}")
        #     append2cfg(cfgData, self.moduleEngineIgnitor)
        if self.moduleFuelTank:
            cfgData.extend([" ",
            "  !RESOURCE[LiquidFuel] {}",
            "  !RESOURCE[Oxidizer] {}",
            "  !RESOURCE[MonoPropellant] {}",
            "  !RESOURCE[SolidFuel] {}",
            "  !RESOURCE[XenonGas] {}"])
            append2cfg(cfgData, self.moduleFuelTank)

        cfgData.append("}")
        cfgData.append("")
        cfgData.append("")
        return cfgData


    def export2ODS(self):
        # Export all data in formatted list
        # This is main parameters of the part
        data = [["P",
                self.name,
                self.mass,
                self.cost,
                self.entryCost,
                self.maxTemp,
                self.comment]]

        # One line for moduleEngine
        if self.moduleEngine:
            tmpLine = ["ME", "", "", "",
                       "AtmCurve0>",self.moduleEngine.atmoCurveKey0,
                       "AtmCurve1>",self.moduleEngine.atmoCurveKey1]
            data.append(tmpLine)

        # One line for moduleRCS
        if self.moduleRCS:
            tmpLine = ["MRCS", "", "", "",
                       "AtmCurve0>", self.moduleRCS.atmoCurveKey0,
                       "AtmCurve1>", self.moduleRCS.atmoCurveKey1]
            data.append(tmpLine)

        # Many lines for all engine configurations
        if self.moduleEngineConfigsModule:
            tmpLines = self.moduleEngineConfigsModule.export2ODS()
            for line in tmpLines:
                data.append(line)

        # ModuleFuelTanks here
        if self.moduleFuelTank:
            tmpLines = self.moduleFuelTank.export2ODS()
            for line in tmpLines:
                data.append(line)

        # This lines are kust delimiters for better readability
        data.append(["C"])
        data.append(["C"])

        return data

def append2cfg(exportList, object):
    """
    This function is adding data from nested object (with export2CFG function) to selected list
    :param exportList:
    :param object:
    :return:
    """
    moduleData = object.export2CFG()
    for item in moduleData:
        exportList.append("  " + item)