class ModuleEngineIgnitorClass:
    """
    ModuleEngineIgnitor generic configuration class (for engine's default configuration)
    """

    def __init__(self):
        self.ignitionsAvailable = -1
        self.autoIgnitionTemperature = -1
        self.useUllageSimulation = False
        self.ignitorType = "Electric"
        self.ignitorElectricChargeAmount = -1

    def __str__(self):
        seq = ("\t *** MODULE_ENGINE_IGNITOR ***",
               "\t\t\tignitionsAvailable = " + str(self.ignitionsAvailable),
               "\t\t\tautoIgnitionTemperature = " + str(self.autoIgnitionTemperature),
               "\t\t\tuseUllageSimulation = " + str(self.useUllageSimulation),
               "\t\t\tignitorType = " + str(self.ignitorType),
               "\t\t\tignitorElectricChargeAmount = " + str(self.ignitorElectricChargeAmount))

        return '\n'.join(seq)


class ModuleFuelTanksClass:
    """
    RealFuels ModuleFuelTanks configuration class
    """

    def __init__(self):
        self.basemass = -1024   # I usually use -1 to signal that parameter is absent in config, but in this case -1 is an actual parameter used by RF
        self.volume = -1
        self.type = "Default"
        self.tanks = []

    def __str__(self):
        seq = ["\t *** MODULE_FUEL_TANKS ***",
               "\t\tbasemass = " + str(self.basemass),
               "\t\tvolume = " + str(self.volume),
               "\t\ttype = " + str(self.type)]
        for tank in self.tanks:
            seq.append(str(tank))
        return '\n'.join(seq)

    def exportList(self):
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

    def __init__(self):
        self.name = ""
        self.amount = ""
        self.maxAmount = 0.0    # This is percentage! % sign should be added to final config

    def __str__(self):
        seq = ("\t\t\tname = " + str(self.name),
               "\t\t\tamount = " + str(self.amount),
               "\t\t\tmaxAmount = " + str(self.maxAmount))
        return '\n'.join(seq)


class ModuleEngineClass:
    """
    RealFuels ModuleEngine / ModuleEngineRF configuration class
    """

    def __init__(self):
        self.maxThrust = -1
        self.heatProduction = -1
        self.atmoCurveKey0 = -1
        self.atmoCurveKey1 = -1
        self.propellants = []


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

    def __init__(self):
        self.name = "none"
        self.ratio = -1.0
        self.drawGauge = False
        self.flowMode = "none"

    def __str__(self):
        seq = ("\t\t *** PROPELLANT ***",
               "\t\t\t\tname = " + str(self.name),
               "\t\t\t\tratio = " + str(self.ratio),
               "\t\t\t\tdrawGauge = " + str(self.drawGauge),
               "\t\t\t\tflowMode = " + str(self.flowMode))
        return '\n'.join(seq)

    def exportList(self):
        # Export all data in formatted list
        data = ["PP","","","","Propellant>",
                self.name,
                self.ratio,
                "Draw gauge>", self.drawGauge,
                "Flow>", self.flowMode]
        return data


class ModuleRCSClass:
    """
    Modification of stock Squad ModuleRCS in configs
    """

    def __init__(self):
        self.thrusterPower = -1
        self.heatProduction = -1
        self.atmoCurveKey0 = -1
        self.atmoCurveKey1 = -1
        self.propellants = []


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

    def __init__(self):
        self.techLevel = -1
        self.origTechLevel = -1
        self.type = "ModuleEnginesRF"
        self.engineType = "None"
        self.origMass = -1.0
        self.defaultConfiguration = "None"
        self.modded = False
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

    def exportList(self):
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
                 "Ignitions", "AutoIgnitionTemp", "Ullage", "Ignitor", "Electr. to ignite"]]

        for configuration in self.configurations:
            tmpData = configuration.exportList()
            for line in tmpData:
                data.append(line)

        return data

class EngineConfigClass():
    """
    Engine config (CONFIG module) class
    """

    def __init__(self):
        self.name = "none"
        self.maxThrust = -1.0
        self.heatProduction = False
        self.ispSL = -1.0
        self.ispV = -1.0
        self.throttle = -1
        self.thrusterPower = -1
        self.propellants = []
        self.moduleEngineIgnitor = None

    def __str__(self):
        seq = ["\t *** ENGINE CONFIG ***",
               "\t\t\tName = " + str(self.name),
               "\t\t\tmaxThrust = " + str(self.maxThrust),
               "\t\t\theatProduction = " + str(self.heatProduction),
               "\t\t\tIspSL = " + str(self.ispSL),
               "\t\t\tIspV = " + str(self.ispV),
               "\t\t\tthrusterPower = " + str(self.thrusterPower),
               "\t\t\tthrottle = " + str(self.throttle)]
        for propellant in self.propellants:
            seq.append(str(propellant))
        if self.moduleEngineIgnitor: seq.append(str(self.moduleEngineIgnitor))
        return '\n'.join(seq)

    def exportList(self):
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
            tmpData.append(self.moduleEngineIgnitor.autoIgnitionTemperature)
            tmpData.append(self.moduleEngineIgnitor.useUllageSimulation)
            tmpData.append(self.moduleEngineIgnitor.ignitorType)
            tmpData.append(self.moduleEngineIgnitor.ignitorElectricChargeAmount)

        data = []
        data.append(tmpData)

        # Add propellants, in separate lines
        for propellant in self.propellants:
            data.append(propellant.exportList())
        return data

class PartClass:
    """
    Main class for generic parts
    """

    def __init__(self, name = "none", comment = "", mass = -1, cost = -1, entryCost = -1, maxTemp = -1):
        self.name = name
        self.comment = comment
        self.mass = mass
        self.cost = cost
        self.entryCost = entryCost
        self.maxTemp = maxTemp
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
               "\tmaxTemp = " + str(self.maxTemp)]
        if self.moduleEngine: seq.append(str(self.moduleEngine))
        if self.moduleRCS: seq.append(str(self.moduleRCS))
        if self.moduleEngineConfigsModule: seq.append(str(self.moduleEngineConfigsModule))
        if self.moduleEngineIgnitor: seq.append(str(self.moduleEngineIgnitor))
        if self.moduleFuelTank: seq.append(str(self.moduleFuelTank))
        return '\n'.join(seq)

    def exportList(self):
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
            tmpLines = self.moduleEngineConfigsModule.exportList()
            for line in tmpLines:
                data.append(line)

        # ModuleFuelTanks here
        if self.moduleFuelTank:
            tmpLines = self.moduleFuelTank.exportList()
            for line in tmpLines:
                data.append(line)

        # This lines are kust delimiters for better readability
        data.append(["C"])
        data.append(["C"])

        return data
