# -*- coding: utf-8 -*-
import lca_algebraic as agb

# # Definition of input parameters

# In this section, we define the main variable and fixed parameters that will be used for modeling the wind electricity production facility.
#
# In this case, Kouloumpis and Azapagic (2022) was considered as a reference source to set the default values of the variable parameters defined in this section.
#
# The minimum and maximum values were "arbitrarily" fixed considering the set of variation of this parameters in existing or upcomping wind farms.

# ## Global Wind farm parameters 

# +
n_turbines = agb.newFloatParam(
    "n_turbines",
    default=60, min=1, max=100,         
    group="1. Global wind farm",
    label="the number of wind turbines in the wind farm",
    unit="turbines")

#Default value chosen based on French wind farms (non pilot farms) with an AC connexion 

# +
turbine_MW = agb.newFloatParam(
    "turbine_MW",
    default = 8, min = 5, max = 15,
    group="1. Global wind farm",
    label = " the unit capacity of one wind turbine",
    unit ="MW")

#Default value is the average of min and max value

# +
life_time = agb.newFloatParam(
    'life_time',
    default = 25, min = 20, max = 30,
    group="1. Global wind farm",
    label = 'the life time of wind farm',
    unit = 'years')

#Default value from Kouloumpis and Azapagic (2022)  

#Internal RTE studies for electrical connection sub-system chose a life time of 40 years for these equipments.
#To be consistant, we have chosen a common life time for all the system.
#Indeed, we dont know what will happen after the decommisioning of wind turbines.
#If the wind turbines are replaced by new ones and the electric connexion is maintained,
#this would decrease the contribution of this subsystem to the total impacts as its life time would be increased.

# +
availability = agb.newFloatParam(
    'availability',
    default = 1, min = 0.9, max = 1,
    group="1. Global wind farm",
    label ='ratio of time when the windturbines are not stopped for maintenance')

#Default value = 100% assumes that the availability is already included in the load factor

# +
elec_losses = agb.newFloatParam(
    'elec_losses',
    default = 0.003+0.006+0.001, min = 0.002, max = 0.02,
    group="1. Global wind farm",
    label ='ratio of electricity losses between the production (wind turbines) and the landfall junction')

# Default value taken from 
# 1. wind experts for interarray cables
# 2. RTE Study considering the losses of the offshore substation (transformers) and export cables for a 600 MW farm with an AC connexion with 30 km of cables
# See report for more explanations

# +
load_rate = agb.newFloatParam(
    'load_rate',
    default = 0.4, min = 0, max = 1,
    group="1. Global wind farm",
    label = 'ratio of the total electricity produced against the theoretical one for a year')

#Default value based on load factors found for France offshore wind farms 

# +
foundations_type = agb.newEnumParam(
    "foundations_type", 
    group = '1. Global wind farm',
    default="jacket",
    values=["gbf", "monopod", "tripod", "jacket", "floatingspar", "semisub","custom"], 
    label = 'the type of foundations. Warning : water depth and foundation type are correlated')

#gbf, monopod, tripod, floating spar foundations or customised foundations
#customised = the user can do customised inventories 

# +
fixed_foundations = agb.newBoolParam(
    "fixed_foundations",
    1, # defaut value : fixed-bottom foundations
    group = "1. Global wind farm",
    label ="the type of foundations fixed/floating")

floating_foundations = 1 - fixed_foundations

# default value : fixed-bottom foundations

# +
water_depth = agb.newFloatParam(
    "water_depth",
    default = 30, min = 10, max = 200,
    group="1. Global wind farm",
    label="the water depth of the wind farm site",
    unit="m")

# default value : arbitrary value that is compatible with fixed-bottom foundations

# +
#Warning : the length defined is not the total length of export cables but the length of one export cables.
# If there are 2 or 3 cables, the total length of cables is the double or the triple of the parameters values.

length_1_expcable_tot = agb.newFloatParam(
                'length_1_expcable_tot',
            default = 20000, min = 10000, max = 40000,
            group="1. Global wind farm",
            label = 'the total length of one export cables',
            unit = 'm')

# default value : RTE study of Dunkerque installation

length_1_expcable_cop = agb.newFloatParam(
                'length_1_expcable_cop',
            default = 1000, min = 0, max = 10000,
            group="1. Global wind farm",
            label = 'the length of one copper export cables',
            unit = 'm')

# default value : RTE study of Dunkerque installation

#The length of the aluminium section of one export cables is divided 
length_1_expcable_alu=length_1_expcable_tot-length_1_expcable_cop #m
# -

# ## Parameters specific for transport, installation, O&M, decomissioning stages

# +
#Parameter for transport stage
d_manufacturingsite_onshoresite_lorry = agb.newFloatParam(
    "d_manufacturingsite_onshoresite_lorry",  
    default = 3000, min = 0, max = 10000,
    group = '2. Transport, installation, O&M, decomissioning',
    label = "the distance between manufacturing site and onshore site that is done by lorry",
    unit = "km")

d_manufacturingsite_onshoresite_ship = agb.newFloatParam(
    "d_manufacturingsite_onshoresite_ship",  
    default = 3000, min = 0, max = 10000,
    group = '2. Transport, installation, O&M, decomissioning',
    label = "the distance between manufacturing site and onshore site that is done by container ship",
    unit = "km")

# Default value : arbitrary value chosen considering transport from European countries close to France

# +
#Parameter for installation stage  
d_shore = agb.newFloatParam(
    "d_shore",
    default = 20, min=5, max=50,
    group = '2. Transport, installation, O&M, decomissioning',
    label = 'The distance between the port (onshore area) and the windturbines in the sea (offshore area)',
    unit = "km")

#Default value based on distances found for France offshore wind farms 
# -

# ## Recycled materials IN

# +
steel_recycled_share_IN = agb.newFloatParam(
    "steel_recycled_share_IN",
    default = 0.76, min=0, max=1,            #default value calculated from ecoinvent 3.7
    group = '3. Materials IN',
    label = 'The share of recycled steel used as an input to manufacture the wind farm components')

steel_primary_share_IN=1-steel_recycled_share_IN

# +
alu_recycled_share_IN = agb.newFloatParam(
    "alu_recycled_share_IN",
    default = 0.30, min=0, max=1,        #default value calculated from ecoinvent 3.7
    group = '3. Materials IN',
    label = 'The share of recycled aluminium used as an input to manufacture the wind farm components')

alu_primary_share_IN=1-alu_recycled_share_IN

# +
copper_recycled_share_IN = agb.newFloatParam(
    'copper_recycled_share_IN',
    default = 0.20, min = 0, max = 1,        #default value calculated from ecoinvent 3.7
    group = '3. Materials IN',
    label = 'The share of recycled copper used as an input to manufacture the wind farm components')

copper_primary_share_IN=1-copper_recycled_share_IN
# -

# ## End-of-life of materials

# **Note** all the default values are settled as all materials are landfilled
#
# **Warning** When we create ratio with 3 or more options, the ratios needs to be corrected to be sure that the sum of the ratios equals to 1. This is why some materials ratios are corrected in the model. 

# ### Steel

steel_recycled_share_OUT = agb.newFloatParam(
    "steel_recycled_share_OUT",
    default = 0, min=0, max=1,
    group = '4. EoL - Materials OUT',
    label = 'The share of steel going to recycling after the wind farm decommissioning')

# ### Aluminium

alu_recycled_share_OUT = agb.newFloatParam(
    "alu_recycled_share_OUT",
    default = 0, min=0, max=1,
    group = '4. EoL - Materials OUT',
    label = 'The share of aluminium going to recycling after the wind farm decommissioning')

alu_landfill_share = agb.newFloatParam(
   "alu_landfill_share",
    default = 1, min=0, max=1,
    group = '4. EoL - Materials OUT',
    label = 'The share of aluminium going to landfilling after the wind farm decommissioning')

alu_incineration_share = agb.newFloatParam(
    "alu_incineration_share",
    default =0, min=0, max=1,
    group = '4. EoL - Materials OUT',
    label = 'The share of aluminium going to incineration after the wind farm decommissioning')

#Correction in case alu_recycled_share_OUT + alu_landfill_share + alu_incineration_share >1:
alu_recycled_share_OUT_correc=(alu_recycled_share_OUT)/(alu_recycled_share_OUT+alu_landfill_share+alu_incineration_share)
alu_landfill_share_correc=(alu_landfill_share)/(alu_recycled_share_OUT+alu_landfill_share+alu_incineration_share)
alu_incineration_share_correc=(alu_incineration_share)/(alu_recycled_share_OUT+alu_landfill_share+alu_incineration_share)

# ### Copper

copper_recycled_share_OUT = agb.newFloatParam(
    'copper_recycled_share_OUT',
    default = 0, min = 0, max = 0.3,
    group = '4. EoL - Materials OUT',
    label = 'The share of copper going to recycling after the wind farm decommissioning')

copper_landfill_share = agb.newFloatParam(
   "copper_landfill_share",
    default = 1, min=0, max=1,
    group = '4. EoL - Materials OUT',
    label = 'The share of copper going to landfilling after the wind farm decommissioning')

copper_incineration_share = agb.newFloatParam(
    "copper_incineration_share",
    default =0, min=0, max=1,
    group = '4. EoL - Materials OUT',
    label = 'The share of copper going to incineration after the wind farm decommissioning')

#Correction in case alu_recycled_share_OUT + alu_landfill_share + alu_incineration_share >1:
copper_recycled_share_OUT_correc=(copper_recycled_share_OUT)/(copper_recycled_share_OUT+copper_landfill_share+copper_incineration_share)
copper_landfill_share_correc=(copper_landfill_share)/(copper_recycled_share_OUT+copper_landfill_share+copper_incineration_share)
copper_incineration_share_correc=(copper_incineration_share)/(copper_recycled_share_OUT+copper_landfill_share+copper_incineration_share)

# ### Concrete

# +
concrete_recycled_share_OUT = agb.newFloatParam(
    'concrete_recycled_share_OUT',
    default = 0, min = 0, max = 0.3, ## Rate of recyclability for concrete limited to 30% according to ArchDaily, 2022 (https://www.archdaily.com/972748/concrete-recycling-is-already-a-reality)
    group = '4. EoL - Materials OUT',
    label = 'The share of concrete going to recycling after the wind farm decommissioning')

# Default value = 0 because recycling concrete as aninput material for the manufacturing of the wind farm is not considered in the model.
# -

# ## Check that the name of the parameter is the same as the name of the variable

## Check that the name of the parameter is the same as the name of the variable
for name, var in list(globals().items()):
    if isinstance(var, agb.ParamDef) and var.name != name :
        print("Alert : param name is different for var name : %s <> %s" % (var.name, name))
