# KSP_RF_parcer

Simple converter for KSP-specific RealFuel patches (.cfg)
Converts to/from ODS LibreOffice tables.

Written to simplify editing of RealFuels patches - It's to easy to make an error while editing standart KSP config file in text editor.

Format of resulting table is explained in converted table itself; I recomment to convert existing .cfg patch to ODS and looks 

## Usage

Converting patch config (cfg) to ODS
```
RF_unpacker.py <cfg file> <ODS file> 
```

Converting ODS to patch config (cfg)
```
RF_packer.py <ODS file> <cfg file>
```

### Prerequisites

Understanding of RealFuels modules structure

python3
https://www.python.org/downloads/

pyexcel_ods3 library
```
pip install pyexcel_ods3
```

### Links

ReadFuels repository: https://github.com/NathanKell/ModularFuelSystem
RealFules forum thread: https://forum.kerbalspaceprogram.com/index.php?/topic/58236-13-real-fuels-v1223-july-30/
