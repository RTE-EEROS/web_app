# -*- coding: utf-8 -*-
# # Text variables

# +
# Life cycle stages 
# Axis name = "phase"
PHASE_1_MANUFACTURING="phase 1 - manufacturing"
PHASE_2_TRANSPORT="phase 2 - transport"
PHASE_3_INSTALLATION="phase 3 - installation"
PHASE_4_OANDM ="phase 4 - operation and maintenance"
PHASE_5_DECOM="phase 5 - decommissionning"
PHASE_6_EOL="phase 6 - end of life"

# Subsystems
# Axis name = "system_1"
WIND_TURBINES="wind turbines"
WT_FOUNDATIONS="wind turbines foundations"
INT_CABLES="inter-array cables"
SUBSTATION="offshore substation"
EXP_CABLES="export cables"
WT_WTFOUNDATIONS_INTCABLES="wind turbines + foundations ¨+ inter-array cables"

#system_2 / Wind Turbine
TOWER="tower"
NACELLE="nacelle"
ROTOR="rotor"

#system_2 / Export cables
ALU_EXP_CABLES="aluminum export cables"
COP_EXP_CABLES="copper export cables"

#system_2 / Offshore substation
OFFSHORE_SUB_STRUCTURE="offshore substation structure"
OFFSHORE_SUB_EQUIPMENT ="offshore substation equipments"
# -

# # Constant variables

# +
KWH_TO_MJ = 3.6 #kWh/MJ 
DIESEL_CALORIFIC_VALUE_MJ_PER_L = 38.68 #MJ/L     # Conversion of 1L of diesel into MJ #https://fr.wikipedia.org/wiki/Discussion:Empreinte_carbone#:~:text=1%20litre%20de%20diesel%20%3D%2038,68%20MJ%20%3D%2010%2C74%20kWh 
DIESEL_DENSITY_KG_L = 0.832 #kg/L                #https://www.infineuminsight.com/media/2228/infineum-wdfqs-2018-v10-14112018.pdf
DIESEL_CALORIFIC_VALUE_MJ_PER_KG=DIESEL_CALORIFIC_VALUE_MJ_PER_L/DIESEL_DENSITY_KG_L
HEAVY_FUEL_CALORIFIC_VALUE_MJ_PER_KG = 40.9 #MJ/kg  https://www.sciencedirect.com/topics/engineering/heavy-fuel-oil#:~:text=(b)%20Heavy%20fuel%20oil%20or%20marine%20diesel&text=The%20typical%20heating%20value%20is,is%20typically%20%3E%2060%20%C2%B0C.
HEAVY_FUEL_DENSITY_KG_L=1 #kg/L
HEAVY_FUEL_CALORIFIC_VALUE_MJ_PER_L =HEAVY_FUEL_CALORIFIC_VALUE_MJ_PER_KG*HEAVY_FUEL_DENSITY_KG_L
STEEL_KG_PER_METER = 507*7.92 #kg/m              #https://www.twi-global.com/technical-knowledge/job-knowledge/calculating-weld-volume-and-weight-095

#Note_Paula : Question transmitted to Manel - to be verified by her
STEEL_DENSITY_TOWER = 8500 #kg/m3
DENSITY_STEEL = 7850  #kg/m³

#Note_Paula : Question transmitted to Manel - to be verified by her
CONCRETE_DENSITY = 2300 #kg/m3         (Pacheco-Torgal et al, 2020: https://www.sciencedirect.com/book/9780128190555/advances-in-construction-and-demolition-waste-recycling)
CONCRETE_DENSITY_2= 2406.53 #kg/m3     (https://www.traditionaloven.com/building/masonry/concrete/convert-cubic-metre-m3-concrete-to-kilogram-kg-of-concrete.html#:~:text=The%20answer%20is%3A%20The%20change,for%20the%20same%20concrete%20type.)

#Fixed parameters used for the calculations of Rotor & Nacelle LCI
DENSITY_ALU = 2710 #kg/m3                (https://www.thyssenkrupp-materials.co.uk/density-of-aluminium.html)
DENSITY_COPPER = 8960 # kg/m³ 
DENSITY_LEAD = 11342 #kg/m³ 
DENSITY_HDPE = 970  #kg/m3               > high density polyethylene
DENSITY_PP = 946 #kg/m³                  > polypropylene
DENSITY_PINEWOOD = 600.5 #kg/m3          # Mean value for the range 352-849, source https://matmatch.com/learn/property/density-of-wood
GAS_ENERGY_PER_VOLUME = 10.55 #kWh/m3    # Conversion volume to kWh, gaz, source: https://learnmetr "ics.com/m3-gas-to-kwh/   

# Fixed parameter used for the calculations of Inter-array cables' LCI.
ZINC_COATING = 214.2 #kg/m2 > zinc coating for foundations structure, 30*7.14, source: (https://itemscatalogue.redcross.int/detail.aspx?productcode=EMEAGAUG01#:~:text=The%20density%20of%20the%20zinc,equivalent%20to%207.14%20g%2Fm2.&text=Example%3A%20zinc%20coating%20thickness%20measured,of%20zinc%20on%20one%20side.)
# -


