---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
  kernelspec:
    display_name: lifowi
    language: python
    name: lifowi
---

# Description of the wind power farm life cycle assessment model and system boundaries

This parameterized Life Cycle Assessment (LCA) model has been built in the frame of [LIF-OWI project](https://www.france-energies-marines.org/projets/lif-owi/) with the aim of facilitating the development of tailor-made life cycle inventories to obtain fast estimates of multi-criteria LCA results for offshore fixed and floating wind power projects in France. 

The model uses functions of the python packages [lca_algebraic](https://github.com/oie-mines-paristech/lca_algebraic), and Brightway2.

A report explaining this LCA model is available.


## LIF-OWI model scope and wind power farm subsystems


The parameterized LCA model was developed to evaluate **wind power farms composed of wind turbines ranging between 5 MW and 15 MW capacity.**

The wind power farm is composed of 5 main subsystems, indicated in Figure 1 : 
* Windturbines (divided into 3 subsystems : tower, rotor and nacelle)
* Foundations of wind turbines
* Inter-array cables 
* Offshore substation 
* Export cables (divided into 2 subsystems : aluminium cables and copper cables)

![Image_systeme_v4.png](attachment:Image_systeme_v4.png)

Fig.1. Components of an offshore wind power farm included in LIF-OWI parameterized model (adapted from RTE website)


## Life cycle stages of the wind power farm


The functional unit chosen to refer the estimated impacts to is **1 kWh**. In an intermediate step, the user can also obtain the LCI and impacts associated per **1 MW installed capacity** and at **the scale of the wind farm**. 

The life cycle of the wind power farm has been divided in 6 main stages, namely:
* Manufacturing: raw material extraction, manufactured material production and shaping, assembly of components  ​ 
* Transport from the manufacturing sites to the onshore site
* Installation from the onshore site to the offshore area
* Operation and maintenance
* Decommissioning 
* End-of-life

![Life%20cycle%20step_v2.png](attachment:Life%20cycle%20step_v2.png)
Fig.2. Life cycles stages studied in this model 

The model is divided in sections that correspond to the above-mentioned life cycle stages.


## "Level of use" of the parameterised model


This LCA model is parameterised. It means the values of the inventories flows can be alculated automatically based on the values of a set of parameter.

1️⃣ The user just settles lca_algebraic parameters values.

2️⃣ The user can either change the formula to calculate the intermediate variables, either directly enter the value of this "intermediate variable". 

3️⃣ As in “level 2”, the user can modify the value of some "intermediate variables” that are more detailed than on level 2. 

4️⃣ The user can customise all the flows of the inventory (not only changing material masses)

If there is an icon 1️⃣ or 2️⃣ or 3️⃣ or 4️⃣ in the title of a section, it means that the user has to change something in this section to use the model at the level indicated by the icon. 


# Initialization of the model (import of packages and functions)

```python
#Automatic reload of .py files
%load_ext autoreload
%autoreload 2

# We import all the usefull librairies including lca_algebraic as agb.
from init import *

# Import constants (text and numbers)
from constants import *

# Import custom functions
from utils import compute_value
from utils import values_table
from utils import compute_impacts
from utils import list_parameters_as_df
from utils import export_data_to_excel

#Import functions that define background flows
from background_flows import negAct
from background_flows import import_background
from background_flows import print_background
from background_flows import USER_DB

#Import wind turbines and rotor diameter model 
from mass_extrapolation_functions import rotor_diameter_m_power_MW_2,tower_mass_t_power_MW_2,three_blades_mass_t_power_MW_2,nacelle_with_hub_mass_t_power_MW_2,wind_turbine_mass_t_power_MW_2
from mass_extrapolation_functions import jacket_mass_per_length_tperm_power_MW
```

```python
# Setup new project
agb.initProject('Parameterized_model_OWF_Original')

# Import Ecoinvent DB (if not already done)
# To do : Update the PATH to suit your installation
agb.importDb("ecoinvent", '/var/local/ecoinvent/ecoinvent3.7/datasets')

# We use a separate DB for defining our model, reset it beforehand
agb.resetDb(USER_DB)

# Reset the definition of all parameters 
agb.resetParams()
```

# Selection of LCIA method and impact categories

## LCIA method

```python
# We choose the LCIA method : the Environmental Footprint method v3.0 
LCIA_method = 'EF v3.0'
```

## Selection of impact categories 

```python
# We define the impacts categories that we want to study
climate_tot = (LCIA_method,'climate change','global warming potential (GWP100)')
climate_bio = (LCIA_method,'climate change: biogenic','global warming potential (GWP100)')
climate_foss = (LCIA_method,'climate change: fossil','global warming potential (GWP100)')
climate_land = (LCIA_method,'climate change: land use and land use change','global warming potential (GWP100)')
ecosystem_quality_ecotox= (LCIA_method,'ecotoxicity: freshwater','comparative toxic unit for ecosystems (CTUe) ')
ecosystem_quality_acid = (LCIA_method,'acidification','accumulated exceedance (ae)')
ecosystem_quality_fresh_eut = (LCIA_method,'eutrophication: freshwater','fraction of nutrients reaching freshwater end compartment (P)')
ecosystem_quality_mar_eut = (LCIA_method,'eutrophication: marine','fraction of nutrients reaching marine end compartment (N)')
ecosystem_quality_ter_eut=(LCIA_method,'eutrophication: terrestrial','accumulated exceedance (AE) ')
human_health_io= (LCIA_method,'ionising radiation: human health','human exposure efficiency relative to u235')
human_health_oz= (LCIA_method,'ozone depletion','ozone depletion potential (ODP) ')
human_health_pht= (LCIA_method, 'photochemical ozone formation: human health','tropospheric ozone concentration increase')
human_health_res= (LCIA_method,'particulate matter formation','impact on human health')
human_health_noncar= (LCIA_method,'human toxicity: non-carcinogenic','comparative toxic unit for human (CTUh) ')
human_health_car= (LCIA_method,'human toxicity: carcinogenic','comparative toxic unit for human (CTUh) ')
resources_foss =(LCIA_method,  'energy resources: non-renewable',  'abiotic depletion potential (ADP): fossil fuels')
resources_land = (LCIA_method, 'land use', 'soil quality index')
resources_min_met =(LCIA_method,'material resources: metals/minerals','abiotic depletion potential (ADP): elements (ultimate reserves)')
resources_water = (LCIA_method,  'water use',  'user deprivation potential (deprivation-weighted water consumption)')
```

```python
#We define a list of 19 impacts
impacts_EF_3_0 = [climate_tot, climate_bio, climate_foss, climate_land, ecosystem_quality_ecotox,ecosystem_quality_acid,
                  ecosystem_quality_fresh_eut, 
                  ecosystem_quality_mar_eut, 
                  ecosystem_quality_ter_eut, human_health_io,
                  human_health_oz, human_health_pht, human_health_res, human_health_noncar, human_health_car, resources_foss,
                  resources_land, resources_min_met, resources_water]

#We define a list of 1 impact (climate change impact) to do fast calculation
impacts_EF_CO2 = [climate_tot]
```

```python
nb_impacts=len(impacts_EF_3_0)
print(f"We have selected {nb_impacts} impacts categories calculated with the LCIA method : '{LCIA_method}' that are :")
impacts_EF_3_0
```

# 1️⃣ Definition of lca_algebraic parameters


In this section, we define the main variable parameters that will be used for modeling the wind electricity production facility.

Level 1️⃣ : you have to settle the default values of parameters in the parameters.py file. 

```python
from parameters import *
#Pay attention to Alert message but do not pay attention to Warning message
```

```python
# The list of parameters is : 
agb.list_parameters()
```

# Definition of activities from the background database


In this section, we import the background activities (i.e. ecoinvent processes from technosphere) that will be used for modeling the wind electricity production facility. These activities are defined in background_flows.py files 


## Definition of background activities

```python
# Get all background activities
acts = import_background()

# Import them as global variable in current scope
globals().update(acts)

# Print the background flows
print_background(acts)
```

**Warning !!!** 
Activities with negative flows are corrected with **negAct function**.
We use negAct function to correct the sign of some activities that are accounted as negative in brightway (mostly waste treatment activities)
Warning, if you print activities defined with negAct, the reference flow will still appear as negative
when you print them with agb.printAct
but it will be accounted as a positive flow (you can compute a basic impact calcultation to check that)


## Definition of new materials activities including recycling
The recycling of materials is modeled with a simple cut-off approach. We define new material activities that are a mix between virgin and recycled material for **aluminium, steel, copper and concrete.** <br>
<br>
As the exchanges of market activities have same code names, they can not be sorted easily by their code names using updateExchange function. This is why specific functions are defined to be able to manipulate the exchanges using their input name and / or their location. 


### Steel

```python
#Copy of market for steel to be modified
steel_low_alloyed_mix = agb.copyActivity(
    USER_DB,
    steel_low_alloyed, 
    "steel mix primary and recycled",
    location="GLO")

#Print activity before being modified
agb.printAct(steel_low_alloyed)

#List of exchanges in this activity
exchs=steel_low_alloyed_mix.exchanges()
```

```python
# We calculate the share of recycled material in the market ecoinvent activity
steel_recycled_share_IN_ecoinvent=0       #initialisation
for exch in exchs:
    act=agb.getActByCode(*exch["input"])  #exchanges can not be sorted by name as they all have the same name, they have to be sorted by their "input"
    if "electric" in (act['name']):       #recycled steel activities include "electric" in their name
        steel_recycled_share_IN_ecoinvent=steel_recycled_share_IN_ecoinvent+exch["amount"]

steel_primary_share_IN_ecoinvent=1-steel_recycled_share_IN_ecoinvent
print("{:.0%}".format(steel_recycled_share_IN_ecoinvent))
```

```python
#We change the value of exchanges' amount to make vary the recycling rate using the recycling rate parameter and the ecoinvent static recycling rate

def replace_steel(exch,keyword_recycled,keyword_primary):
    act=agb.getActByCode(*exch["input"]) #exchanges can not be sorted by name as they all have the same name, they have to be sorted by their "input"
    if keyword_recycled in (act['name']):
        old_exc_amount=exch["amount"]
        exch["formula"]=str(old_exc_amount*steel_recycled_share_IN/steel_recycled_share_IN_ecoinvent)
        exch.save()

    elif keyword_primary in (act['name']): 
        old_exc_amount=exch["amount"]
        exch["formula"]=str(old_exc_amount*steel_primary_share_IN/steel_primary_share_IN_ecoinvent)
        exch.save()

for exch in exchs:
    replace_steel(exch,"electric","converter")


```

```python
#Print the differences between ecoinvent activity and parameterised activity 
agb.printAct(steel_low_alloyed,steel_low_alloyed_mix)

#Print the inventory with a given value of recycled share
agb.printAct(steel_low_alloyed_mix,steel_recycled_share_IN=0.76)
```

### Aluminium

```python
#Copy of market for aluminium to be modified
aluminium_mix = agb.copyActivity(
    USER_DB,
    aluminium, 
    "aluminium mix primary and recycled",
    location="GLO")

#Print activity before being modified
agb.printAct(aluminium_mix)

#List of exchanges in this activity
exchs=aluminium_mix.exchanges()
```

```python
# We calculate the share of recycled material in the market ecoinvent activity

alu_recycled_share_IN_ecoinvent=0         #initialisation
for exch in exchs:
    act=agb.getActByCode(*exch["input"])  #exchanges can not be sorted by name as they all have the same name, they have to be sorted by their "input"
    if "scrap" in (act['name']):         #recycled aluminium activities include "scrap" in their name
        alu_recycled_share_IN_ecoinvent=alu_recycled_share_IN_ecoinvent+exch["amount"]

alu_primary_share_IN_ecoinvent=1-alu_recycled_share_IN_ecoinvent

print("{:.0%}".format(alu_recycled_share_IN_ecoinvent))
```

```python
#We change the value of exchanges' amount to make vary the recycling rate using the recycling rate parameter and the ecoinvent static recycling rate

def replace_alu(exch,keyword_recycled,keyword_primary):
    act=agb.getActByCode(*exch["input"]) #exchanges can not be sorted by name as they all have the same name, they have to be sorted by their "input"
    
    if keyword_recycled in (act['name']):
        old_exc_amount=exch["amount"]
        exch["formula"]=str(old_exc_amount*alu_recycled_share_IN/alu_recycled_share_IN_ecoinvent)
        exch.save()

    elif keyword_primary in (act['name']):
        old_exc_amount=exch["amount"]
        exch["formula"]=str(old_exc_amount*alu_primary_share_IN/alu_primary_share_IN_ecoinvent)
        exch.save()

for exch in exchs:
    replace_alu(exch,"scrap","primary")

    
```

```python
#Print the differences between ecoinvent activity and parameterised activity 
agb.printAct(aluminium,aluminium_mix)

#Print the inventory with a given value of recycled share
agb.printAct(aluminium_mix,alu_recycled_share_IN=0.30)
```

### Copper

```python
#Copy of market for copper to be modified
copper_mix = agb.copyActivity(
    USER_DB,
    copper, 
    "copper mix primary and recycled",
    location="GLO")

#Print activity before being modified
agb.printAct(copper_mix)

#List of exchanges in this activity
exchs=copper_mix.exchanges()
```

```python
# Simplification and normalisation of copper activity
correction_copper_1kg=0 #initialisation

for exch in exchs:
    act=agb.getActByCode(*exch["input"])    #exchanges can not be sorted by name as they all have the same name, they have to be sorted by their "input"
 
    if exch["amount"]<=0.01:      # We simplify the copper activity by deleting exchanges below 0,01 kg
        correction_copper_1kg=correction_copper_1kg+exch["amount"]
        exch["amount"]=0          # exc = 0 instead of delete exc to picture better the changes with printAct
        #exch.delete()
        exch.save()
    else :                       # We normalize the remaining exchanges so that their sum equals to 1 kg
        exch["amount"]=exch["amount"]/(1-correction_copper_1kg)
        exch.save()
        
print("%.3f" % (1-correction_copper_1kg)) #The remaining exchanges in kg before being resized"
agb.printAct(copper,copper_mix)
```

```python
# We calculate the share of recycled material in the simplified market ecoinvent activity
copper_recycled_share_IN_ecoinvent=0       #initialisation
for exch in exchs:                         #exchanges can not be sorted by name as they all have the same name, they have to be sorted by their "input"
    act=agb.getActByCode(*exch["input"])
    if "treatment" in (act['name']):       #recycled copper = "treatment ...""
        copper_recycled_share_IN_ecoinvent=copper_recycled_share_IN_ecoinvent+exch["amount"]
copper_primary_share_IN_ecoinvent=1-copper_recycled_share_IN_ecoinvent
print("{:.0%}".format(copper_recycled_share_IN_ecoinvent))
```

```python
# We introduce the parameter "share of recycled material" normalised by ecoinvent value
def replace_copper(exch,keyword):
    act=agb.getActByCode(*exch["input"]) #exchanges can not be sorted by name as they all have the same name, they have to be sorted by their "input"
    if keyword in (act['name']):
        old_exc_amount=exch["amount"]
        exch["formula"]=str(old_exc_amount*copper_recycled_share_IN/copper_recycled_share_IN_ecoinvent)
        exch.save()  
    else:
        old_exc_amount=exch["amount"]
        exch["formula"]=str(old_exc_amount*copper_primary_share_IN/copper_primary_share_IN_ecoinvent)
        exch.save()

for exch in exchs:
    replace_copper(exch,"treatment")
    


```

```python
#Print the differences between ecoinvent activity and parameterised activity 
agb.printAct(copper,copper_mix)
#Print the inventory with a given value of recycled share
agb.printAct(copper_mix, copper_recycled_share_IN=0.2)
```

### Concrete

```python
concrete_mix = agb.copyActivity(
    USER_DB,
    concrete, 
    "concrete mix - only primary",
    location="GLO")

agb.printAct(concrete)
```

### Modify by yourself an exchange of market activity

```python
#1. Create an activity "test_act" that you want to modify with agb.copyActivity by copying an existing activity "initial_act"
#1bis. Print it with agb.printAct
#2. Define the of exchanges in this activity
        #exchs=test_act.exchanges()
#3. Define a function to replace an exchange according to its input name and its location
def replace_exchange(exch,keyword,loc):
    act=agb.getActByCode(*exch["input"])  
    if keyword in (act['name']) and loc in act['location']:
        old_exc_amount=exch["amount"]
        exch["amount"]=1 #amount to be updated 
        exch["formula"]=str(old_exc_amount*1) #formula to be updated
        exch.save()
#4. Apply the function to the activity to be modified
    #for exch in exchs:
    #    replace_exchange(exch,"treatment","RER")
#5. Print the initial and modified activity to     
    #agb.printAct(initial_act,test_act)

# Alternative to 3 and 4 : modify directly exchanges without creating a function 
    #for exch in exchs:
    #act=agb.getActByCode(*exch["input"])
        #if  "treatment of copper scrap" in (act['name']) and "RoW" in (act['location']):
           #old_exc_amount=exch["amount"]
           #exch["formula"]=str(old_exc_amount*copper_primary_share_IN/copper_primary_share_IN_ecoinvent)
           #exch.save() 
```

# Transversal calculation


## 2️⃣ Electricity delivered to the grid
Using the defined input parameters, the total power capacity of the wind farm (in MW) the total electricity (in kWh) delivered to the grid over the lifetime of the offshore wind farm can be estimated with the following equations.

Level 2️⃣ : you can enter directly the total electricity produced by the wind farm, the formula can be deleted and replaced by the given value. 

```python
power_tot_farm_MW=n_turbines*turbine_MW
```

```python
elec_prod_lifetime_kWh=(load_rate*availability*(1-elec_losses)*8760*turbine_MW*1000*n_turbines*life_time)
#8760 = Number of hours per year
#*1000 to convert from MW to kW
```

## Wind turbine's rotor diameter and mass model = f(turbine_MW)
Using formula provided by an implemented model based on online collected data, we calculate rotor diameter, mass of rotor, mass of nacelle and mass of tower of a wind turbine based on its power capacity. The formulas are imported from the file:  mass_extrapolation_function.py. The mass model are printed in the file : visualisation_wind_turbine_extrapolation.py <br> 
The calculated masses can then be used or not by the model depending on the model of use (section 7.1). 

```python
rotor_diameter_calc_m=rotor_diameter_m_power_MW_2(turbine_MW)
mass_nacelle_calc_kg=nacelle_with_hub_mass_t_power_MW_2(turbine_MW)*1000
mass_rotor_calc_kg=three_blades_mass_t_power_MW_2(turbine_MW)*1000
mass_tower_calc_kg=tower_mass_t_power_MW_2(turbine_MW)*1000
mass_wind_turbine_tot_calc_kg=wind_turbine_mass_t_power_MW_2(turbine_MW)*1000
```

```python
values_table(
    mass_nacelle_calc_kg=(mass_nacelle_calc_kg, "kg"),
    mass_rotor_calc_kg=(mass_rotor_calc_kg, "kg"),
    mass_tower_calc_kg=(mass_tower_calc_kg, "kg"))

values_table(
    rotor_diameter_calc_m=(rotor_diameter_calc_m, "m"))
```

## Jacket foundations mass model = f(turbine_MW)

```python
#Mass of jacket per meter is generated with online collected data
lineic_mass_foundations_jacket_calc_kg_per_m=jacket_mass_per_length_tperm_power_MW(turbine_MW)*1000 #kg
```

## Semi-submersible foundations mass model = f(turbine_MW)

```python
lineic_mass_foundations_semisub_calc_kg_per_m=0 #kg
```

# Inventories : Manufacture and assembly of components


## Wind turbines : tower, rotor and nacelle


Estimates of input flows to the manufacturing processes were based on data from a reference wind farm composed of 30 wind turbines of 5MW, provided by Kouloumpis and Azapagic (2022), https://doi.org/10.1016/j.spc.2021.10.024.

```python
#Reference data 

#Nominal power of one turbine
POWER_REF_TURBINE_MW = 5 # MW
#Number of turbines in the wind farm
NUMBER_REF_TURBINE = 30 # wind turbines
```

### Tower 


#### Reference inventory

```python
#Reference data for the tower

#Mass of steel in the tower
MASS_TOWER_STEEL_LOW_ALLOYED_KG=6510660/NUMBER_REF_TURBINE                       #kg
#Mass of steel in the tower
MASS_TOWER_ALUMINIUM_KG=119340/NUMBER_REF_TURBINE                                #kg
#Total mass of the tower
MASS_TOWER_TOT_KG=MASS_TOWER_STEEL_LOW_ALLOYED_KG+MASS_TOWER_ALUMINIUM_KG        #kg

#Amount of other flows
TOWER_ELECTRICITY_kWH= 676923/NUMBER_REF_TURBINE                                  #kWh
TOWER_DIESEL_MJ = 3315*DIESEL_CALORIFIC_VALUE_MJ_PER_L/NUMBER_REF_TURBINE         #MJ
TOWER_HEATING_MJ = 127959*KWH_TO_MJ/NUMBER_REF_TURBINE                            #MJ
TOWER_WELDING_GAS_M = 663/STEEL_KG_PER_METER/NUMBER_REF_TURBINE                   #m
TOWER_FUEL_OIL_MJ = 53703*HEAVY_FUEL_CALORIFIC_VALUE_MJ_PER_L/NUMBER_REF_TURBINE        #MJ
TOWER_WASTEWATER_L = 103428/NUMBER_REF_TURBINE                                    #L or kg (similar)
TOWER_WASTE_UNSPECIFIED_KG = 91494/NUMBER_REF_TURBINE                             #kg
TOWER_WASTE_HAZARDOUS_KG = 663/NUMBER_REF_TURBINE                                 #kg
TOWER_OIL_WASTE_KG = 132.6/NUMBER_REF_TURBINE                                     #kg
```

```python
#Print a table with the masses of materials of the reference tower
#function values_table is defined in "utils"

values_table(
    MASS_TOWER_TOT_KG=(MASS_TOWER_TOT_KG,"kg"),
    MASS_TOWER_STEEL_LOW_ALLOYED_KG=(MASS_TOWER_STEEL_LOW_ALLOYED_KG, "kg"),
    MASS_TOWER_ALUMINIUM_KG=(MASS_TOWER_ALUMINIUM_KG, "kg"))
```

```python
#We define the reference tower manufacturing inventory based on data provided by Kouloumpis and Azapagic, 2022
tower_manufacturing_ref = agb.newActivity(USER_DB,
                       "manufacturing of the tower of one 5 MW reference turbine ",
                       unit = "unit",
                       phase = PHASE_1_MANUFACTURING,
                       system_2=TOWER,
                       exchanges = {
                           steel_low_alloyed_mix:   MASS_TOWER_STEEL_LOW_ALLOYED_KG, 
                           aluminium_mix :          MASS_TOWER_ALUMINIUM_KG,
                           
                           electricity_UCTE:        TOWER_ELECTRICITY_kWH, 
                           diesel_process:          TOWER_DIESEL_MJ,
                           district_heating:        TOWER_HEATING_MJ, 
                           welding_gas:             TOWER_WELDING_GAS_M,
                           fuel_oil_process:        TOWER_FUEL_OIL_MJ,
                           wastewater_treatment:    TOWER_WASTEWATER_L,
                           waste_unspecified:       TOWER_WASTE_UNSPECIFIED_KG,
                           waste_hazardous:         TOWER_WASTE_HAZARDOUS_KG,
                           oil_waste:               TOWER_OIL_WASTE_KG,
             })

#Print the reference inventory
agb.printAct(tower_manufacturing_ref)
```

```python
# Explore the climate change impacts of the reference inventory
agb.exploreImpacts(impacts_EF_CO2[0], tower_manufacturing_ref)
```

####  2️⃣ 3️⃣ 4️⃣ Resizing masses
 1️⃣ wind_turbine_inventory = "mass_model" > If you only know the power capacity of the turbine, you have nothing to do, the masses are calculated based on an implemented mass model
 
 2️⃣ wind_turbine_inventory = "user_mass_model" > If you know the aggregated masses of tower/rotor/nacelle, you can enter their values (or formula to calculate them)
 
 3️⃣ wind_turbine_inventory = "bill_of_materials" > If you know the bill of materials, you can enter the masses of materials
 
 4️⃣ wind_turbine_inventory = "custom" > If you get the whole inventory of the wind turbine, you can enter the bill of materials in this section and the whole inventory in the next section. Warning ! if you change material masses values, it shall be done using material masses variables (ex: mass_tower_steel_kg) as these mass values are reused in other parts of the model (eg for transport, maintenance, end of life)

```python
#Delete the # at the beginning of the line corresponding to the chosen level and put an # in front of the other lines

tower_wind_turbine_inventory = "mass_model"           #level 1
#tower_wind_turbine_inventory = "user_mass_model"            #level 2
#tower_wind_turbine_inventory = "bill_of_materials"          #Level 3
#tower_wind_turbine_inventory = "custom"                     #Level 4
```

```python
#Depending on the level selected, change the value of the variables in the dedicated section (except in level 1)

if tower_wind_turbine_inventory=="mass_model":
    # level 1: Calculation of the total mass of the tower based on Sacchi tower/rotor/nacelle mass model
    mass_tower_tot_kg=mass_tower_calc_kg
    
    #Automatic calculation : we assume material ratios in the tower are the same as in the reference inventory 
    resizing_mass_tower=mass_tower_tot_kg/MASS_TOWER_TOT_KG
    mass_tower_steel_kg=MASS_TOWER_STEEL_LOW_ALLOYED_KG*resizing_mass_tower
    mass_tower_alu_kg=MASS_TOWER_ALUMINIUM_KG*resizing_mass_tower

elif tower_wind_turbine_inventory=="user_mass_model":
    # Level 2 : Calculation of the total mass of the tower based on user mass model (formula or given value )
    mass_tower_tot_kg=0
    
    #Automatic calculation : we assume material ratios in the tower are the same as in the reference inventory 
    resizing_mass_tower=mass_tower_tot_kg/MASS_TOWER_TOT_KG
    mass_tower_steel_kg=MASS_TOWER_STEEL_LOW_ALLOYED_KG*resizing_mass_tower
    mass_tower_alu_kg=MASS_TOWER_ALUMINIUM_KG*resizing_mass_tower
    
    
elif tower_wind_turbine_inventory=="bill_of_materials":
    #Level 3 : if you have the masses of each material, enter the value of the masses
    mass_tower_steel_kg=0 #kg
    mass_tower_alu_kg=0 #kg
    
    #Automatic calculation of the total mass
    mass_tower_tot_kg=mass_tower_steel_kg+mass_tower_alu_kg
    resizing_mass_tower=mass_tower_tot_kg/MASS_TOWER_TOT_KG
    
elif tower_wind_turbine_inventory=="custom":
    #Level 4 : if you have the whole inventory of the wind turbine,  enter the value of the masses (and you will enter the new inventory in the next section)
    mass_tower_steel_kg=0 #kg
    mass_tower_alu_kg=0 #kg
    
    #Automatic calculation of the total mass
    mass_tower_tot_kg=mass_tower_steel_kg+mass_tower_alu_kg

```

```python
#Print a table with the masses of materials of the modeled tower
#function values_table is defined in "utils"
values_table(
    resizing_mass_tower=(resizing_mass_tower, " "),
    mass_tower_tot_kg=(mass_tower_tot_kg, "kg"),
    mass_tower_steel_kg=(mass_tower_steel_kg, "kg"),
    mass_tower_alu_kg=(mass_tower_alu_kg, "kg"))
```

#### 4️⃣ Resizing the inventory

```python
if tower_wind_turbine_inventory=="mass_model":
    #Level 1: Resized inventory : linear extrapolation based on the total mass of the tower
    tower_manufacturing_resized_1 = agb.newActivity(USER_DB,
                       "manufacturing of the tower of one wind turbine - reference inventory is resized based on implemented mass model",
                       unit = "unit",
                       exchanges = {tower_manufacturing_ref:resizing_mass_tower                         
             })   
    tower_manufacturing = tower_manufacturing_resized_1

elif tower_wind_turbine_inventory=="user_mass_model": 
    #Level 2 : Resized inventory : linear extrapolation based on the total mass of the tower
    tower_manufacturing_resized_2 = agb.newActivity(USER_DB,
                       "manufacturing of the tower of one wind turbine - reference inventory is resized based on user's mass model ",
                       unit = "unit",
                       exchanges = {tower_manufacturing_ref:resizing_mass_tower                           
             })
    tower_manufacturing = tower_manufacturing_resized_2

elif tower_wind_turbine_inventory=="bill_of_materials": 
    #Level 3 : Resized inventory : materials flows are recalculated based on user's bill oof materials, flows that are non related to materials are linearly extrapolated based on the total mass of the tower
    tower_manufacturing_resized_3 = agb.newActivity(USER_DB,
                       "manufacturing of the tower of one wind turbine - reference inventory is resized based on user's bill of materials ",
                       unit = "unit",
                       phase = PHASE_1_MANUFACTURING,
                       system_2=TOWER,
                       exchanges = {
                           steel_low_alloyed_mix: mass_tower_steel_kg, 
                           aluminium_mix :        mass_tower_alu_kg,                                               
                           electricity_UCTE:      resizing_mass_tower*TOWER_ELECTRICITY_kWH, 
                           diesel_process:        resizing_mass_tower*TOWER_DIESEL_MJ,
                           district_heating:      resizing_mass_tower*TOWER_HEATING_MJ, 
                           welding_gas:           resizing_mass_tower*TOWER_WELDING_GAS_M,
                           fuel_oil_process:      resizing_mass_tower*TOWER_FUEL_OIL_MJ,
                           wastewater_treatment:  resizing_mass_tower*TOWER_WASTEWATER_L,
                           waste_unspecified:     resizing_mass_tower*TOWER_WASTE_UNSPECIFIED_KG,
                           waste_hazardous:       resizing_mass_tower*TOWER_WASTE_HAZARDOUS_KG,
                           oil_waste:             resizing_mass_tower*TOWER_OIL_WASTE_KG,
             })

    tower_manufacturing = tower_manufacturing_resized_3
    
elif tower_wind_turbine_inventory=="custom":
    
    # Custom inventory

    #Level 4 : It is possible to customise other flows of the inventory (not only changing material masses)
    #but if you change material masses values, it shall be done using material masses variables in the previous section (ex: mass_tower_steel_kg)
    #as these mass values are reused in other parts of the model (eg for transport, maintenance, end of life)
    #if you add a new material, make sure to update the variables and their use in other life cycle stages

    tower_manufacturing_custom = agb.newActivity(USER_DB,
                       "manufacturing of the tower of one wind turbine - customized inventory",
                       unit = "unit",
                       phase = PHASE_1_MANUFACTURING,
                       system_2=TOWER,
                       exchanges = {
                           steel_low_alloyed_mix: mass_tower_steel_kg, 
                           aluminium_mix :        mass_tower_alu_kg,                                               
                           #add flows,
             })
    tower_manufacturing = tower_manufacturing_custom
    
agb.printAct(tower_manufacturing)
```

### Rotor = only blades


#### Reference inventory

```python
#Reference data for the blades (part of rotor)

#Mass of glass fiber in the rotor's blades
MASS_ROTOR_BLADES_GLASS_FIBER_KG =1315125/NUMBER_REF_TURBINE                                #kg
#Mass of epoxy in the rotor's blades
MASS_ROTOR_BLADES_EPOXY_KG = 519750/NUMBER_REF_TURBINE                                      #kg
#Mass of wood in the rotor's blades
MASS_ROTOR_BLADES_WOOD_MIX_KG = 96468.75/NUMBER_REF_TURBINE                                #kg
#Volume of wood in the rotor's blades
VOLUME_ROTOR_BLADES_WOOD_MIX_M3 = MASS_ROTOR_BLADES_WOOD_MIX_KG/DENSITY_PINEWOOD           #m3
#Mass of polypropylene in the rotor's blades
MASS_ROTOR_BLADES_POLYPROPYLENE_KG = 37406.25/NUMBER_REF_TURBINE                           #kg

#Total mass of the rotor's blades
MASS_ROTOR_BLADES_TOT_KG=MASS_ROTOR_BLADES_GLASS_FIBER_KG+MASS_ROTOR_BLADES_EPOXY_KG+MASS_ROTOR_BLADES_WOOD_MIX_KG+MASS_ROTOR_BLADES_POLYPROPYLENE_KG

#Amount of other flows
ROTOR_BLADES_WATER_KG = 2023875/NUMBER_REF_TURBINE                                    #kgMASS_ROTOR_BLADES_TOT_KG
ROTOR_BLADES_NATURAL_GAS_M3 = (675281.25/GAS_ENERGY_PER_VOLUME)/NUMBER_REF_TURBINE    #m3
ROTOR_BLADES_ELECTRICITY_kWH = 1350562.5/NUMBER_REF_TURBINE                    #kWh
ROTOR_BLADES_HEATING_MJ = 385875*KWH_TO_MJ/NUMBER_REF_TURBINE                        #MJ
```

```python
#Print a table with the masses of materials of the reference rotor
#function values_table is defined in "utils"

values_table(
    MASS_ROTOR_BLADES_TOT_KG=(MASS_ROTOR_BLADES_TOT_KG,"kg"),
    MASS_ROTOR_BLADES_GLASS_FIBER_KG=(MASS_ROTOR_BLADES_GLASS_FIBER_KG, "kg"),
    MASS_ROTOR_BLADES_EPOXY_KG=(MASS_ROTOR_BLADES_EPOXY_KG, "kg"),
    MASS_ROTOR_BLADES_WOOD_MIX_KG=(MASS_ROTOR_BLADES_WOOD_MIX_KG, "kg"),
    MASS_ROTOR_BLADES_POLYPROPYLENE_KG=(MASS_ROTOR_BLADES_POLYPROPYLENE_KG, "kg"))
```

```python
#We define the reference rotor blades manufacturing inventory based on data provided by Kouloumpis and Azapagic, 2022
rotor_blades_manufacturing_ref = agb.newActivity(USER_DB,
                       "manufacturing of the rotor's blades of one 5 MW reference turbine' ",
                       unit = "unit",
                       phase = PHASE_1_MANUFACTURING,
                       system_2= ROTOR,
                       exchanges = {
                           glass_fibre:MASS_ROTOR_BLADES_GLASS_FIBER_KG,
                           epoxy: MASS_ROTOR_BLADES_EPOXY_KG,
                           wood_mix: VOLUME_ROTOR_BLADES_WOOD_MIX_M3, 
                           polypropylene: MASS_ROTOR_BLADES_POLYPROPYLENE_KG,
                           
                           water: ROTOR_BLADES_WATER_KG,
                           natural_gas: ROTOR_BLADES_NATURAL_GAS_M3,
                           electricity_UCTE:ROTOR_BLADES_ELECTRICITY_kWH,
                           district_heating: ROTOR_BLADES_HEATING_MJ,

             })

#We define the reference rotor manufacturing inventory based on data provided by Kouloumpis and Azapagic, 2022
rotor_manufacturing_ref = agb.newActivity(USER_DB,
                       "manufacturing of the rotor of one 5 MW reference turbine",
                       unit = "unit",
                       exchanges = {
                           rotor_blades_manufacturing_ref:1,

             })

#Print the reference inventories
agb.printAct(rotor_blades_manufacturing_ref)
```

```python
# Explore the climate change impacts of the reference inventories 
agb.exploreImpacts(impacts_EF_CO2[0], rotor_blades_manufacturing_ref)
```

####  2️⃣ 3️⃣ 4️⃣ Resizing masses
 1️⃣ wind_turbine_inventory = "mass_model" > If you only know the power capacity of the turbine, you have nothing to do, the masses are calculated based on implemented mass model
 
 2️⃣ wind_turbine_inventory = "user_mass_model" > If you know the aggregated masses of tower/rotor/nacelle, you can enter their values (or formula to calculate them)
 
 3️⃣ wind_turbine_inventory = "bill_of_materials" > If you know the bill of materials, you can enter the masses of materials
 
 4️⃣ wind_turbine_inventory = "custom" > If you get the whole inventory of the wind turbine, you can enter the bill of materials in this section and the whole inventory in the next section. Warning ! if you change material masses values, it shall be done using material masses variables (ex: mass_tower_steel_kg) as these mass values are reused in other parts of the model (eg for transport, maintenance, end of life)

```python
rotor_wind_turbine_inventory = "mass_model"           #level 1
#rotor_wind_turbine_inventory = "user_mass_model"            #level 2
#rotor_wind_turbine_inventory = "bill_of_materials"          #Level 3
#rotor_wind_turbine_inventory = "custom"                     #Level 4
```

```python
if rotor_wind_turbine_inventory=="mass_model":
    # Level 1: Calculation of the total mass of the rotor based on implemented tower/rotor/nacelle mass model
    mass_rotor_tot_kg=mass_rotor_calc_kg
    
    #Automatic calculation : we assume material ratios in the rotor are the same as in the reference inventory 
    resizing_mass_rotor=mass_rotor_tot_kg/MASS_ROTOR_BLADES_TOT_KG
    mass_rotor_glass_fiber_kg=MASS_ROTOR_BLADES_GLASS_FIBER_KG*resizing_mass_rotor
    mass_rotor_epoxy_kg=MASS_ROTOR_BLADES_EPOXY_KG*resizing_mass_rotor
    mass_rotor_wood_mix_kg=MASS_ROTOR_BLADES_WOOD_MIX_KG*resizing_mass_rotor
    mass_rotor_polypropylene_kg=MASS_ROTOR_BLADES_POLYPROPYLENE_KG*resizing_mass_rotor

elif rotor_wind_turbine_inventory=="user_mass_model":
    # Level 2 : Calculation of the total mass of the rotor based on user mass model (formula or given value )
    mass_rotor_tot_kg=0
    
    #Automatic calculation : we assume material ratios in the rotor are the same as in the reference inventory 
    resizing_mass_rotor=mass_rotor_tot_kg/MASS_ROTOR_BLADES_TOT_KG
    mass_rotor_glass_fiber_kg=MASS_ROTOR_BLADES_GLASS_FIBER_KG*resizing_mass_rotor
    mass_rotor_epoxy_kg=MASS_ROTOR_BLADES_EPOXY_KG*resizing_mass_rotor
    mass_rotor_wood_mix_kg=MASS_ROTOR_BLADES_WOOD_MIX_KG*resizing_mass_rotor
    mass_rotor_polypropylene_kg=MASS_ROTOR_BLADES_POLYPROPYLENE_KG*resizing_mass_rotor
    
    
elif rotor_wind_turbine_inventory=="bill_of_materials":
    #Level 3 : if you have the masses of each material, enter the value of the masses
    mass_rotor_glass_fiber_kg=0 #kg
    mass_rotor_epoxy_kg=0 #kg
    mass_rotor_wood_mix_kg=0 #kg
    mass_rotor_polypropylene_kg=0 #kg
    
    #Automatic calculation of the total mass
    mass_rotor_tot_kg=mass_rotor_glass_fiber_kg+mass_rotor_epoxy_kg+mass_rotor_wood_mix_kg+mass_rotor_polypropylene_kg
    resizing_mass_rotor=mass_rotor_tot_kg/MASS_ROTOR_BLADES_TOT_KG
    
elif rotor_wind_turbine_inventory=="custom":
    #Level 4 : if you have the whole inventory of the wind turbine,  enter the value of the masses (and you will enter the new inventory in the next section)
    mass_rotor_glass_fiber_kg=0 #kg
    mass_rotor_epoxy_kg=0 #kg
    mass_rotor_wood_mix_kg=0 #kg
    mass_rotor_polypropylene_kg=0 #kg
    
    #Automatic calculation of the total mass
    mass_rotor_tot_kg=mass_rotor_glass_fiber_kg+mass_rotor_epoxy_kg+mass_rotor_wood_mix_kg+mass_rotor_polypropylene_kg
    resizing_mass_rotor=mass_rotor_tot_kg/MASS_ROTOR_BLADES_TOT_KG

```

```python
#Print a table with the masses of materials of the resized rotor
#function values_table is defined in "utils"

values_table(
    mass_rotor_tot_kg=(mass_rotor_tot_kg,"kg"),
    mass_rotor_glass_fiber_kg=(mass_rotor_glass_fiber_kg, "kg"),
    mass_rotor_epoxy_kg=(mass_rotor_glass_fiber_kg, "kg"),
    mass_rotor_wood_mix_kg=(mass_rotor_wood_mix_kg, "kg"),
    mass_rotor_polypropylene_kg=(mass_rotor_polypropylene_kg, "kg"))
```

#### 4️⃣ Resizing the inventory

```python
if rotor_wind_turbine_inventory=="mass_model":
    #Level 1: Resized inventory : linear extrapolation based on the total mass of the rotor
    rotor_manufacturing_resized_1 = agb.newActivity(USER_DB,
                       "manufacturing of the rotor of one wind turbine - reference inventory is resized based on implemented mass model",
                       unit = "unit",
                       exchanges = {rotor_manufacturing_ref:resizing_mass_rotor                          
             })
    rotor_manufacturing = rotor_manufacturing_resized_1

elif rotor_wind_turbine_inventory=="user_mass_model": 
    #Level 2 : Resized inventory : linear extrapolation based on the total mass of the rotor
    rotor_manufacturing_resized_2 = agb.newActivity(USER_DB,
                       "manufacturing of the rotor of one wind turbine - reference inventory is resized based on user's mass model ",
                       unit = "unit",
                       exchanges = {rotor_manufacturing_ref:resizing_mass_rotor                           
             })
    rotor_manufacturing = rotor_manufacturing_resized_2

elif rotor_wind_turbine_inventory=="bill_of_materials": 
    #Level 3 :Resized inventory : materials flows are recalculated based on user's bill of materials, flows that are non related to materials are linearly extrapolated based on the total mass of the rotor
    rotor_manufacturing_resized_3 = agb.newActivity(USER_DB,
                       "manufacturing of the rotor of one wind turbine - reference inventory is resized based on user's bill of materials ",
                       unit = "unit",
                       phase = PHASE_1_MANUFACTURING,
                       system_2=ROTOR,
                       exchanges = {
                           
                           glass_fibre:mass_rotor_glass_fiber_kg,
                           epoxy: mass_rotor_epoxy_kg,
                           wood_mix: mass_rotor_wood_mix_kg/DENSITY_PINEWOOD, 
                           polypropylene: mass_rotor_polypropylene_kg,
                           
                           water: resizing_mass_rotor*(ROTOR_BLADES_WATER_KG), 
                           natural_gas: resizing_mass_rotor*(ROTOR_BLADES_NATURAL_GAS_M3), 
                           electricity_UCTE:resizing_mass_rotor*(ROTOR_BLADES_ELECTRICITY_kWH),
                           district_heating: resizing_mass_rotor*ROTOR_BLADES_HEATING_MJ,
              })
                           
    rotor_manufacturing = rotor_manufacturing_resized_3
    
elif rotor_wind_turbine_inventory=="custom":
    
    # Custom inventory

    #Level 4 : It is possible to customise other flows of the inventory (not only changing material masses)
    #but if you change material masses values, it shall be done using material masses variables in the previous section (ex: mass_tower_steel_kg)
    #as these mass values are reused in other parts of the model (eg for transport, maintenance, end of life)
    #if you add a new material, make sure to update the variables and their use in other life cycle stages

    rotor_manufacturing_custom = agb.newActivity(USER_DB,
                       "manufacturing of the rotor of one wind turbine - customized inventory",
                       unit = "unit",
                       phase = PHASE_1_MANUFACTURING,
                       system_2=ROTOR,
                       exchanges = {
                           glass_fibre:mass_rotor_glass_fiber_kg,
                           epoxy: mass_rotor_epoxy_kg,
                           wood_mix: mass_rotor_wood_mix_kg/DENSITY_PINEWOOD, 
                           polypropylene: mass_rotor_polypropylene_kg,                                            
                           #add flows,
             })
    rotor_manufacturing = rotor_manufacturing_custom
    
agb.printAct(rotor_manufacturing)
```

### Nacelle


#### Reference inventory

```python
#Reference data for the hub (part of nacelle)

#Mass of cast iron in the rotor's hub
MASS_HUB_CAST_IRON_KG = 821156.25/NUMBER_REF_TURBINE                              #kg
#Mass of chromium steel in the rotor's hub
MASS_HUB_CHROMIUM_STEEL_KG = 479156.25/NUMBER_REF_TURBINE                          #kg
#Mass of steel low alloyed in the rotor's hub
MASS_HUB_STEEL_MIX_KG = 432843.75/NUMBER_REF_TURBINE                               #kg
#Mass of glass fiber in the rotor's hub
MASS_HUB_GLASS_FIBER_KG=49875/NUMBER_REF_TURBINE                                  #kg

#Total mass of the rotor's hub
MASS_HUB_TOT_KG=MASS_HUB_CAST_IRON_KG+MASS_HUB_CHROMIUM_STEEL_KG+MASS_HUB_STEEL_MIX_KG+MASS_HUB_GLASS_FIBER_KG

#Amount of other flows
HUB_ELECTRICITY_KWH = 2162437.5/NUMBER_REF_TURBINE                           #kWh
HUB_NATURAL_GAS_M3 = (890625/GAS_ENERGY_PER_VOLUME)/NUMBER_REF_TURBINE       #m3
HUB_WATER_KG = 778406.25/NUMBER_REF_TURBINE                                   #kg
HUB_SAND_KG = 7125000/NUMBER_REF_TURBINE                                      #kg

```

```python
#Reference data for the nacelle main body (NACELLE_MB)

#Mass of cast iron in the nacelle main body
MASS_NACELLE_MB_CAST_IRON_KG = 3900733.2/NUMBER_REF_TURBINE                  #kg
#Mass of steel low alloyed in the nacelle main body
MASS_NACELLE_MB_STEEL_MIX_KG = 3734035.2/NUMBER_REF_TURBINE                       #kg
#Mass of chromium steel in the nacelle main body
MASS_NACELLE_MB_CHROMIUM_STEEL_KG = 233377.2/NUMBER_REF_TURBINE                   #kg
#Mass of steel electric in the nacelle main body
MASS_NACELLE_MB_STEEL_ELECTRIC_KG = 208372.5/NUMBER_REF_TURBINE                   #kg
#Mass of copper in the nacelle main body
MASS_NACELLE_MB_COPPER_KG = 150028.2/NUMBER_REF_TURBINE                           #kg
#Mass of aluminium in the nacelle main body
MASS_NACELLE_MB_ALUMINIUM_MIX_KG = 108353.7/NUMBER_REF_TURBINE                    #kg

#Total mass of the nacelle main body
MASS_NACELLE_MB_TOT_KG=MASS_NACELLE_MB_CAST_IRON_KG+MASS_NACELLE_MB_STEEL_MIX_KG+MASS_NACELLE_MB_CHROMIUM_STEEL_KG+MASS_NACELLE_MB_STEEL_ELECTRIC_KG+MASS_NACELLE_MB_COPPER_KG+MASS_NACELLE_MB_ALUMINIUM_MIX_KG #kg

#Amount of other flows
NACELLE_MB_ELECTRICITY_UCTE_KWH = 1250235/NUMBER_REF_TURBINE                       #kWh
NACELLE_MB_NATURAL_GAS_MJ = 6870624.768/GAS_ENERGY_PER_VOLUME/NUMBER_REF_TURBINE  #m3

```

```python
#Reference data for the nacelle power/transformer unit (NACELLE_PTU)

#Mass of steel low alloyed in the nacelle power/transformer unit
MASS_NACELLE_PTU_STEEL_MIX_KG = 580967.1/NUMBER_REF_TURBINE                       #kg
#Mass of steel electric in the nacelle power/transformer unit
MASS_NACELLE_PTU_STEEL_ELECTRIC_KG = 217444.5/NUMBER_REF_TURBINE                  #kg
#Mass of copper in the nacelle power/transformer unit
MASS_NACELLE_PTU_COPPER_KG = 212984.1/NUMBER_REF_TURBINE                          #kg
#Mass of aluminium in the nacelle power/transformer unit
MASS_NACELLE_PTU_ALUMINIUM_MIX_KG = 60215.4/NUMBER_REF_TURBINE                    #kg
#Mass of polyethylene in the nacelle power/transformer unit
MASS_NACELLE_PTU_POLYETHYLENE_KG = 43488.9/NUMBER_REF_TURBINE                          #kg

#Total mass of the nacelle power/transformer unit
MASS_NACELLE_PTU_TOT_KG=MASS_NACELLE_PTU_STEEL_MIX_KG+MASS_NACELLE_PTU_STEEL_ELECTRIC_KG+MASS_NACELLE_PTU_COPPER_KG+MASS_NACELLE_PTU_ALUMINIUM_MIX_KG+MASS_NACELLE_PTU_POLYETHYLENE_KG

#Amount of other flows
NACELLE_PTU_COPPER_PROCESS_KG = MASS_NACELLE_PTU_COPPER_KG                               #kg
NACELLE_PTU_STEEL_PROCESS_KG = MASS_NACELLE_PTU_STEEL_MIX_KG + MASS_NACELLE_PTU_STEEL_ELECTRIC_KG                              #kg
```

```python
#Masses in the nacelle
MASS_NACELLE_CAST_IRON_KG=MASS_HUB_CAST_IRON_KG+MASS_NACELLE_MB_CAST_IRON_KG
MASS_NACELLE_STEEL_MIX_KG=MASS_HUB_STEEL_MIX_KG+MASS_NACELLE_MB_STEEL_MIX_KG+MASS_NACELLE_PTU_STEEL_MIX_KG+MASS_NACELLE_MB_STEEL_ELECTRIC_KG+MASS_NACELLE_PTU_STEEL_ELECTRIC_KG
MASS_NACELLE_CHROMIUM_STEEL_KG=MASS_HUB_CHROMIUM_STEEL_KG+MASS_NACELLE_MB_CHROMIUM_STEEL_KG
MASS_NACELLE_COPPER_KG=MASS_NACELLE_MB_COPPER_KG+MASS_NACELLE_PTU_COPPER_KG
MASS_NACELLE_ALUMINIUM_MIX_KG=MASS_NACELLE_MB_ALUMINIUM_MIX_KG+MASS_NACELLE_PTU_ALUMINIUM_MIX_KG
MASS_NACELLE_POLYETHYLENE_KG=MASS_NACELLE_PTU_POLYETHYLENE_KG
MASS_NACELLE_GLASS_FIBER_KG=MASS_HUB_GLASS_FIBER_KG

#Total mass of the nacelle
MASS_NACELLE_TOT_KG=MASS_NACELLE_CAST_IRON_KG+MASS_NACELLE_STEEL_MIX_KG+MASS_NACELLE_CHROMIUM_STEEL_KG+MASS_NACELLE_COPPER_KG+MASS_NACELLE_ALUMINIUM_MIX_KG+MASS_NACELLE_POLYETHYLENE_KG+MASS_NACELLE_GLASS_FIBER_KG
```

```python
#Print a table with the masses of materials of the reference nacelle
#function values_table is defined in "utils"

values_table(
   MASS_NACELLE_TOT_KG=(MASS_NACELLE_TOT_KG,"kg"),
   MASS_NACELLE_CAST_IRON_KG=(MASS_NACELLE_CAST_IRON_KG, "kg"),
   MASS_NACELLE_STEEL_MIX_KG=(MASS_NACELLE_STEEL_MIX_KG, "kg"),
   MASS_NACELLE_CHROMIUM_STEEL_KG=(MASS_NACELLE_CHROMIUM_STEEL_KG, "kg"),
   MASS_NACELLE_COPPER_KG=(MASS_NACELLE_COPPER_KG, "kg"),
   MASS_NACELLE_ALUMINIUM_MIX_KG=(MASS_NACELLE_ALUMINIUM_MIX_KG, "kg"),
   MASS_NACELLE_POLYETHYLENE_KG=(MASS_NACELLE_POLYETHYLENE_KG, "kg"))

```

```python
#We define the reference hub manufacturing inventory based on data provided by Kouloumpis and Azapagic, 2022
nacelle_hub_manufacturing_ref = agb.newActivity(USER_DB,
                       "manufacturing of the hub of one 5 MW reference turbine' ",
                       unit = "unit",                       
                       phase = PHASE_1_MANUFACTURING,
                       system_2= NACELLE,
                       exchanges = {
                           cast_iron: MASS_HUB_CAST_IRON_KG,
                           chromium_steel: MASS_HUB_CHROMIUM_STEEL_KG,
                           steel_low_alloyed_mix: MASS_HUB_STEEL_MIX_KG,
                           glass_fibre:MASS_HUB_GLASS_FIBER_KG,
                           
                           electricity_UCTE:HUB_ELECTRICITY_KWH,
                           natural_gas:HUB_NATURAL_GAS_M3,
                           water:HUB_WATER_KG,
                           sand: HUB_SAND_KG,
                        
             })


#We define the reference nacelle main body manufacturing inventory based on data provided by Kouloumpis and Azapagic, 2022
nacelle_main_body_manufacturing_ref = agb.newActivity(USER_DB,
                       "manufacturing of the nacelle main body of one 5 MW reference turbine' ",
                       unit = "unit",
                       phase = PHASE_1_MANUFACTURING,
                       system_2=NACELLE,
                       exchanges = {
                           cast_iron: MASS_NACELLE_MB_CAST_IRON_KG, 
                           steel_low_alloyed_mix: MASS_NACELLE_MB_STEEL_MIX_KG+MASS_NACELLE_MB_STEEL_ELECTRIC_KG, 
                           chromium_steel: MASS_NACELLE_MB_CHROMIUM_STEEL_KG,
                           copper: MASS_NACELLE_MB_COPPER_KG,
                           aluminium_mix: MASS_NACELLE_MB_ALUMINIUM_MIX_KG,

                           electricity_UCTE: NACELLE_MB_ELECTRICITY_UCTE_KWH,
                           natural_gas: NACELLE_MB_NATURAL_GAS_MJ,
                       })

#We define the reference nacelle power/transformer unit inventory based on data provided by Kouloumpis and Azapagic, 2022
nacelle_ptu_manufacturing_ref = agb.newActivity(USER_DB,
                       "manufacturing of the  nacelle power/transformer unit of one 5 MW reference turbine' ",
                       unit = "unit",                       
                       phase = PHASE_1_MANUFACTURING,
                       system_2=NACELLE,
                       exchanges = {
                           steel_low_alloyed_mix: MASS_NACELLE_PTU_STEEL_MIX_KG+MASS_NACELLE_PTU_STEEL_ELECTRIC_KG, 
                           copper: MASS_NACELLE_PTU_COPPER_KG,
                           aluminium_mix: MASS_NACELLE_PTU_ALUMINIUM_MIX_KG,
                           polyethylene_HD: MASS_NACELLE_PTU_POLYETHYLENE_KG,

                           copper_process: NACELLE_PTU_COPPER_PROCESS_KG,
                           steel_process: NACELLE_PTU_STEEL_PROCESS_KG,
                        
             })

#We define the reference nacelle inventory based on data provided by Kouloumpis and Azapagic, 2022
nacelle_manufacturing_ref = agb.newActivity(USER_DB,
                       "manufacturing of the nacelle of one 5 MW reference turbine' ",
                       unit = "unit", 
                       exchanges = {
                           nacelle_hub_manufacturing_ref:1,
                           nacelle_main_body_manufacturing_ref:1,
                           nacelle_ptu_manufacturing_ref:1,

             })

#Print the reference inventories
agb.printAct(nacelle_hub_manufacturing_ref)
agb.printAct(nacelle_main_body_manufacturing_ref)
agb.printAct(nacelle_ptu_manufacturing_ref)
```

```python
# Explore the climate change impacts of the reference inventories 
agb.exploreImpacts(impacts_EF_CO2[0], nacelle_hub_manufacturing_ref)
agb.exploreImpacts(impacts_EF_CO2[0], nacelle_main_body_manufacturing_ref)
agb.exploreImpacts(impacts_EF_CO2[0], nacelle_ptu_manufacturing_ref)
```

####  2️⃣ 3️⃣ 4️⃣ Resizing masses
 1️⃣ wind_turbine_inventory = "mass_model" > If you only know the power capacity of the turbine, you have nothing to do, the masses are calculated based on implemented mass model
 
 2️⃣ wind_turbine_inventory = "user_mass_model" > If you know the aggregated masses of tower/rotor/nacelle, you can enter their values (or formula to calculate them)
 
 3️⃣ wind_turbine_inventory = "bill_of_materials" > If you know the bill of materials, you can enter the masses of materials
 
 4️⃣ wind_turbine_inventory = "custom" > If you get the whole inventory of the wind turbine, you can enter the bill of materials in this section and the whole inventory in the next section. Warning ! if you change material masses values, it shall be done using material masses variables (ex: mass_tower_steel_kg) as these mass values are reused in other parts of the model (eg for transport, maintenance, end of life)

```python
nacelle_wind_turbine_inventory = "mass_model"           #level 1
#nacelle_wind_turbine_inventory = "user_mass_model"            #level 2
#nacelle_wind_turbine_inventory = "bill_of_materials"          #Level 3
#nacelle_wind_turbine_inventory = "custom"                     #Level 4
```

```python
if nacelle_wind_turbine_inventory=="mass_model":
    # Level 1: Calculation of the total mass of the nacelle based on implemented tower/rotor/nacelle mass model
    mass_nacelle_tot_kg=mass_nacelle_calc_kg
    
    #Automatic calculation : we assume material ratios in the nacelle are the same as in the reference inventory 
    resizing_mass_nacelle=mass_nacelle_tot_kg/MASS_NACELLE_TOT_KG
    mass_nacelle_cast_iron_kg=MASS_NACELLE_CAST_IRON_KG*resizing_mass_nacelle
    mass_nacelle_steel_mix_kg=MASS_NACELLE_STEEL_MIX_KG/MASS_NACELLE_TOT_KG*resizing_mass_nacelle
    mass_nacelle_chromium_steel_kg=MASS_NACELLE_CHROMIUM_STEEL_KG*resizing_mass_nacelle
    mass_nacelle_copper_kg=MASS_NACELLE_COPPER_KG*resizing_mass_nacelle
    mass_nacelle_aluminium_mix_kg=MASS_NACELLE_ALUMINIUM_MIX_KG*resizing_mass_nacelle
    mass_nacelle_polyethylene_kg=MASS_NACELLE_POLYETHYLENE_KG*resizing_mass_nacelle
    mass_nacelle_glass_fiber_kg=MASS_NACELLE_GLASS_FIBER_KG*resizing_mass_nacelle
    
elif nacelle_wind_turbine_inventory=="user_mass_model":
    # Level 2 : Calculation of the total mass of the nacelle based on user mass model (formula or given value )
    mass_nacelle_tot_kg=0
    
    #Automatic calculation : we assume material ratios in the nacelle are the same as in the reference inventory 
    resizing_mass_nacelle=mass_nacelle_tot_kg/MASS_NACELLE_TOT_KG
    mass_nacelle_cast_iron_kg=MASS_NACELLE_CAST_IRON_KG*resizing_mass_nacelle
    mass_nacelle_steel_mix_kg=MASS_NACELLE_STEEL_MIX_KG/MASS_NACELLE_TOT_KG*resizing_mass_nacelle
    mass_nacelle_chromium_steel_kg=MASS_NACELLE_CHROMIUM_STEEL_KG*resizing_mass_nacelle
    mass_nacelle_copper_kg=MASS_NACELLE_COPPER_KG*resizing_mass_nacelle
    mass_nacelle_aluminium_mix_kg=MASS_NACELLE_ALUMINIUM_MIX_KG*resizing_mass_nacelle
    mass_nacelle_polyethylene_kg=MASS_NACELLE_POLYETHYLENE_KG*resizing_mass_nacelle
    mass_nacelle_glass_fiber_kg=MASS_NACELLE_GLASS_FIBER_KG*resizing_mass_nacelle    
    
elif nacelle_wind_turbine_inventory=="bill_of_materials":
    #Level 3 : if you have the masses of each material, enter the value of the masses
    mass_nacelle_cast_iron_kg= 0 #kg
    mass_nacelle_mb_steel_mix_kg=0 #kg
    mass_nacelle_ptu_steel_mix_kg=0 #kg
    mass_nacelle_steel_mix_kg= mass_nacelle_mb_steel_mix_kg+mass_nacelle_ptu_steel_mix_kg 

    mass_nacelle_chromium_steel_kg=0 #kg

    mass_nacelle_mb_copper_kg=0 #kg
    mass_nacelle_ptu_copper_kg=0 #kg
    mass_nacelle_copper_kg=mass_nacelle_ptu_copper_kg+mass_nacelle_mb_copper_kg

    mass_nacelle_aluminium_mix_kg=0 #kg
    mass_nacelle_polyethylene_kg=0 #kg
    mass_nacelle_glass_fiber_kg=0 #kg
    
    #Automatic calculation of the total mass
    mass_nacelle_tot_kg=mass_nacelle_cast_iron_kg+mass_nacelle_chromium_steel_kg+mass_nacelle_copper_kg+mass_nacelle_aluminium_mix_kg+mass_nacelle_polyethylene_kg+mass_nacelle_glass_fiber_kg
    resizing_mass_nacelle=mass_nacelle_tot_kg/MASS_NACELLE_TOT_KG
    
elif nacelle_wind_turbine_inventory=="custom":
    #Level 4 : if you have the whole inventory of the wind turbine,  enter the value of the masses (and you will enter the new inventory in the next section)
    mass_nacelle_cast_iron_kg= 0 #kg
    mass_nacelle_mb_steel_mix_kg=0 #kg
    mass_nacelle_ptu_steel_mix_kg=0 #kg
    mass_nacelle_steel_mix_kg= mass_nacelle_mb_steel_mix_kg+mass_nacelle_ptu_steel_mix_kg 

    mass_nacelle_chromium_steel_kg=0 #kg

    mass_nacelle_mb_copper_kg=0 #kg
    mass_nacelle_ptu_copper_kg=0 #kg
    mass_nacelle_copper_kg=mass_nacelle_ptu_copper_kg+mass_nacelle_mb_copper_kg

    mass_nacelle_aluminium_mix_kg=0 #kg
    mass_nacelle_polyethylene_kg=0 #kg
    mass_nacelle_glass_fiber_kg=0 #kg
    #add flows

    #Automatic calculation of the total mass
    mass_nacelle_tot_kg=mass_nacelle_cast_iron_kg+mass_nacelle_chromium_steel_kg+mass_nacelle_copper_kg+mass_nacelle_aluminium_mix_kg+mass_nacelle_polyethylene_kg+mass_nacelle_glass_fiber_kg
    resizing_mass_nacelle=mass_nacelle_tot_kg/MASS_NACELLE_TOT_KG

```

```python
#Print a table with the masses of materials of the resized nacelle
#function values_table is defined in "utils"

values_table(
   mass_nacelle_tot_kg=(mass_nacelle_tot_kg,"kg"),
   mass_nacelle_cast_iron_kg=(mass_nacelle_cast_iron_kg, "kg"),
   mass_nacelle_steel_mix_kg=(mass_nacelle_steel_mix_kg, "kg"),
   mass_nacelle_chromium_steel_kg=(mass_nacelle_chromium_steel_kg, "kg"),
   mass_nacelle_copper_kg=(mass_nacelle_copper_kg, "kg"),
   mass_nacelle_aluminium_mix_kg=(mass_nacelle_aluminium_mix_kg, "kg"),
   mass_nacelle_polyethylene_kg=(mass_nacelle_polyethylene_kg, "kg"),
   mass_nacelle_glass_fiber_kg=(mass_nacelle_glass_fiber_kg,"kg"))

```

#### 4️⃣ Resizing the inventory

```python
if nacelle_wind_turbine_inventory=="mass_model":
    # Level 1: Resized inventory : linear extrapolation based on the total mass of the nacelle
    nacelle_manufacturing_resized_1 = agb.newActivity(USER_DB,
                       "manufacturing of the nacelle of one wind turbine - reference inventory is resized based on implemented mass model",
                       unit = "unit",
                       exchanges = {nacelle_manufacturing_ref:resizing_mass_nacelle                        
             })
    nacelle_manufacturing = nacelle_manufacturing_resized_1

elif nacelle_wind_turbine_inventory=="user_mass_model": 
    #Level 2 : Resized inventory : linear extrapolation based on the total mass of the nacelle
    nacelle_manufacturing_resized_2 = agb.newActivity(USER_DB,
                       "manufacturing of the nacelle of one wind turbine - reference inventory is resized based on user's mass model ",
                       unit = "unit",
                       exchanges = {nacelle_manufacturing_ref:resizing_mass_nacelle                           
             })
    nacelle_manufacturing = nacelle_manufacturing_resized_2

elif nacelle_wind_turbine_inventory=="bill_of_materials": 
    #Level 3 :Resized inventory : materials flows are recalculated based on user's bill of materials, flows that are non related to materials are linearly extrapolated based on the total mass of the rotor
    nacelle_manufacturing_resized_3 = agb.newActivity(USER_DB,
                       "manufacturing of the nacelle of one wind turbine - reference inventory is resized based on user's bill of materials ",
                       unit = "unit",
                       phase = PHASE_1_MANUFACTURING,
                       system_2=NACELLE,
                       exchanges = {
                           
                           cast_iron: mass_nacelle_cast_iron_kg, 
                           steel_low_alloyed_mix: mass_nacelle_steel_mix_kg, 
                           chromium_steel: mass_nacelle_chromium_steel_kg,
                           copper: mass_nacelle_copper_kg,
                           aluminium_mix : mass_nacelle_aluminium_mix_kg,
                           polyethylene_HD: mass_nacelle_polyethylene_kg,
                           
                           copper_process: mass_nacelle_ptu_copper_kg,
                           steel_process: mass_nacelle_ptu_steel_mix_kg,
                           
                           water: resizing_mass_nacelle*HUB_WATER_KG,
                           electricity_UCTE: resizing_mass_nacelle*(NACELLE_MB_ELECTRICITY_UCTE_KWH+HUB_ELECTRICITY_KWH),
                           natural_gas: resizing_mass_nacelle*(NACELLE_MB_NATURAL_GAS_MJ+HUB_NATURAL_GAS_M3),
                           sand: resizing_mass_rotor*HUB_SAND_KG,

              })                           
    nacelle_manufacturing = nacelle_manufacturing_resized_3
    
elif nacelle_wind_turbine_inventory=="custom":
    
    # Custom inventory

    #Level 4 : It is possible to customise other flows of the inventory (not only changing material masses)
    #but if you change material masses values, it shall be done using material masses variables in the previous section (ex: mass_tower_steel_kg)
    #as these mass values are reused in other parts of the model (eg for transport, maintenance, end of life)
    #if you add a new material, make sure to update the variables and their use in other life cycle stages

    nacelle_manufacturing_custom = agb.newActivity(USER_DB,
                       "manufacturing of the nacelle of one wind turbine - customized inventory",
                       unit = "unit",
                       phase = PHASE_1_MANUFACTURING,
                       system_2=NACELLE,
                       exchanges = {
                           cast_iron: mass_nacelle_cast_iron_kg, 
                           steel_low_alloyed_mix: mass_nacelle_steel_mix_kg, 
                           chromium_steel: mass_nacelle_chromium_steel_kg,
                           copper: mass_nacelle_copper_kg,
                           aluminium_mix : mass_nacelle_aluminium_mix_kg,
                           polyethylene_HD: mass_nacelle_polyethylene_kg,
                           
                           copper_process: mass_nacelle_ptu_copper_kg,
                           steel_process: mass_nacelle_ptu_steel_mix_kg,                                              
                           #add flows,
             })
    nacelle_manufacturing = nacelle_manufacturing_custom
    
agb.printAct(nacelle_manufacturing)
```

### Assembly of windturbines


#### One wind turbine assembly

```python
mass_one_wind_turbine_tot_kg=mass_tower_tot_kg+mass_rotor_tot_kg+mass_nacelle_tot_kg

values_table(
    mass_tower_tot_kg=(mass_tower_tot_kg,"kg"),
    mass_rotor_tot_kg=(mass_rotor_tot_kg,"kg"),
    mass_nacelle_tot_kg=(mass_nacelle_tot_kg,"kg"),
    mass_one_wind_turbine_tot_kg=(mass_one_wind_turbine_tot_kg,"kg")
)
```

```python
# We introduce an activity for one wind turbine that is composed of tower, rotor and nacelle

one_wind_turbine_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of one windturbine",
                       unit = "unit",
                       phase = PHASE_1_MANUFACTURING,
                       system_1 = WIND_TURBINES,  
                       exchanges = {
                           tower_manufacturing:1,
                           rotor_manufacturing:1,
                           nacelle_manufacturing:1
                          })
```

#### Wind Turbines 

```python
# We introduce an activity for all the wind turbines of the wind farm

wind_turbines_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of windturbines of the farm",
                       unit = "unit",
                       exchanges = {
                          one_wind_turbine_manufacturing:n_turbines
                          })

agb.printAct(wind_turbines_manufacturing)
```

#### LCA RESULT: climate change impacts of wind turbine manufacturing
As most of the impacts come from manufacturing step, we do intermediate calculation to visualise the climate change impact due to manufacturing of each subsystem.
Impacts are calculated 
* for the whole infrastructure
* per MW of installed capacity
* per kWh of electricity produced

```python
#Climate change impact of the whole infrastructure
compute_impacts(
    wind_turbines_manufacturing,
    impacts_EF_CO2,
    axis="system_2"
)
```

```python
#Climate change impact per MW installed
#We use the function compute_impacts to resize the inventory (division per power_tot_farm_MW)
compute_impacts(
    wind_turbines_manufacturing,
    impacts_EF_CO2,
    functional_unit=power_tot_farm_MW,
    axis="system_2"
)
```

```python
#Climate change impact per kWh of electricity produced
#We use the function compute_impacts to resize the inventory (division per elec_prod_lifetime_kWh)
compute_impacts(
    wind_turbines_manufacturing,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh,
    axis="system_2")
```

## Wind turbine foundations


Both fixed and floating foundations are included in the current version of LIF-OWI parameterized modeled.

* Among fixed foundations, three types are available: ground-based, monopile and tripodal.
* The only floating foundation modeled is a spar technology.

Estimates of input flows to the manufacturing processes of foundations were based on data provided by [Tsai et al. 2016](https://onlinelibrary.wiley.com/doi/10.1111/jiec.12400) for fixed foundations of 3 MW wind turbines and Weinzettel et al., 2008 for a spar floating foundations of 5 MW wind turbines.


### Reference inventories

```python
# Reference data for fixed foundations
FIXED_FOUNDATION_REF_POWER_MW = 3 #MW
GBF_REF_WATER_DEPTH_M = 15 #m
MONOPILE_REF_WATER_DEPTH_M = 20 #m
TRIPOD_REF_WATER_DEPTH_M = 35 #m

# Reference data for floating foundations
SPAR_FOUNDATION_REF_POWER_MW = 5 #MW
SPAR_REF_WATER_DEPTH_M = 200 #m
SUBMERGED_PART_LENGTH = 100 #m
```

#### Gravity -based foundations 

```python
#Reference: fixed gravity-based foundation at water depth of 15 meters as the base case (Tsai et al, 2016, SI)
MASS_FOUNDATION_GBF_STEEL_REINFORCING_KG = 336000   #kg
VOLUME_FOUNDATION_GBF_CONCRETE_M3 = 1027  #m3     # in the reference inventory, the data is given in m3  
MASS_FOUNDATION_GBF_CONCRETE_KG = VOLUME_FOUNDATION_GBF_CONCRETE_M3*CONCRETE_DENSITY #kg
MASS_FOUNDATION_GBF_GRAVEL_KG = 12200000  #kg
MASS_FOUNDATION_GBF_TOT_KG = MASS_FOUNDATION_GBF_STEEL_REINFORCING_KG + MASS_FOUNDATION_GBF_CONCRETE_KG + MASS_FOUNDATION_GBF_GRAVEL_KG  #kg
```

```python
#Print a table with the masses of materials of the reference gravity based foundations
values_table(
    MASS_FOUNDATION_GBF_TOT_KG=(MASS_FOUNDATION_GBF_TOT_KG, "kg"),
    MASS_FOUNDATION_GBF_STEEL_REINFORCING_KG=(MASS_FOUNDATION_GBF_STEEL_REINFORCING_KG,"kg"),
    MASS_FOUNDATION_GBF_CONCRETE_KG=(MASS_FOUNDATION_GBF_CONCRETE_KG, "kg"),
    MASS_FOUNDATION_GBF_GRAVEL_KG=(MASS_FOUNDATION_GBF_GRAVEL_KG, "kg"))
```

```python
#We define the reference manufacturing inventory for gravity based foundations based on data provided by Tsai et al, 2016
one_foundation_gbf_manufacturing_ref = agb.newActivity(USER_DB,
                                "manufacturing of one gravity based foundations at depth 15m for a 3 MW wind turbine",
                                 unit = "unit",
                                 phase = PHASE_1_MANUFACTURING,
                                 system_1 = WT_FOUNDATIONS,
                                exchanges = {
                                    steel_reinforcing:MASS_FOUNDATION_GBF_STEEL_REINFORCING_KG,
                                    concrete: VOLUME_FOUNDATION_GBF_CONCRETE_M3,
                                    gravel: MASS_FOUNDATION_GBF_GRAVEL_KG,
                                })
#Print the reference inventory
agb.printAct(one_foundation_gbf_manufacturing_ref)
```

#### Monopile Foundations

```python
#Reference: monopile fixed foundation at water depth of 20 meters as the base case (Tsai et al, 2016, SI)
MASS_FOUNDATION_MONOPILE_STEEL_MIX_KG = (276000+169500)  #kg
FOUNDATION_MONOPILE_STEEL_PROCESS_KG = MASS_FOUNDATION_MONOPILE_STEEL_MIX_KG   #kg
MASS_FOUNDATION_MONOPILE_CONCRETE_KG = 21300            #kg # in the reference inventory, the data is given in mass not in volume 
VOLUME_FOUNDATION_MONOPILE_CONCRETE_M3 = MASS_FOUNDATION_MONOPILE_CONCRETE_KG/CONCRETE_DENSITY  #m3  
MASS_FOUNDATION_MONOPILE_TOT_KG = MASS_FOUNDATION_MONOPILE_STEEL_MIX_KG+MASS_FOUNDATION_MONOPILE_CONCRETE_KG #kg
```

```python
#Print a table with the masses of materials of the reference monopile foundations
values_table(
    MASS_FOUNDATION_MONOPILE_TOT_KG=(MASS_FOUNDATION_MONOPILE_TOT_KG, "kg"),
    MASS_FOUNDATION_MONOPILE_STEEL_MIX_KG=(MASS_FOUNDATION_MONOPILE_STEEL_MIX_KG,"kg"),
    MASS_FOUNDATION_MONOPILE_CONCRETE_KG=(MASS_FOUNDATION_MONOPILE_CONCRETE_KG, "kg"))
```

```python
#We define the reference manufacturing inventory for monopile foundations based on data provided by Tsai et al, 2016
one_foundation_monopile_manufacturing_ref = agb.newActivity(USER_DB,
                                      "manufacturing of one monopile foundations at depth 20 m for a 3 MW wind turbine",
                                      unit = 'unit',
                                      phase = PHASE_1_MANUFACTURING,
                                      system_1 = WT_FOUNDATIONS,
                                      exchanges = {
                                          steel_low_alloyed_mix: MASS_FOUNDATION_MONOPILE_STEEL_MIX_KG,
                                          concrete: VOLUME_FOUNDATION_MONOPILE_CONCRETE_M3,
                                          steel_process : FOUNDATION_MONOPILE_STEEL_PROCESS_KG                                          
                                      })

#Print the reference inventory
agb.printAct(one_foundation_monopile_manufacturing_ref)
```

#### Tripod foundations

```python
#Reference: tripod fixed foundation at water depth of 35 meters as the base case (Tsai et al, 2016, SI)
MASS_FOUNDATION_TRIPOD_STEEL_MIX_KG = (807000+847000)  #kg
FOUNDATION_TRIPOD_STEEL_PROCESS_KG = MASS_FOUNDATION_TRIPOD_STEEL_MIX_KG    #kg
MASS_FOUNDATION_TRIPOD_CONCRETE_KG = 63900 #kg # in the reference inventory, the data is given in kg
VOLUME_FOUNDATION_TRIPOD_CONCRETE_M3 = MASS_FOUNDATION_MONOPILE_CONCRETE_KG/CONCRETE_DENSITY #m3
MASS_FOUNDATION_TRIPOD_TOT_KG = MASS_FOUNDATION_TRIPOD_STEEL_MIX_KG+MASS_FOUNDATION_MONOPILE_CONCRETE_KG #kg
```

```python
values_table(
    MASS_FOUNDATION_TRIPOD_TOT_KG=(MASS_FOUNDATION_TRIPOD_TOT_KG,"kg"),
    MASS_FOUNDATION_TRIPOD_STEEL_MIX_KG=(MASS_FOUNDATION_TRIPOD_STEEL_MIX_KG, "kg"),
    MASS_FOUNDATION_TRIPOD_CONCRETE_KG=(MASS_FOUNDATION_TRIPOD_CONCRETE_KG, "kg"))
```

```python
#We define the reference manufacturing inventory for tripod foundations based on data provided by Tsai et al, 2016
one_foundation_tripod_manufacturing_ref = agb.newActivity(USER_DB,
                                   'manufacturing of one tripod foundations at depth 35 m for a 3 MW wind turbine',
                                      unit = 'unit',
                                      phase = PHASE_1_MANUFACTURING,
                                      system_1 = WT_FOUNDATIONS,
                                   exchanges = {
                                       steel_low_alloyed_mix:      MASS_FOUNDATION_TRIPOD_STEEL_MIX_KG,
                                       steel_process : FOUNDATION_TRIPOD_STEEL_PROCESS_KG,
                                       concrete:       VOLUME_FOUNDATION_TRIPOD_CONCRETE_M3,
                                   })

#Print the reference inventory
agb.printAct(one_foundation_tripod_manufacturing_ref)
```

#### Jacket foundations

```python
# The jacket foundation is assumed being only made of steel. There is no reference inventory as it is directly calculated by our own model.
```

#### Floating spar foundations

```python
#Reference: spar floating foundations at water depth 200 m (Weinzettel et al, 2008)
# water depth shall be at least 100 m for using this foundation technology. 
MASS_FOUNDATION_SPAR_STEEL_LOW_ALLOYED_KG = 1000000/2 #/2 to model only the immersed part
MASS_FOUNDATION_SPAR_STEEL_HIGH_ALLOYED_KG=5000/2  #kg #/2 to model only the immersed part
FOUNDATION_SPAR_STEEL_PROCESS_KG = MASS_FOUNDATION_SPAR_STEEL_LOW_ALLOYED_KG+MASS_FOUNDATION_SPAR_STEEL_HIGH_ALLOYED_KG  #kg #there is no process for high alloyed steel in ecoinvent
MASS_FOUNDATION_SPAR_GRAVEL_BALLAST_KG = 2500000 #kg
MASS_FOUNDATION_SPAR_GRAVEL_MOORING_KG = 500000 #kg
MASS_FOUNDATION_SPAR_TOT_KG = MASS_FOUNDATION_SPAR_STEEL_LOW_ALLOYED_KG+MASS_FOUNDATION_SPAR_STEEL_HIGH_ALLOYED_KG+MASS_FOUNDATION_SPAR_GRAVEL_BALLAST_KG+MASS_FOUNDATION_SPAR_GRAVEL_MOORING_KG  #kg
```

```python
values_table(
    MASS_FOUNDATION_SPAR_TOT_KG=(MASS_FOUNDATION_SPAR_TOT_KG,"kg"),
    MASS_FOUNDATION_SPAR_STEEL_LOW_ALLOYED_KG=(MASS_FOUNDATION_SPAR_STEEL_LOW_ALLOYED_KG, "kg"),
    MASS_FOUNDATION_SPAR_STEEL_HIGH_ALLOYED_KG=(MASS_FOUNDATION_SPAR_STEEL_HIGH_ALLOYED_KG, "kg"),
    MASS_FOUNDATION_SPAR_GRAVEL_BALLAST_KG=(MASS_FOUNDATION_SPAR_GRAVEL_BALLAST_KG, "kg"),
    MASS_FOUNDATION_SPAR_GRAVEL_MOORING_KG=(MASS_FOUNDATION_SPAR_GRAVEL_MOORING_KG, "kg"))
```

```python
#We define the reference manufacturing inventory for spar floating foundations based on data provided by Weinzettel et al. 2008
one_foundation_spar_manufacturing_ref = agb.newActivity(USER_DB,
                                     'manufacturing of one floating spar foundations at depth 200 m for a 5 MW wind turbine',
                                      unit = 'unit',
                                      phase = PHASE_1_MANUFACTURING,
                                      system_1 = WT_FOUNDATIONS,
                                     exchanges = {
                                         steel_low_alloyed_mix: MASS_FOUNDATION_SPAR_STEEL_LOW_ALLOYED_KG+MASS_FOUNDATION_SPAR_STEEL_HIGH_ALLOYED_KG,
                                         steel_process: FOUNDATION_SPAR_STEEL_PROCESS_KG,
                                         gravel: MASS_FOUNDATION_SPAR_GRAVEL_BALLAST_KG+MASS_FOUNDATION_SPAR_GRAVEL_MOORING_KG,    
                                     })
#Print the reference inventory
agb.printAct(one_foundation_spar_manufacturing_ref)
```

#### Floating semi submersible foundations

```python
# The semi-submersible foundation is assumed being only made of steel. There is no reference inventory as it is directly calculated by our own model.
```

####  2️⃣ 3️⃣ 4️⃣ Resizing masses
 1️⃣ foundation_inventory = "automatised_mass_model" > If you only know the water depth, the submerged height of foundation and the wind turbine power capacity, you have nothing to do, the masses are calculated based on a simplified mass model (based on linear extrapolation and/or model computed with online collected data)
 
 2️⃣ foundation_inventory = "user_mass_model" > If you know the aggregated masses of foundations, you can enter their values (or formula to calculate them)
 
 3️⃣4️⃣ this levels are included in the custom inventory

```python
foundations_inventory = "automatised_mass_model"              #level 1
#foundations_inventory = "user_mass_model"            #level 2
```

**Foundations mass model**

```python
#We assume the emerged part of the foundations is :
emerged_height_m=20 #m

#We assume the mass one pile for jacket foundations is constant equal to : 
mass_pile_jacket_kg=62000 #kg 
```

```python
# Calculation of the total mass of the wind turbine foundations, function of water_depth, submerged_height and turbine_MW
# GBF
mass_foundations_gbf_calc_kg=MASS_FOUNDATION_GBF_TOT_KG*(water_depth+emerged_height_m)/(GBF_REF_WATER_DEPTH_M+emerged_height_m)*(turbine_MW/FIXED_FOUNDATION_REF_POWER_MW)
#MONOPILE
mass_foundations_monopile_calc_kg=MASS_FOUNDATION_MONOPILE_TOT_KG*(water_depth+emerged_height_m)/(MONOPILE_REF_WATER_DEPTH_M+emerged_height_m)*(turbine_MW/FIXED_FOUNDATION_REF_POWER_MW)
#TRIPOD
mass_foundations_tripod_calc_kg=MASS_FOUNDATION_TRIPOD_TOT_KG*(water_depth+emerged_height_m)/(TRIPOD_REF_WATER_DEPTH_M+emerged_height_m)*(turbine_MW/FIXED_FOUNDATION_REF_POWER_MW)
#JACKET
mass_foundations_jacket_calc_kg=lineic_mass_foundations_jacket_calc_kg_per_m*(water_depth+emerged_height_m)+mass_pile_jacket_kg*4
#FLOATING SPAR
mass_foundations_spar_calc_kg=MASS_FOUNDATION_SPAR_TOT_KG*(turbine_MW/SPAR_FOUNDATION_REF_POWER_MW)
#FLOATING SEMI-SUBMERSIBLE
mass_foundations_semisub_calc_kg=lineic_mass_foundations_semisub_calc_kg_per_m*(water_depth+emerged_height_m)
```

**GBF**

```python
#GBF

if foundations_inventory=="automatised_mass_model":
    # Level 1 : Calculation of the total mass of the foundations based on linear mass model
    mass_foundations_gbf_tot_kg=mass_foundations_gbf_calc_kg
    #We assume material ratios in the foundations are the same as in the reference inventory
    resizing_mass_gbf_foundation=mass_foundations_gbf_tot_kg/MASS_FOUNDATION_GBF_TOT_KG
    mass_foundation_gbf_steel_reinforcing_kg=MASS_FOUNDATION_GBF_STEEL_REINFORCING_KG*resizing_mass_gbf_foundation
    mass_foundation_gbf_concrete_kg=MASS_FOUNDATION_GBF_CONCRETE_KG*resizing_mass_gbf_foundation
    mass_foundation_gbf_gravel_kg=MASS_FOUNDATION_GBF_GRAVEL_KG*resizing_mass_gbf_foundation
    
elif foundations_inventory=="user_mass_model":
    # Level 2 : Calculation of the total mass of the foundations based on the user mass model
    mass_foundations_gbf_tot_kg=0 #kg
    #We assume material ratios in the foundations are the same as in the reference inventory
    resizing_mass_gbf_foundation=mass_foundations_gbf_tot_kg/MASS_FOUNDATION_GBF_TOT_KG
    mass_foundation_gbf_steel_reinforcing_kg=MASS_FOUNDATION_GBF_STEEL_REINFORCING_KG*resizing_mass_gbf_foundation
    mass_foundation_gbf_concrete_kg=MASS_FOUNDATION_GBF_CONCRETE_KG*resizing_mass_gbf_foundation
    mass_foundation_gbf_gravel_kg=MASS_FOUNDATION_GBF_GRAVEL_KG*resizing_mass_gbf_foundation

```

```python
values_table(
    mass_foundations_gbf_tot_kg=(mass_foundations_gbf_tot_kg, "kg"),
    mass_foundation_gbf_steel_reinforcing_kg=(mass_foundation_gbf_steel_reinforcing_kg,"kg"),
    mass_foundation_gbf_concrete_kg=(mass_foundation_gbf_concrete_kg, "kg"),
    mass_foundation_gbf_gravel_kg=(mass_foundation_gbf_gravel_kg, "kg"))
```

**MONOPILE**

```python
#Monopile

if foundations_inventory=="automatised_mass_model":
    # Level 1 : Calculation of the total mass of the foundations based on linear mass model
    mass_foundations_monopile_tot_kg=mass_foundations_monopile_calc_kg
    
    #We assume material ratios in the foundations are the same as in the reference inventory
    resizing_mass_monopile_foundation=mass_foundations_monopile_tot_kg/MASS_FOUNDATION_MONOPILE_TOT_KG
    mass_foundation_monopile_steel_mix_kg =MASS_FOUNDATION_MONOPILE_STEEL_MIX_KG * resizing_mass_monopile_foundation
    mass_foundation_monopile_concrete_kg=MASS_FOUNDATION_MONOPILE_CONCRETE_KG * resizing_mass_monopile_foundation
    
elif foundations_inventory=="user_mass_model":
    # Level 2 : Calculation of the total mass of the foundations based on the user mass model
    mass_foundations_monopile_tot_kg=0 #kg
        
    #We assume material ratios in the foundations are the same as in the reference inventory
    resizing_mass_monopile_foundation=mass_foundations_monopile_tot_kg/MASS_FOUNDATION_MONOPILE_TOT_KG
    mass_foundation_monopile_steel_mix_kg =MASS_FOUNDATION_MONOPILE_STEEL_MIX_KG * resizing_mass_monopile_foundation
    mass_foundation_monopile_concrete_kg=MASS_FOUNDATION_MONOPILE_CONCRETE_KG * resizing_mass_monopile_foundation

```

```python
values_table(
    mass_foundations_monopile_tot_kg=(mass_foundations_monopile_tot_kg, "kg"),
    mass_foundation_monopile_steel_mix_kg =(mass_foundation_monopile_steel_mix_kg ,"kg"),
    mass_foundation_monopile_concrete_kg=(mass_foundation_monopile_concrete_kg, "kg"))
```

**TRIPOD**

```python
#Tripod

if foundations_inventory=="automatised_mass_model":
    # Level 1 : Calculation of the total mass of the foundations based on linear mass model
    mass_foundations_tripod_tot_kg=mass_foundations_tripod_calc_kg
    #We assume material ratios in the foundations are the same as in the reference inventory
    resizing_mass_tripod_foundation=mass_foundations_tripod_tot_kg/MASS_FOUNDATION_TRIPOD_TOT_KG
    mass_foundation_tripod_steel_mix_kg =MASS_FOUNDATION_TRIPOD_STEEL_MIX_KG *resizing_mass_tripod_foundation
    mass_foundation_tripod_concrete_kg=MASS_FOUNDATION_TRIPOD_CONCRETE_KG * resizing_mass_tripod_foundation
    
elif foundations_inventory=="user_mass_model":
    # Level 2 : Calculation of the total mass of the foundations based on the user mass model
    mass_foundations_tripod_tot_kg=0 #kg
    #We assume material ratios in the foundations are the same as in the reference inventory
    resizing_mass_tripod_foundation=mass_foundations_tripod_tot_kg/MASS_FOUNDATION_TRIPOD_TOT_KG
    mass_foundation_tripod_steel_mix_kg =MASS_FOUNDATION_TRIPOD_STEEL_MIX_KG *resizing_mass_tripod_foundation
    mass_foundation_tripod_concrete_kg=MASS_FOUNDATION_TRIPOD_CONCRETE_KG * resizing_mass_tripod_foundation

```

```python
values_table(
    mass_foundations_tripod_tot_kg=(mass_foundations_tripod_tot_kg, "kg"),
    mass_foundation_tripod_steel_mix_kg=(mass_foundation_tripod_steel_mix_kg,"kg"),
    mass_foundation_tripod_concrete_kg=(mass_foundation_tripod_concrete_kg, "kg"))
```

**JACKET**

```python
#jacket

if foundations_inventory=="automatised_mass_model":
    # Level 1 : Calculation of the total mass of the foundations based on own mass model
    mass_foundations_jacket_tot_kg=mass_foundations_jacket_calc_kg
    #We assume it is only steel
    mass_foundation_jacket_steel_mix_kg =mass_foundations_jacket_tot_kg
    
elif foundations_inventory=="user_mass_model":
    # Level 2 : Calculation of the total mass of the foundations based on user mass model
    mass_foundations_jacket_tot_kg=0 #kg
    #We assume it is only steel
    mass_foundation_jacket_steel_mix_kg =mass_foundations_jacket_tot_kg
```

```python
values_table(
    mass_foundations_jacket_tot_kg=(mass_foundations_jacket_tot_kg, "kg"),
    mass_foundation_jacket_steel_mix_kg=(mass_foundation_jacket_steel_mix_kg,"kg"))
```

**FLOATING SPAR**

```python
#Floating spar

if foundations_inventory=="automatised_mass_model":
    # Level 1 : Calculation of the total mass of the foundations based on linear mass model
    mass_foundations_spar_tot_kg=mass_foundations_spar_calc_kg
    #We assume material ratios in the foundations are the same as in the reference inventory
    resizing_mass_spar_foundation=mass_foundations_spar_tot_kg/MASS_FOUNDATION_SPAR_TOT_KG
    mass_foundation_spar_steel_low_alloyed_kg = MASS_FOUNDATION_SPAR_STEEL_LOW_ALLOYED_KG * resizing_mass_spar_foundation
    mass_foundation_spar_steel_high_alloyed_kg = MASS_FOUNDATION_SPAR_STEEL_HIGH_ALLOYED_KG* resizing_mass_spar_foundation
    mass_foundation_spar_gravel_ballast_kg =  MASS_FOUNDATION_SPAR_GRAVEL_BALLAST_KG * resizing_mass_spar_foundation
    mass_foundation_spar_gravel_mooring_kg =  MASS_FOUNDATION_SPAR_GRAVEL_MOORING_KG * resizing_mass_spar_foundation

    
elif foundations_inventory=="user_mass_model":
    # Level 2 : Calculation of the total mass of the foundations based on the user mass model
    mass_foundations_spar_tot_kg=0 #kg
    #We assume material ratios in the foundations are the same as in the reference inventory
    resizing_mass_spar_foundation=mass_foundations_spar_tot_kg/MASS_FOUNDATION_SPAR_TOT_KG
    mass_foundation_spar_steel_low_alloyed_kg = MASS_FOUNDATION_SPAR_STEEL_LOW_ALLOYED_KG * resizing_mass_spar_foundation
    mass_foundation_spar_steel_high_alloyed_kg = MASS_FOUNDATION_SPAR_STEEL_HIGH_ALLOYED_KG* resizing_mass_spar_foundation
    mass_foundation_spar_gravel_ballast_kg =  MASS_FOUNDATION_SPAR_GRAVEL_BALLAST_KG * resizing_mass_spar_foundation
    mass_foundation_spar_gravel_mooring_kg =  MASS_FOUNDATION_SPAR_GRAVEL_MOORING_KG * resizing_mass_spar_foundation

```

```python
values_table(
    mass_foundations_spar_tot_kg=(mass_foundations_spar_tot_kg, "kg"),
    mass_foundation_spar_steel_low_alloyed_kg=(mass_foundation_spar_steel_low_alloyed_kg,"kg"),
    mass_foundation_spar_steel_high_alloyed_kg=(mass_foundation_spar_steel_high_alloyed_kg, "kg"),
    mass_foundation_spar_gravel_ballast_kg=(mass_foundation_spar_gravel_ballast_kg, "kg"),
    mass_foundation_spar_gravel_mooring_kg=(mass_foundation_spar_gravel_mooring_kg, "kg"))
```

**FLOATING SEMI SUBMERSIBLE**

```python
#SEMI SUB

if foundations_inventory=="automatised_mass_model":
    # Level 1 : Calculation of the total mass of the foundations based on own mass model
    mass_foundations_semisub_tot_kg=mass_foundations_semisub_calc_kg
    #We assume it is only steel
    mass_foundation_semisub_steel_mix_kg =mass_foundations_semisub_tot_kg
    
elif foundations_inventory=="user_mass_model":
    # Level 2 : Calculation of the total mass of the foundations based on user mass model
    mmass_foundations_semisub_tot_kg=0 #kg
    #We assume it is only steel
    mass_foundation_semisub_steel_mix_kg =mass_foundations_semisub_tot_kg
```

```python
values_table(
    mass_foundations_semisub_tot_kg=(mass_foundations_semisub_tot_kg, "kg"),
    mass_foundation_semisub_steel_mix_kg=(mass_foundation_semisub_steel_mix_kg,"kg"))
```

**Custom**

```python
#Level 3 and 4 : enter the masses 
mass_foundation_custom_steel_kg=0 #kg
mass_foundation_custom_concrete_kg= 0 #kg
volume_foundation_custom_concrete_m3= mass_foundation_custom_concrete_kg/CONCRETE_DENSITY #m3
mass_foundation_custom_gravel_kg = 0 # kg
#automatic calculation of total mass
mass_foundations_custom_tot_kg =mass_foundation_custom_steel_kg+mass_foundation_custom_concrete_kg+ mass_foundation_custom_gravel_kg
```

```python
values_table(
    mass_foundations_custom_tot_kg=(mass_foundations_custom_tot_kg, "kg"),
    mass_foundation_custom_steel_kg=(mass_foundation_custom_steel_kg,"kg"),
    mass_foundation_custom_concrete_kg=(mass_foundation_custom_concrete_kg, "kg"),
    mass_foundation_custom_gravel_kg=(mass_foundation_custom_gravel_kg, "kg"))
```

### 4️⃣ Resizing the inventory

```python
#level 1 and 2 :
one_foundation_gbf_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of the gbf foundations of one wind turbine",
                       unit = "unit",
                       exchanges = {one_foundation_gbf_manufacturing_ref:resizing_mass_gbf_foundation                           
             })

one_foundation_monopile_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of the monopile foundations of one wind turbine",
                       unit = "unit",
                       exchanges = {one_foundation_monopile_manufacturing_ref:resizing_mass_monopile_foundation                           
             })
    
one_foundation_tripod_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of the tripod foundations of one wind turbine",
                       unit = "unit",
                       exchanges = {one_foundation_tripod_manufacturing_ref:resizing_mass_tripod_foundation                          
             })

one_foundation_jacket_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of the jacket foundations of one wind turbine",
                       unit = "unit",
                       system_1=WT_FOUNDATIONS,
                       phase=PHASE_1_MANUFACTURING,
                       exchanges = {
                           steel_low_alloyed_mix: mass_foundation_jacket_steel_mix_kg,
                           steel_process: mass_foundation_jacket_steel_mix_kg,                           
             })
    
one_foundation_spar_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of the floating spar foundations of one wind turbine",
                       unit = "unit",
                       exchanges = {one_foundation_spar_manufacturing_ref:resizing_mass_spar_foundation                           
             })

one_foundation_semisub_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of the semi submersible foundations of one wind turbine",
                       unit = "unit",
                       system_1=WT_FOUNDATIONS,
                       phase=PHASE_1_MANUFACTURING,
                       exchanges = {
                           steel_low_alloyed_mix: mass_foundation_semisub_steel_mix_kg,
                           steel_process: mass_foundation_semisub_steel_mix_kg,                           
             })
    

#Level 3 and 4:
one_foundation_custom_manufacturing = agb.newActivity(USER_DB,
                                     'manufacturing of one xx technology foundations at yy m water depth for a zz MW wind turbine',
                                      unit = 'unit',
                                      phase = PHASE_1_MANUFACTURING,
                                      system_1 = WT_FOUNDATIONS,
                                     exchanges = {
                                         steel_low_alloyed_mix: mass_foundation_custom_steel_kg,
                                         steel_process: mass_foundation_custom_steel_kg,
                                         concrete: volume_foundation_custom_concrete_m3,
                                         gravel: mass_foundation_custom_gravel_kg, 
                                         #add flows of needed
                                     })

#Print the customized inventory
agb.printAct(one_foundation_custom_manufacturing)
    
```

### Choice of fundation type

```python
#We introduce an activity for the manufacturing of foundations according to the type of foundations selected
one_foundation_manufacturing = agb.newSwitchAct(USER_DB,
                             "manufacturing of one wind turbine foundation",                                      
                            foundations_type,
                            {
                                 "gbf": one_foundation_gbf_manufacturing,
                                 "monopod": one_foundation_monopile_manufacturing ,
                                 "tripod": one_foundation_tripod_manufacturing,
                                 "jacket":one_foundation_jacket_manufacturing,
                                 "floatingspar":one_foundation_spar_manufacturing,
                                 "semisub": one_foundation_semisub_manufacturing,
                                 "custom":one_foundation_custom_manufacturing
                            })
```

### Foundations at wind farm level

```python
foundations_manufacturing = agb.newActivity(
                                      USER_DB,
                                      "manufacturing of the foundations of wind turbines",     
                                      unit = 'unit',
                                     exchanges = {
                                         one_foundation_manufacturing:n_turbines,    
                                     })
```

### LCA RESULT: climate change impacts of wind turbines' foundations manufacturing

```python
#Climate change impact of the whole infrastructure
agb.multiLCAAlgebric(
    [foundations_manufacturing],
    impacts_EF_CO2)
```

```python
#Climate change impact per MW installed
#We use the function compute_impacts to resize the inventory (division per power_tot_farm_MW)

compute_impacts(
    foundations_manufacturing,
    impacts_EF_CO2,
    functional_unit=power_tot_farm_MW)
```

```python
#Climate change impact per kWh of electricity produced
#We use the function compute_impacts to resize the inventory (division per elec_prod_lifetime_kWh)

compute_impacts(
    foundations_manufacturing,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh                )
```

## Export cables


Reference inventory : linear inventory of 225 kV AC cables for 300 MW of installed power capacity, data taken directly on the SimaPro inventories provided by RTE (not in the report).

```python
# In RTE reference study, the capacity of the wind farm is 600 MW but there are two cables, each one for 300 MW capacity, 
# so the reference inventories are the ones of one cable for 300 MW wind farm capacity
EXPORT_CABLES_REF_POWER_MW=300 #MW   (source: RTE report)
EXPORT_CABLES_ALU_REF_LENGTH_M=29000 #m
EXPORT_CABLES_COP_REF_LENGTH_M=1000#m
EXPORT_CABLES_REF_LENGTH_M=EXPORT_CABLES_ALU_REF_LENGTH_M+EXPORT_CABLES_COP_REF_LENGTH_M
```

### Aluminum export cables 



#### Reference inventory

```python
# The reference data are linear
# Reference data for the aluminum export cable that is provided in RTE study for a 300 MW wind farm capacity 
LINEAR_MASS_ALU_EXPCABLES_ALU=12.96 #kg/m
LINEAR_MASS_STEEL_EXPCABLES_ALU=26 #kg/m
LINEAR_MASS_LEAD_EXPCABLES_ALU=27.72 #kg/m
LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_ALU=2.4+2.1+15.3+7.26E-3 #kg/m
LINEAR_MASS_POLYPROPYLENE_EXPCABLES_ALU=2+2.2+4.8 #kg/m
LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_ALU=17.56E-6 #kg/m
LINEAR_MASS_EXPCABLES_ALU_TOT=LINEAR_MASS_ALU_EXPCABLES_ALU+LINEAR_MASS_STEEL_EXPCABLES_ALU+LINEAR_MASS_LEAD_EXPCABLES_ALU+LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_ALU+LINEAR_MASS_POLYPROPYLENE_EXPCABLES_ALU+LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_ALU  #kg/m

MASS_EXPCABLES_ALU_TOT_KG=EXPORT_CABLES_ALU_REF_LENGTH_M*LINEAR_MASS_EXPCABLES_ALU_TOT
```

```python
values_table(
   LINEAR_MASS_EXPCABLES_ALU_TOT=(LINEAR_MASS_EXPCABLES_ALU_TOT,"kg/m"),
   LINEAR_MASS_ALU_EXPCABLES_ALU=(LINEAR_MASS_ALU_EXPCABLES_ALU, "kg/m"),
   LINEAR_MASS_STEEL_EXPCABLES_ALU=(LINEAR_MASS_STEEL_EXPCABLES_ALU, "kg/m"),
   LINEAR_MASS_LEAD_EXPCABLES_ALU=(LINEAR_MASS_LEAD_EXPCABLES_ALU, "kg/m"),
   LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_ALU=(LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_ALU, "kg/m"),
   LINEAR_MASS_POLYPROPYLENE_EXPCABLES_ALU=(LINEAR_MASS_POLYPROPYLENE_EXPCABLES_ALU, "kg/m"),
   LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_ALU=(LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_ALU, "kg/m"),
   )
```

```python
# We define a linear inventory for the aluminum export cable based on data provided in RTE study for a 300 MW wind farm capacity 

expcables_alu_linear_manufacturing_ref = agb.newActivity(USER_DB,
                       "manufacturing of one 225kV export aluminium cable per linear meter of cable for a 300 MW wind farm",
                       unit = "unit/m",
                       phase = PHASE_1_MANUFACTURING,
                       system_2 = ALU_EXP_CABLES,
                       exchanges = {
                           aluminium_mix: LINEAR_MASS_ALU_EXPCABLES_ALU, 
                           alu_process:LINEAR_MASS_ALU_EXPCABLES_ALU,
                           
                           steel_low_alloyed_mix: LINEAR_MASS_STEEL_EXPCABLES_ALU,
                           steel_process_2 : LINEAR_MASS_STEEL_EXPCABLES_ALU,
                           
                           lead: LINEAR_MASS_LEAD_EXPCABLES_ALU,
                           lead_process: LINEAR_MASS_LEAD_EXPCABLES_ALU,
                          
                           polyethylene_HD : LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_ALU,
                           plastic_process :LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_ALU,
                           
                           polypropylene : LINEAR_MASS_POLYPROPYLENE_EXPCABLES_ALU,
                           plastic_process : LINEAR_MASS_POLYPROPYLENE_EXPCABLES_ALU,
                           
                           glass_fibre: LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_ALU, 
                           
                       })


#Print the reference inventory
agb.printAct(expcables_alu_linear_manufacturing_ref)
```

#### 2️⃣ Resizing the mass

```python
# Calculation of the total mass of all the export cables based on nominal power and cable length
# We do a linear extrapolation based on total installed power 
# We do a linear extrapolation based on cable length
# * length_1_expcable_alu*(power_tot_farm_MW/EXPORT_CABLES_REF_POWER_MW)

mass_expcables_alu_tot_kg=LINEAR_MASS_EXPCABLES_ALU_TOT* (length_1_expcable_alu) * (power_tot_farm_MW/EXPORT_CABLES_REF_POWER_MW) #kg

```

```python
#We assume material ratios in the cables are the same as in the reference inventory of the cables

resizing_mass_expcables_alu=mass_expcables_alu_tot_kg/LINEAR_MASS_EXPCABLES_ALU_TOT
mass_alu_expcables_alu=LINEAR_MASS_ALU_EXPCABLES_ALU*resizing_mass_expcables_alu #kg
mass_steel_expcables_alu=LINEAR_MASS_STEEL_EXPCABLES_ALU*resizing_mass_expcables_alu #kg
mass_lead_expcables_alu=LINEAR_MASS_LEAD_EXPCABLES_ALU*resizing_mass_expcables_alu #kg
mass_polyethylene_HD_expcables_alu=LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_ALU*resizing_mass_expcables_alu #kg
mass_polypropylene_HD_expcables_alu=LINEAR_MASS_POLYPROPYLENE_EXPCABLES_ALU*resizing_mass_expcables_alu #kg
mass_glass_fibre_HD_expcables_alu=LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_ALU*resizing_mass_expcables_alu #kg
```

#### Resizing the inventory

```python
#Resizing the inventory : linear extrapolation based on the total mass of the cables

expcables_alu_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of export aluminium cables of the wind farm",
                       unit = "unit",
                       exchanges = {
                           expcables_alu_linear_manufacturing_ref:resizing_mass_expcables_alu
                       })
```

### Copper export cables 


#### Reference inventory

```python
# The reference data are linear
# Reference data for the copper export cable that is provided in RTE study for a 300 MW wind farm capacity 
LINEAR_MASS_COP_EXPCABLES_COP= 33.75 #kg/m
LINEAR_MASS_STEEL_EXPCABLES_COP= 33 #kg/m
LINEAR_MASS_LEAD_EXPCABLES_COP= 26.280 #kg/m
LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_COP= 2.4+2.1+14.1+7.26E-3 #kg/m
LINEAR_MASS_POLYPROPYLENE_EXPCABLES_COP= 2+1.7+4.6 #kg/m
LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_COP=17.56E-6 #kg/m
LINEAR_MASS_EXPCABLES_COP_TOT= LINEAR_MASS_COP_EXPCABLES_COP+LINEAR_MASS_STEEL_EXPCABLES_COP+LINEAR_MASS_LEAD_EXPCABLES_COP+LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_COP+LINEAR_MASS_POLYPROPYLENE_EXPCABLES_COP+LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_COP #kg/m

MASS_EXPCABLES_COP_TOT_KG=EXPORT_CABLES_COP_REF_LENGTH_M*LINEAR_MASS_EXPCABLES_COP_TOT
```

```python
values_table(
   LINEAR_MASS_EXPCABLES_COP_TOT=(LINEAR_MASS_EXPCABLES_COP_TOT,"kg/m"),
   LINEAR_MASS_COP_EXPCABLES_COP=(LINEAR_MASS_COP_EXPCABLES_COP, "kg/m"),
   LINEAR_MASS_LEAD_EXPCABLES_COP=(LINEAR_MASS_LEAD_EXPCABLES_COP, "kg"),
   LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_COP=(LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_COP, "kg/m"),
   LINEAR_MASS_POLYPROPYLENE_EXPCABLES_COP=(LINEAR_MASS_POLYPROPYLENE_EXPCABLES_COP, "kg/m"),
   LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_COP=(LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_COP, "kg/m"),
   )
```

```python
# We define a linear inventory for the copper export cable based on data provided in RTE study for a 300 MW wind farm capacity 

expcables_cop_linear_manufacturing_ref = agb.newActivity(USER_DB,
                       "manufacturing of one 225kV export copper cable per linear meter of cable for 300 MW wind farm",
                       unit = "unit/m",
                       phase = PHASE_1_MANUFACTURING,
                       system_2 = COP_EXP_CABLES,
                       exchanges = {
                           copper: LINEAR_MASS_COP_EXPCABLES_COP, 
                           copper_process:LINEAR_MASS_COP_EXPCABLES_COP,
                           
                           steel_low_alloyed_mix: LINEAR_MASS_STEEL_EXPCABLES_COP,
                           steel_process_2 : LINEAR_MASS_STEEL_EXPCABLES_COP,
                           
                           lead: LINEAR_MASS_LEAD_EXPCABLES_COP,
                           lead_process: LINEAR_MASS_LEAD_EXPCABLES_COP,
                          
                           polyethylene_HD : LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_COP,
                           plastic_process :LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_COP,
                           
                           polypropylene :LINEAR_MASS_POLYPROPYLENE_EXPCABLES_COP,
                           plastic_process : LINEAR_MASS_POLYPROPYLENE_EXPCABLES_COP,
                           
                           glass_fibre: LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_COP, 
                           
                       })

#Print the reference inventory
agb.printAct(expcables_cop_linear_manufacturing_ref)
```

#### 2️⃣ Resizing the mass

```python
# Calculation of the total mass of all the export cables based on nominal power and cable length
# We do a linear extrapolation based on total installed power 
# We do a linear extrapolation based on cable length
# * length_1_expcable_alu*(power_tot_farm_MW/EXPORT_CABLES_REF_POWER_MW)

mass_expcables_cop_tot_kg=LINEAR_MASS_EXPCABLES_COP_TOT*length_1_expcable_cop*power_tot_farm_MW/EXPORT_CABLES_REF_POWER_MW #kg
```

```python
#We assume material ratios in the cable are the same as in the reference inventory of the cable

resizing_mass_expcables_cop=mass_expcables_cop_tot_kg/LINEAR_MASS_EXPCABLES_COP_TOT

mass_cop_expcables_cop=LINEAR_MASS_COP_EXPCABLES_COP*resizing_mass_expcables_cop #kg
mass_steel_expcables_cop=LINEAR_MASS_STEEL_EXPCABLES_COP*resizing_mass_expcables_cop #kg
mass_lead_expcables_cop=LINEAR_MASS_LEAD_EXPCABLES_COP*resizing_mass_expcables_cop #kg
mass_polyethylene_HD_expcables_cop=LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_COP*resizing_mass_expcables_cop #kg
mass_polypropylene_HD_expcables_cop=LINEAR_MASS_POLYPROPYLENE_EXPCABLES_COP*resizing_mass_expcables_cop #kg
mass_glass_fibre_HD_expcables_cop=LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_COP*resizing_mass_expcables_cop #kg

```

#### Resizing the inventory

```python
#Resizing the inventory : linear extrapolation based on the total mass of the cables

expcables_cop_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of export copper cables of the wind farm",
                       unit = "unit",
                       exchanges = {
                           expcables_cop_linear_manufacturing_ref:resizing_mass_expcables_cop

                       })
```

### Export cables assembly

```python
# We introduce an activity for the export cables that are composed of aluminium and copper cables
expcables_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of export cables",
                       unit = "unit",
                       system_1 = EXP_CABLES,
                       exchanges = {
                           expcables_alu_manufacturing :1,
                           expcables_cop_manufacturing :1,
                          })
```

```python
MASS_EXPCABLES_TOT_KG=MASS_EXPCABLES_ALU_TOT_KG+MASS_EXPCABLES_COP_TOT_KG
mass_expcables_tot_kg=mass_expcables_alu_tot_kg+mass_expcables_cop_tot_kg

values_table(
   MASS_EXPCABLES_TOT_KG=(MASS_EXPCABLES_TOT_KG,"kg"),
   mass_expcables_tot_kg=(mass_expcables_tot_kg, "kg"),
   )
```

###  4️⃣ Customised inventory
If you have the value of masses of each material, you can write expcable_inventory="bills_of_materials" and generate a new inventory. <br>

```python
#Turn expcable_inventory name if you want to customise the inventory
expcable_inventory="mass_model"
#expcable_inventory="bills_of_materials"

#If you have the linear masses of each material, enter the value of the masses
linear_mass_alu_expcables_custom= 0 #kg/m
linear_mass_steel_expcables_custom = 0 #kg/m
linear_mass_lead_expcables_custom = 0 #kg/m
linear_mass_polyethylene_hd_expcables_custom = 0 #kg/m
linear_mass_polypropylene_expcables_custom = 0 #kg/m
linear_mass_glass_fibre_hd_expcables_custom =0 #kg/m
linear_mass_tot_expcables_custom = linear_mass_alu_expcables_custom +linear_mass_steel_expcables_custom +linear_mass_lead_expcables_custom +linear_mass_polyethylene_hd_expcables_custom +linear_mass_polypropylene_expcables_custom +linear_mass_glass_fibre_hd_expcables_custom #kg/m

expcables_custom_linear_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of one 225kV export custom cable per linear meter of cable for a 300 MW wind farm",
                       unit = "unit/m",
                       phase = PHASE_1_MANUFACTURING,
                       system_1=EXP_CABLES,
                       exchanges = {
                           aluminium_mix: linear_mass_alu_expcables_custom, 
                           alu_process:linear_mass_alu_expcables_custom,
                           
                           steel_low_alloyed_mix: linear_mass_steel_expcables_custom,
                           steel_process_2 :linear_mass_steel_expcables_custom,
                           
                           lead: linear_mass_lead_expcables_custom,
                           lead_process: linear_mass_lead_expcables_custom,
                          
                           polyethylene_HD : linear_mass_polyethylene_hd_expcables_custom,
                           plastic_process : linear_mass_polyethylene_hd_expcables_custom,
                           
                           polypropylene : linear_mass_polypropylene_expcables_custom,
                           plastic_process : linear_mass_polypropylene_expcables_custom,
                           
                           glass_fibre: linear_mass_tot_expcables_custom, 
                           
                       })



if expcable_inventory=="bills_of_materials":
    # If it is an aluminium cable, use the length and the names of masses for the aluminium cable (to automatise the tranport and en of life stages)
    # If it is a copper cable, change for copper names for masses
    
    #enter numbers of cables
    number_of_cables_custom=0
    
    #automatic calculation
    tot_length_expcables_custom=length_1_expcable_alu*number_of_cables_custom
    mass_tot_expcables_alu=linear_mass_tot_expcables_custom* tot_length_expcables_custom
    mass_alu_expcables_alu=linear_mass_alu_expcables_custom* tot_length_expcables_custom #kg
    mass_steel_expcables_alu=linear_mass_steel_expcables_custom* tot_length_expcables_custom #kg
    mass_lead_expcables_alu=linear_mass_lead_expcables_custom* tot_length_expcables_custom #kg
    mass_polyethylene_HD_expcables_alu=linear_mass_polyethylene_hd_expcables_custom* tot_length_expcables_custom #kg
    mass_polypropylene_HD_expcables_alu= linear_mass_polypropylene_expcables_custom* tot_length_expcables_custom #kg
    mass_glass_fibre_HD_expcables_alu=linear_mass_tot_expcables_custom* tot_length_expcables_custom #kg

   #The customised inventory is put into the aluminim cable activity, the copper cable inventory is considered as empty.
    #masses are = 0 as they are used for transort and at end of life stage
    mass_tot_expcables_cop=0
    mass_alu_expcables_cop=0
    mass_steel_expcables_cop=0
    mass_lead_expcables_cop=0
    mass_polyethylene_HD_expcables_cop=0
    mass_polypropylene_HD_expcables_cop=0
    mass_glass_fibre_HD_expcables_cop=0
    
    mass_tot_expcables=mass_tot_expcables_alu+mass_tot_expcables_cop
    
    expcables_manufacturing= agb.newActivity(USER_DB,
                       "manufacturing of customised export cables",
                       unit = "unit/m",
                       phase = PHASE_1_MANUFACTURING,
                       exchanges = {
                           expcables_custom_linear_manufacturing:tot_length_expcables_custom 
                       })
    
    #Print the custom inventory
    agb.printAct(expcables_manufacturing)
    
    #Print the masses
    values_table(
       mass_tot_expcables=(mass_tot_expcables, "kg"),
       )
```

### LCA Result : climate change

```python
#Climate change impact of the whole infrastructure
compute_impacts(
    expcables_manufacturing,
    impacts_EF_CO2,
    axis="system_2")
```

```python
#Climate change impact per MW installed
#We use the function compute_impacts to resize the inventory (division per power_tot_farm_MW)
compute_impacts(
    expcables_manufacturing,
    impacts_EF_CO2,
    functional_unit=power_tot_farm_MW,
    axis="system_2")
```

```python
#Climate change impact per kWh of electricity produced
#We use the function compute_impacts to resize the inventory (division per elec_prod_lifetime_kWh)
compute_impacts(
    expcables_manufacturing,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh,
    axis="system_2")
```

## Wind farm inter-array cables


Reference inventory : resized inventory of one alumimium export cable based on geometric data provided by RTE study and prysmian
* Prysmian Group study "66 kV Submarine Cable Systems FOR OFFSHORE WIND" (66 kV cables, 800 mm2 conductor section, copper cables, wet design)


### 4️⃣ Reference inventory
Level 4 : change the total linear mass or the total linear mass. 

```python
#From Prysmian Group study: 66 kV cables, 800 mm2 conductor section, aluminium cables, semi-wet design)
LINEAR_MASS_EXPCABLES_ALU_TOT
LINEAR_MASS_INTCABLES_ALU_TOT=39.4 #kg/m
resizing_mass_exp_to_intcable=LINEAR_MASS_INTCABLES_ALU_TOT/LINEAR_MASS_EXPCABLES_ALU_TOT
print(resizing_mass_exp_to_intcable)
```

```python
intcables_alu_linear_manufacturing_ref = agb.newActivity(USER_DB,
                       "manufacturing of 66 kV interray aluminium cables per linear meter",
                       unit = "unit/m",
                       system_1 = INT_CABLES,
                       exchanges = {
                           expcables_alu_linear_manufacturing_ref :resizing_mass_exp_to_intcable
                       })
```

```python
# Reference linear masses resizing
LINEAR_MASS_ALU_INTCABLES_ALU= resizing_mass_exp_to_intcable* LINEAR_MASS_ALU_EXPCABLES_ALU #kg/m
LINEAR_MASS_STEEL_INTCABLES_ALU= resizing_mass_exp_to_intcable*LINEAR_MASS_STEEL_EXPCABLES_ALU #kg/m
LINEAR_MASS_LEAD_INTCABLES_ALU=resizing_mass_exp_to_intcable* LINEAR_MASS_LEAD_EXPCABLES_ALU #kg/m
LINEAR_MASS_POLYETHYLENE_HD_INTCABLES_ALU= resizing_mass_exp_to_intcable* LINEAR_MASS_POLYETHYLENE_HD_EXPCABLES_ALU #kg/m
LINEAR_MASS_POLYPROPYLENE_INTCABLES_ALU= resizing_mass_exp_to_intcable* LINEAR_MASS_POLYPROPYLENE_EXPCABLES_ALU #kg/m
LINEAR_MASS_GLASS_FIBRE_HD_INTCABLES_ALU= resizing_mass_exp_to_intcable*LINEAR_MASS_GLASS_FIBRE_HD_EXPCABLES_ALU #kg/m

```

```python
values_table(
   LINEAR_MASS_INTCABLES_ALU_TOT=(LINEAR_MASS_INTCABLES_ALU_TOT,"kg"),
   LINEAR_MASS_ALU_INTCABLES_ALU=(LINEAR_MASS_ALU_INTCABLES_ALU, "kg"),
   LINEAR_MASS_LEAD_INTCABLES_ALU=(LINEAR_MASS_LEAD_INTCABLES_ALU, "kg"),
   LINEAR_MASS_POLYETHYLENE_HD_INTCABLES_ALU=(LINEAR_MASS_POLYETHYLENE_HD_INTCABLES_ALU, "kg"),
   LINEAR_MASS_POLYPROPYLENE_INTCABLES_ALU=(LINEAR_MASS_POLYPROPYLENE_INTCABLES_ALU, "kg"),
   LINEAR_MASS_GLASS_FIBRE_HD_INTCABLES_ALU=(LINEAR_MASS_GLASS_FIBRE_HD_INTCABLES_ALU, "kg"),
   )
```

###  2️⃣ 3️⃣ Length of cables

```python
#level 2 : change the rotor diameter
rotor_diameter_m = rotor_diameter_calc_m

#Level 3: change the length
length_1_intcable_m=fixed_foundations*(2*water_depth+8.5*rotor_diameter_m)+(1-fixed_foundations)*(4*water_depth+8.5*rotor_diameter_m)
n_intcables=n_turbines 

length_tot_intcables_m=n_turbines*length_1_intcable_m #m

values_table(
   length_1_intcable_m=(length_1_intcable_m,"m"),
   length_tot_intcables_m=(length_tot_intcables_m, "m")
   )
```

### Resizing the mass

```python
# Automatic calculation of the total mass of the interarray cables based on cable length
# We do a linear extrapolation based on cable length
mass_intcables_alu_tot_kg=LINEAR_MASS_INTCABLES_ALU_TOT*length_tot_intcables_m #kg

resizing_mass_intcables_alu=mass_intcables_alu_tot_kg/LINEAR_MASS_INTCABLES_ALU_TOT

```

### Resizing the inventory

```python
#Resizing the inventory : linear extrapolation based on the total mass of the cables

intcables_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of interarray aluminium cables of the wind farm",
                       unit = "unit",
                       exchanges = {
                           intcables_alu_linear_manufacturing_ref:resizing_mass_intcables_alu
                       })
```

```python
#We assume material ratios in the nacelle are the same as in the reference inventory of the nacelle
mass_alu_intcables_alu=LINEAR_MASS_ALU_INTCABLES_ALU*resizing_mass_intcables_alu #kg
mass_steel_intcables_alu=LINEAR_MASS_STEEL_INTCABLES_ALU*resizing_mass_intcables_alu #kg
mass_lead_intcables_alu=LINEAR_MASS_LEAD_INTCABLES_ALU*resizing_mass_intcables_alu #kg
mass_polyethylene_HD_intcables_alu=LINEAR_MASS_POLYETHYLENE_HD_INTCABLES_ALU*resizing_mass_intcables_alu #kg
mass_polypropylene_HD_intcables_alu=LINEAR_MASS_POLYPROPYLENE_INTCABLES_ALU*resizing_mass_intcables_alu #kg
mass_glass_fibre_HD_intcables_alu=LINEAR_MASS_GLASS_FIBRE_HD_INTCABLES_ALU*resizing_mass_intcables_alu #kg

```

### LCA Result : climate change

```python
#Climate change impact of the whole infrastructure
compute_impacts(
    intcables_manufacturing,
    impacts_EF_CO2)
```

```python
#Climate change impact per MW installed
#We use the function compute_impacts to resize the inventory (division per power_tot_farm_MW)
compute_impacts(
    intcables_manufacturing,
    impacts_EF_CO2,
    functional_unit=power_tot_farm_MW)
```

```python
#Climate change impact per kWh of electricity produced
#We use the function compute_impacts to resize the inventory (division per elec_prod_lifetime_kWh)
compute_impacts(
    intcables_manufacturing,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh)
```

## Offshore substation


The data for the offshore substation were extracted from a study called "Analyse du cycle de vie du poste en mer", conducted by Elys COnseil, EcoAct and RTE (July 2020). The study modelised an offshore substation for a 600 MW windfarm. The offshore substation is divided is 7 systems :  
* Offshore substation structure 
* Electric component 
* Manipulate equipment 
* Control instrumentation 
* Security scrap equipment 
* Comand control 
* HVAC cooling 


```python
OFFSHORE_SUB_REF_POWER_MW=600 #MW
```

### Offshore substation substructure 


#### Reference inventory


##### Subsystems

```python
#The data for the sacrificial anode is given for a 15 000 kg anode. 
#SACRIFICIAL_ANODE_REF_MASS_KG=15000 #kg

#We introduce a new activity the sacrificial anode 
sacrificial_anode = agb.newActivity(USER_DB,
                            'manufacturing of sacrificial anode for offshore substation',
                            unit = 'unit',
                            phase = PHASE_1_MANUFACTURING,
                            exchanges = {
                                aluminium_mix: 14099,
                                zinc: 862.5,
                                indium: 3,
                                cast_iron: 9,
                                silicon: 18,
                                copper: 0.45,
                                cadmium: 0.3,                      
                            })

#Mass of sacrificial anode 
MASS_ANODE_STRUCTURE_OFFSHORE_SUB_KG_REF=sacrificial_anode.getAmount(['alu*','zinc*','indium*','cast_iron','silicon*','copper*', 'cadmium'],sum=True)
```

```python
#We introduce a new activity for the offshore substation foundations
offshore_sub_structure = agb.newActivity(USER_DB,
                                    "manufacturing of offshore substation foundations",
                                    unit = 'unit',
                                    phase = PHASE_1_MANUFACTURING,
                                    exchanges = {
                                        steel_low_alloyed_mix : (700000 + 875000 + 747000),
                                        gravel : (130000 + 3000000),
                                        zinc_coat: (22000*0.85*100/ZINC_COATING)
                                    })

#Mass of steel in the substation structure
MASS_STEEL_STRUCTURE_OFFSHORE_SUB_KG_REF=offshore_sub_structure.getAmount(['steel*'],sum=True)
```

##### Assembly

```python
#We introduce a new activity for the offshore substation substructure
offshore_sub_structure_manufacturing_ref = agb.newActivity(USER_DB,
                                    "manufacturing of the structure of the reference offshore substation",
                                    unit = 'unit',
                                    system_2 = OFFSHORE_SUB_STRUCTURE,
                                    exchanges = {
                                        offshore_sub_structure:1,
                                        sacrificial_anode:1
                                    })
```

####  2️⃣  4️⃣ Resizing masses

```python
OFFSHORE_SUB_REF_WATER_DEPTH_M=15 #m
station_emerged_height_m=20 #m
MASS_STRUCTURE_OFFSHORE_SUB_KG_REF=MASS_ANODE_STRUCTURE_OFFSHORE_SUB_KG_REF+MASS_STEEL_STRUCTURE_OFFSHORE_SUB_KG_REF

#Level 2 : Formula to calculate the mass of steel on the structure of offshore foundation
mass_steel_struture_offshore_sub_kg=MASS_STEEL_STRUCTURE_OFFSHORE_SUB_KG_REF*(water_depth+station_emerged_height_m)/(OFFSHORE_SUB_REF_WATER_DEPTH_M+emerged_height_m)*(power_tot_farm_MW/OFFSHORE_SUB_REF_POWER_MW)
#Automatic formula
resizing_mass_offshore_sub_struture=mass_steel_struture_offshore_sub_kg/MASS_STEEL_STRUCTURE_OFFSHORE_SUB_KG_REF
mass_anode_struture_offshore_sub_kg=resizing_mass_offshore_sub_struture*MASS_ANODE_STRUCTURE_OFFSHORE_SUB_KG_REF
mass_structure_offshore_sub_kg=mass_steel_struture_offshore_sub_kg+mass_anode_struture_offshore_sub_kg
```

####  4️⃣ Resizing inventory

```python
offshore_sub_structure_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of the structure of the offshore substation",
                       unit = "unit",
                       exchanges = {offshore_sub_structure_manufacturing_ref:resizing_mass_offshore_sub_struture                         
             })
```

### Offshore substation equipments


#### Reference inventory


##### Electric components


###### Subsystems

```python
TSA_1MVA_kg = agb.newActivity(USER_DB,
                      'TSA, 1MVA 66/0.4kv',
                      unit= 'kg',
                      phase = PHASE_1_MANUFACTURING,
                      exchanges = {
                          steel_low_alloyed_mix : (2600+2200)/10250,
                          copper: 1450/10250,
                          paper_printed : 1000*0.5/10250,
                          wood_board :  1000*0.5/DENSITY_PINEWOOD/10250,
                          lubricating_oil: 2000/10250,
                          epoxy: 100/10250,
                      }) 

```

```python
cooling_radiators_kg = agb.newActivity(USER_DB, 
                          'cooling radiators, elevating transformer',
                          unit = 'kg',
                          phase = PHASE_1_MANUFACTURING,
                          exchanges = {
                              steel_unalloyed: 50000/60000,
                              lubricating_oil: 10000/60000,
                          })

```

```python
batteries_kg = agb.newActivity(USER_DB,
                       'Batteries 15, 20 and 50kw, 8h, 48, 127 and 400 VDC',
                       unit = 'kg',
                       phase = PHASE_1_MANUFACTURING,
                       exchanges = {
                           lead: (5797+5478)/16600,
                           water: 2482/16600, 
                           polypropylene: 1328/16600,
                           sulfuric_acid: 1222/16600, 
                           phosphoric_acid: 115/16600,
                           tin: 90/16600, 
                           antimony: 90/16600, 
                       })


```

```python
transformers_330MVA_kg = agb.newActivity(USER_DB, 
                                 'transformers 330MVA-225-66kv',
                                 unit= 'kg',
                                 phase = PHASE_1_MANUFACTURING,
                                 exchanges = {
                                     steel_low_alloyed_mix: 130000/275000,
                                     copper: 30000/275000, 
                                     paper_printed: 15000*0.5/275000,
                                     wood_board:15000*0.5/275000,
                                     lubricating_oil: 100000/275000,
                                     electricity_UCTE: 154110/275000,
                                     district_heating: 655944*3.6/275000,   
                                 })

```

```python
psem_cells_225kv_kg = agb.newActivity(USER_DB,
                        'PSEM cells 225kv',
                        unit = 'kg',
                        phase = PHASE_1_MANUFACTURING,
                        exchanges = {
                            aluminium_mix:3440/5580,
                            steel_low_alloyed_mix: 1380/5580,
                            chromium_steel: 240/5580,
                            epoxy: 150/5580,
                            sf_6: 150/5580,
                            copper: 90/5580,
                            polyethylene_HD: 80/5580,
                        })


```

```python
psem_cells_66kv_kg = agb.newActivity(USER_DB,
                             'PSEM cells 66kv',
                             unit = 'kg',
                             phase = PHASE_1_MANUFACTURING,
                             exchanges = {
                                 aluminium_mix: 1893/3062,
                                 steel_low_alloyed_mix: 645/3062,
                                 pet : (230+2)/3062,
                                 sf_6: 101/3062,
                                 epoxy: 89/3062,
                                 copper:70/3062,
                                 synthetic_rubber: 10/3062,
                                 tetrafluoroethylene:8/3062,
                                 paper_printed: 6/3062,
                                 nylon_6: 3/3062,
                                 zeolite: 2/3062,
                                 pmma: 1/3062,
                             })
```

##### Assembly

```python
offshore_sub_electric_components_manufacturing_ref = agb.newActivity(USER_DB, 
                                 'manufacturing of electric components of the reference offhore substation',
                                 system_2 = OFFSHORE_SUB_EQUIPMENT,
                                 unit = 'unit', 
                                 exchanges = {
                                     TSA_1MVA_kg: 41000,
                                     batteries_kg: 33000,
                                     cooling_radiators_kg: 120000,
                                     psem_cells_225kv_kg:11000,
                                     psem_cells_66kv_kg:61000,
                                     transformers_330MVA_kg: 550000,
                                 })

mass_offshore_sub_electric_components_ref=offshore_sub_electric_components_manufacturing_ref.getAmount(['*'],sum=True)
```

##### Manipulation equipment

```python
offshore_sub_manipulation_equipment_manufacturing_ref = agb.newActivity(USER_DB,
                              'manufacturing of manipulation equipment of the reference offhore substation',
                              unit = 'unit',
                              phase = PHASE_1_MANUFACTURING,
                              system_2 = OFFSHORE_SUB_EQUIPMENT,
                              exchanges = {
                                  steel_low_alloyed_mix: (70000+6000+6000+8000+3000),
                              })

mass_offshore_sub_manipulation_equipment_ref=offshore_sub_manipulation_equipment_manufacturing_ref.getAmount(['*'],sum=True)
```

##### Control instrumentation equiment


###### Subsystems 

```python
#We introduce a new activity : diesel generator
diesel_generator_100kVA = agb.newActivity(USER_DB,
                              'diesel generator 100kVA',
                                   unit = "unit",
                                   phase = PHASE_1_MANUFACTURING,
                                   exchanges = {
                                       alkyd: 25/5791,
                                       aluminium_mix: 150/5791,
                                       brass: 0.5/5791,
                                       brazing:60/5791,
                                       copper: 250/5791,
                                       linerboard: 1.16/5791,
                                       polyethylene_HD: 14/5791,
                                       steel_low_alloyed_mix: (250+4850)/5791,
                                       stone_wool: 190/5791,
                                   })
```

###### Assembly

```python
# We introduce an activity for control-instrumentation of offshore windturbine
offshore_sub_control_instrumentation_manufacturing_ref = agb.newActivity(USER_DB,
                                     'manufacturing of control instrumentation of the reference offshore substation',
                                     unit = "unit",
                                     phase = PHASE_1_MANUFACTURING,
                                     system_2 = OFFSHORE_SUB_EQUIPMENT,
                                     exchanges = {
                                          
                                          diesel_generator_100kVA: 6000,
                                          water: 8000+60000,
                                          co_2: 100,                                         
                                      })

mass_offshore_sub_control_instrumentation_ref=offshore_sub_control_instrumentation_manufacturing_ref.getAmount(['*'],sum=True)
```

##### Security scrap equipment


###### Subsystems

```python
tank_sump_kg = agb.newActivity(USER_DB,
                       'sump tank drum and pump',
                       unit = 'kg',
                       phase = PHASE_1_MANUFACTURING,
                       exchanges = {
                           alkyd: 47/3830,
                           brass: 11/3830,
                           cast_iron: 47/3830,
                           concrete_found: (2/3830)/CONCRETE_DENSITY_2,
                           copper: 158/3830,
                           polyethylene_HD: 4/3830,
                           steel_low_alloyed_mix: 3560/3830,
                       })

diesel_tank_kg = agb.copyActivity(USER_DB,
    tank_sump_kg, 
    "diesel tank 3000L")
```

##### Assembly

```python
offshore_sub_security_scrap_equipment_manufacturing_ref = agb.newActivity(USER_DB,
                                      'manufacturing of equipment security scrap equipment of the reference offshore substation',
                                      unit = 'unit',
                                      system_2 = OFFSHORE_SUB_EQUIPMENT,
                                      exchanges = {
                                          tank_sump_kg:8000,
                                          diesel_tank_kg:12000,
                                      })

mass_offshore_sub_security_scrap_equipment_ref=offshore_sub_security_scrap_equipment_manufacturing_ref.getAmount(['*'],sum=True)
```

##### Command control


###### Subsystems

```python
dc_board_kg = agb.newActivity(USER_DB,
                      'Direct Current DC boards',
                      unit = 'kg',
                      phase = PHASE_1_MANUFACTURING,
                      exchanges = {
                          steel_low_alloyed_mix:180/300,
                          electric_comp:120/300,                         
                      })

telecom_board_kg = agb.copyActivity(USER_DB,
                            dc_board_kg,
                            'telecom boards')

telecom_board_kg.updateExchanges({
    'steel mix primary and recycled':120/200,
    'market for printed wiring board, surface mounted, unspecified, Pb free#GLO':80/200,})

count_board_kg = agb.copyActivity(USER_DB,
                            dc_board_kg,
                            'counting boards')

count_board_kg.updateExchanges({
    'steel mix primary and recycled':240/400,
    'market for printed wiring board, surface mounted, unspecified, Pb free#GLO':160/400,})

supervision_board_kg = agb.copyActivity(USER_DB,
                            telecom_board_kg,
                            'supervision boards')
```

###### Assembly

```python
offshore_sub_command_control_manufacturing_ref = agb.newActivity(USER_DB,
                             'manufacturing of telecom and control command of the reference offshore substation ',
                             unit = 'unit',
                             system_2 = OFFSHORE_SUB_EQUIPMENT,
                             exchanges = {
                                 dc_board_kg:11000,
                                 telecom_board_kg:1000,
                                 count_board_kg:1000,
                                 supervision_board_kg:1000,
                             })

mass_offshore_sub_command_control_ref=offshore_sub_command_control_manufacturing_ref.getAmount(['*'],sum=True)
```

##### HVAC Cooling

```python
# We introduce an activity for the HVAC cooling system of offshore substation 
offshore_sub_HVAC_cooling_manufacturing_ref = agb.newActivity(USER_DB,
                          'manufacturing of cooling for HVAC equipments of the reference offshore substation',
                          unit = 'unit',
                          phase = PHASE_1_MANUFACTURING,
                          system_2 = OFFSHORE_SUB_EQUIPMENT,
                          exchanges = {
                              steel_low_alloyed_mix: 185,
                              copper: 123,
                              aluminium_mix: 18,
                              brass: 3,
                              polyethylene_HD: 15,
                              polypropylene: 9,
                              polystyrene: 1+1,
                              wood_board: 42,
                              refrigerant: 17,
                              linerboard: 7,
                              electric_comp: 4,
                          })

mass_offshore_sub_HVAC_cooling_ref=offshore_sub_HVAC_cooling_manufacturing_ref.getAmount(['*'],sum=True)
```

#### Offshore substation equipment assembly

```python
# We introduce an activity for the offshore substation designed for a 600 MW offshore windfarm
offshore_sub_equipment_manufacturing_ref = agb.newActivity(USER_DB,
                       "manufacturing of the reference offshore substation equipments",
                       unit = "unit",
                       exchanges = {
                           offshore_sub_electric_components_manufacturing_ref:1,
                           offshore_sub_manipulation_equipment_manufacturing_ref:1,
                           offshore_sub_control_instrumentation_manufacturing_ref:1,
                           offshore_sub_security_scrap_equipment_manufacturing_ref:1,
                           offshore_sub_command_control_manufacturing_ref:1,
                           offshore_sub_HVAC_cooling_manufacturing_ref:1, })
```

####  2️⃣  4️⃣ Resizing masses

```python
MASS_OFFSHORE_SUB_EQUIPMENT_KG_REF=mass_offshore_sub_electric_components_ref+mass_offshore_sub_manipulation_equipment_ref+mass_offshore_sub_control_instrumentation_ref+mass_offshore_sub_security_scrap_equipment_ref+mass_offshore_sub_command_control_ref+mass_offshore_sub_HVAC_cooling_ref

#Formula
mass_offshore_sub_equipment_kg=MASS_OFFSHORE_SUB_EQUIPMENT_KG_REF*(power_tot_farm_MW/OFFSHORE_SUB_REF_POWER_MW)

#Automatic calculation
resizing_mass_offshore_sub_equipment=mass_offshore_sub_equipment_kg/MASS_OFFSHORE_SUB_EQUIPMENT_KG_REF
```

####  4️⃣ Resizing inventory

```python
offshore_sub_equipment_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of the equipment of the offshore substation",
                       unit = "unit",
                       exchanges = {offshore_sub_equipment_manufacturing_ref:resizing_mass_offshore_sub_equipment                         
             })
```

### Assembly

```python
offshore_sub_manufacturing = agb.newActivity(USER_DB,
                       "manufacturing of the offshore substation",
                        system_1=SUBSTATION,
                       unit = "unit",
                       exchanges = {
                           offshore_sub_structure_manufacturing:1,
                           offshore_sub_equipment_manufacturing:1                        
             })
```

```python
MASS_OFFSHORE_SUB_TOT_KG_REF=MASS_STRUCTURE_OFFSHORE_SUB_KG_REF+MASS_OFFSHORE_SUB_EQUIPMENT_KG_REF

values_table(
    MASS_OFFSHORE_SUB_TOT_KG_REF=(MASS_OFFSHORE_SUB_TOT_KG_REF,"kg"),
    MASS_STRUCTURE_OFFSHORE_SUB_KG_REF=(MASS_STRUCTURE_OFFSHORE_SUB_KG_REF, "kg"),
    MASS_OFFSHORE_SUB_EQUIPMENT_KG_REF=(MASS_OFFSHORE_SUB_EQUIPMENT_KG_REF, "kg"),
)

```

```python
mass_offshore_sub_tot_kg=mass_structure_offshore_sub_kg+mass_offshore_sub_equipment_kg

values_table(
    mass_offshore_sub_tot_kg=(mass_offshore_sub_tot_kg,"kg"),
    mass_structure_offshore_sub_kg=(mass_structure_offshore_sub_kg, "kg"),
    mass_offshore_sub_equipment_kg=(mass_offshore_sub_equipment_kg, "kg"),
)


```

### LCA RESULT: climate change impacts of wind turbine manufacturing

```python
#Climate change impact of the whole infrastructure
compute_impacts(
    offshore_sub_manufacturing,
    impacts_EF_CO2,
    axis="system_2")
```

```python
#Climate change impact per MW installed
#We use the function compute_impacts to resize the inventory (division per power_tot_farm_MW)
compute_impacts(
    offshore_sub_manufacturing,
    impacts_EF_CO2,
    functional_unit=power_tot_farm_MW)
```

```python
#Climate change impact per kWh of electricity produced
#We use the function compute_impacts to resize the inventory (division per elec_prod_lifetime_kWh)
compute_impacts(
    offshore_sub_manufacturing,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh)
```

## Masses  table

```python
# One wind turbine 
mass_intcables_alu_per_wind_turbine_kg=mass_intcables_alu_tot_kg/n_turbines


values_table(
    mass_one_wind_turbine_tot_kg=(mass_one_wind_turbine_tot_kg,"kg"),
    mass_intcables_alu_per_wind_turbine_kg=(mass_intcables_alu_per_wind_turbine_kg,"kg"),
    mass_foundations_gbf_tot_kg=(mass_foundations_gbf_tot_kg,"kg"),
    mass_foundations_tripod_tot_kg=(mass_foundations_tripod_tot_kg,"kg"),
    mass_foundations_monopile_tot_kg=(mass_foundations_monopile_tot_kg, "kg"),
    mass_foundations_jacket_tot_kg=(mass_foundations_tripod_tot_kg, "kg"),
    mass_foundations_spar_tot_kg=(mass_foundations_spar_tot_kg, "kg"),
    mass_foundations_semisub_tot_kg=(mass_foundations_semisub_tot_kg, "kg"),
    mass_foundations_custom_tot_kg=(mass_foundations_custom_tot_kg,"kg"),
    
)
```

```python
#At wind farm level

mass_wind_turbines_tot_kg=mass_one_wind_turbine_tot_kg*n_turbines
mass_foundations_gbf_tot_farm_kg=mass_foundations_gbf_tot_kg*n_turbines
mass_foundations_tripod_tot_farm_kg=mass_foundations_tripod_tot_kg*n_turbines
mass_foundations_monopile_tot_farm_kg=mass_foundations_monopile_tot_kg*n_turbines
mass_foundations_jacket_tot_farm_kg=mass_foundations_jacket_tot_kg*n_turbines
mass_foundations_spar_tot_farm_kg=mass_foundations_spar_tot_kg*n_turbines
mass_foundations_semisub_tot_farm_kg=mass_foundations_semisub_tot_kg*n_turbines
mass_foundations_custom_tot_farm_kg=mass_foundations_custom_tot_kg*n_turbines

values_table(
    mass_wind_turbines_tot_kg=(mass_wind_turbines_tot_kg,"kg"),
    mass_foundations_gbf_tot_farm_kg=(mass_foundations_gbf_tot_farm_kg,"kg"),
    mass_foundations_tripod_tot_farm_kg=(mass_foundations_tripod_tot_farm_kg,"kg"),
    mass_foundations_monopile_tot_farm_kg=(mass_foundations_monopile_tot_farm_kg, "kg"),
    mass_foundations_jacket_tot_farm_kg=(mass_foundations_jacket_tot_farm_kg, "kg"),
    mass_foundations_spar_tot_farm_kg=(mass_foundations_spar_tot_farm_kg, "kg"),
    mass_foundations_semisub_tot_farm_kg=(mass_foundations_semisub_tot_farm_kg, "kg"),
    mass_foundations_custom_tot_farm_kg=(mass_foundations_custom_tot_farm_kg,"kg"),
    mass_intcables_alu_tot_kg=(mass_intcables_alu_tot_kg,"kg"),
    mass_expcables_tot_kg=(mass_expcables_tot_kg,"kg"),
    mass_offshore_sub_tot_kg=(mass_offshore_sub_tot_kg,"kg"),
)

```

# Inventories : Transportation from manufacturing sites to the onshore site


## Wind turbines transport

```python
#We introduce an activity for the transport of the tower by lorry and container ship
one_tower_transport = agb.newActivity(USER_DB,
                       "transport of turbine tower",
                       unit = "unit",
                       phase = PHASE_2_TRANSPORT,
                       system_2 = TOWER,
                       exchanges = {                           
                           lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_tower_tot_kg,
                           container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_tower_tot_kg,             }) 
```

```python
#We introduce an activity for the transport of the rotor by lorry and container ship
one_rotor_transport = agb.newActivity(USER_DB,
                       "transport of rotor",
                       unit = "unit",
                       phase = PHASE_2_TRANSPORT,
                       system_2 = ROTOR,
                       exchanges = {
                            lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_rotor_tot_kg,
                            container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_rotor_tot_kg 
                       })
```

```python
#We introduce an activity for the transport of the nacelle by lorry and container ship
one_nacelle_transport = agb.newActivity(USER_DB,
                       "transport of nacelle",
                       unit = "unit",
                       phase = PHASE_2_TRANSPORT,
                       system_2 = NACELLE,
                       exchanges = {
                            lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_nacelle_tot_kg,
                            container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_nacelle_tot_kg
                       })
```

```python
#We introduce an activity for the transport of the wind turbines at wind farm level

wind_turbines_transport = agb.newActivity(USER_DB,
                       "transport of wind turbines",
                       unit = "unit",
                       system_1 = WIND_TURBINES,
                       exchanges = {
                           one_tower_transport:n_turbines,
                           one_rotor_transport:n_turbines,
                           one_nacelle_transport:n_turbines,
                          })
```

## Wind turbines foundations

```python
one_foundation_gbf_transport = agb.newActivity(USER_DB,
                                "transport of one gravity based foundation",
                                unit = "unit",
                                phase = PHASE_2_TRANSPORT,
                                system_1 = WT_FOUNDATIONS,
                                exchanges = {
                                    lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_foundations_gbf_tot_kg,
                                    container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_foundations_gbf_tot_kg                                })
```

```python
one_foundation_monopile_transport = agb.newActivity(USER_DB,
                                      "transport of one monopile foundation",
                                      unit = 'unit',
                                      phase = PHASE_2_TRANSPORT,
                                      system_1 = WT_FOUNDATIONS,
                                      exchanges = {
                                            lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_foundations_monopile_tot_kg,
                                            container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_foundations_monopile_tot_kg
                                      })
```

```python
one_foundation_tripod_transport = agb.newActivity(USER_DB,
                                   'transport of one tripod foundation',
                                   unit = 'unit',
                                   phase = PHASE_2_TRANSPORT,
                                   system_1 = WT_FOUNDATIONS,
                                   exchanges = {
                                            lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_foundations_tripod_tot_kg,
                                            container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_foundations_tripod_tot_kg  
                                   })
```

```python
one_foundation_jacket_transport = agb.newActivity(USER_DB,
                                   'transport of one jacket foundation',
                                   unit = 'unit',
                                   phase = PHASE_2_TRANSPORT,
                                   system_1 = WT_FOUNDATIONS,
                                   exchanges = {
                                            lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_foundations_jacket_tot_kg,
                                            container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_foundations_jacket_tot_kg  
                                   })
```

```python
one_foundation_spar_transport = agb.newActivity(USER_DB,
                                     'transport of one floating spar foundation',
                                      unit ='unit',
                                      phase = PHASE_2_TRANSPORT,
                                      system_1 = WT_FOUNDATIONS,
                                      exchanges = {
                                            lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_foundations_spar_tot_kg,
                                            container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_foundations_spar_tot_kg 
                                     })
```

```python
one_foundation_semisub_transport = agb.newActivity(USER_DB,
                                   'transport of one semi submersible foundation',
                                   unit = 'unit',
                                   phase = PHASE_2_TRANSPORT,
                                   system_1 = WT_FOUNDATIONS,
                                   exchanges = {
                                            lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_foundations_semisub_tot_kg,
                                            container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_foundations_semisub_tot_kg  
                                   })
```

```python
one_foundation_custom_transport = agb.newActivity(USER_DB,
                                     'transport of one customized foundation',
                                      phase = PHASE_2_TRANSPORT,
                                      system_1 = WT_FOUNDATIONS,
                                      unit ='unit',
                                      exchanges = {
                                            lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_foundations_custom_tot_kg,
                                            container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_foundations_custom_tot_kg  
                                     })
```

```python
#We introduce an activity for the transport of one foundations according to the type of foundations selected
one_foundation_transport = agb.newSwitchAct(
    USER_DB,
    "transport of one foundations",
    foundations_type,
    {
         "gbf": one_foundation_gbf_transport,
         "monopod": one_foundation_monopile_transport ,
         "tripod": one_foundation_tripod_transport,
         "jacket": one_foundation_jacket_transport,
         "floatingspar":one_foundation_spar_transport, 
         "jacket": one_foundation_jacket_transport,
         "custom":one_foundation_custom_transport
    })
```

```python
#We introduce an activity for the transport of the foundations at wind farm level
foundations_transport = agb.newActivity(USER_DB,
                       "transport of foundations of wind turbines",
                       unit = "unit",
                       exchanges = {
                           one_foundation_transport:n_turbines,
                          })
```

## Wind farm inter-array cables

```python
# We introduce an activity for transport of inter-array cable
intcables_transport = agb.newActivity (USER_DB, 
                                       "transport of inter-array cables",
                                       unit = "unit",
                                       phase =PHASE_2_TRANSPORT,
                                       system_1 = INT_CABLES,
                                       exchanges = {
                                       lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_intcables_alu_tot_kg,
                                       container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_intcables_alu_tot_kg,    
                                       })
```

## Wind farm export cables 

```python
#We introduce an activity for the transport of export cables by lorry and container ship
expcables_tranport = agb.newActivity(USER_DB,
                       "transport of export cables",
                       unit = "unit",
                       phase=PHASE_2_TRANSPORT,
                       system_1 = EXP_CABLES,
                       exchanges = {
                           lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_expcables_tot_kg,
                           container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_expcables_tot_kg,
                       })
agb.printAct(expcables_tranport)
```

## Offshore substation

```python
#We introduce an activity for the transport of offshore substation
offshore_sub_transport = agb.newActivity(USER_DB,
                       "transport of the offshore substation",
                       unit = "unit",
                       phase = PHASE_2_TRANSPORT,
                       system_1 = SUBSTATION,
                       exchanges = {
                           lorry_transp:0.001*d_manufacturingsite_onshoresite_lorry*mass_offshore_sub_tot_kg,
                           container_ship:0.001*d_manufacturingsite_onshoresite_ship*mass_offshore_sub_tot_kg
                       })  
```

# Inventories : Installation on the offshore area

Note : as the installation activities are reused for decomissioning stage, the flag "phase = PHASE_3_INSTALLATION" is done later at the decomissioning stage.


## Wind turbines and wind turbines foundations 


### Reference data

```python
#Saint-Nazaire data
WIND_TURBINES_INSTALL_HFO_L_REF= 18145*1000/HEAVY_FUEL_DENSITY_KG_L #L
WIND_TURBINES_INSTALL_DIESEL_L_REF=21462*1000 #L
WIND_TURBINES_INSTALL_FUEL_L_REF=WIND_TURBINES_INSTALL_HFO_L_REF+WIND_TURBINES_INSTALL_DIESEL_L_REF

WIND_TURBINES_INSTALL_NB_TURBINES_REF= 80 #turbines
WT_INSTALL_D_SHORE_KM_REF= 16 #km

ONE_WIND_TURBINE_INSTALL_FUEL_L_REF=WIND_TURBINES_INSTALL_FUEL_L_REF/WIND_TURBINES_INSTALL_NB_TURBINES_REF
```

###  2️⃣ Resized data

```python
#Proportionnal number of turbines and distance to shore
wind_turbines_install_hfo_L=WIND_TURBINES_INSTALL_HFO_L_REF * (n_turbines/WIND_TURBINES_INSTALL_NB_TURBINES_REF) * (d_shore/WT_INSTALL_D_SHORE_KM_REF) 
wind_turbines_install_diesel_L=WIND_TURBINES_INSTALL_DIESEL_L_REF * (n_turbines/WIND_TURBINES_INSTALL_NB_TURBINES_REF) * (d_shore/WT_INSTALL_D_SHORE_KM_REF)

wind_turbines_install_fuel_L=wind_turbines_install_hfo_L+wind_turbines_install_diesel_L
```

### 4️⃣ Inventory

```python
wind_turbines_install = agb.newActivity(USER_DB,
                                     'Installation of wind turbines and foundations',
                                     unit = 'unit',
                                     #phase = PHASE_3_INSTALLATION - as we reuse this activity for decommissionning stage, the flag is put later 
                                     system_1 = WT_WTFOUNDATIONS_INTCABLES,
                                     exchanges = {
                                         diesel_consumption: wind_turbines_install_diesel_L*DIESEL_CALORIFIC_VALUE_MJ_PER_L,
                                         hfo_consumption:wind_turbines_install_hfo_L*HEAVY_FUEL_CALORIFIC_VALUE_MJ_PER_L,
                                     })
```

## Inter array cables installation


### Reference data

```python
#Saint-Nazaire data

INTCABLES_INSTALL_HFO_L_REF= 3120*1000/HEAVY_FUEL_DENSITY_KG_L #L
INTCABLES_INSTALL_DIESEL_L_REF=0
INTCABLES_INSTALL_FUEL_L_REF=INTCABLES_INSTALL_HFO_L_REF+INTCABLES_INSTALL_DIESEL_L_REF

INTCABLES_INSTALL_TOT_LENGTH_M_REF=116000 #m
INTCABLES_INSTALL_PER_WINDTURBINE_FUEL_L_REF=INTCABLES_INSTALL_FUEL_L_REF/WIND_TURBINES_INSTALL_NB_TURBINES_REF
```

###  2️⃣ Resized data

```python
intcables_install_hfo_L=INTCABLES_INSTALL_HFO_L_REF*(length_tot_intcables_m/INTCABLES_INSTALL_TOT_LENGTH_M_REF)
intcables_install_diesel_L=INTCABLES_INSTALL_DIESEL_L_REF*(length_tot_intcables_m/INTCABLES_INSTALL_TOT_LENGTH_M_REF)
intcables_install_fuel_L=intcables_install_hfo_L+intcables_install_diesel_L
```

### 4️⃣ Inventory

```python
intcables_install = agb.newActivity (USER_DB, 
                "installation of interarray cables",
                system_1 =WT_WTFOUNDATIONS_INTCABLES,
                #phase=PHASE_3_INSTALLATION,
                 unit='unit', 
                 exchanges = {
                     diesel_consumption: intcables_install_diesel_L*DIESEL_CALORIFIC_VALUE_MJ_PER_L,              
                     hfo_consumption: intcables_install_hfo_L*HEAVY_FUEL_CALORIFIC_VALUE_MJ_PER_L,  
                                             })
```

## Export cables installation


### Reference data

```python
EXPCABLES_INSTALL_DIESEL_L_REF=(42.6*10+28.4*200)/2 #L
EXPCABLES_INSTALL_HFO_L_REF=(5000*80+2000*10+13400*45+16000*10+23800*2+20000*10+5000*10)/2 #L
EXPCABLES_INSTALL_FUEL_L_REF=EXPCABLES_INSTALL_DIESEL_L_REF+EXPCABLES_INSTALL_HFO_L_REF
```

###  2️⃣ Resized data

```python
expcables_install_diesel_L=EXPCABLES_INSTALL_DIESEL_L_REF*mass_expcables_tot_kg/MASS_EXPCABLES_TOT_KG
expcables_install_hfo_L=EXPCABLES_INSTALL_HFO_L_REF*mass_expcables_tot_kg/MASS_EXPCABLES_TOT_KG
expcables_install_fuel_L=expcables_install_diesel_L+expcables_install_hfo_L
```

### 4️⃣ Inventory

```python
expcables_install = agb.newActivity(USER_DB,
                       "installation of export cables - fuel consumption",
                       unit = "unit",
                       #phase = PHASE_3_INSTALLATION,
                       system_1 = EXP_CABLES, 
                       exchanges = {
                                   diesel_consumption: expcables_install_diesel_L*DIESEL_CALORIFIC_VALUE_MJ_PER_L,
                                   hfo_consumption: expcables_install_hfo_L*HEAVY_FUEL_CALORIFIC_VALUE_MJ_PER_L,  
                       })
```

## Offshore substation


### Reference data

```python
OFFSHORE_SUB_SHORE_DISTANCE_KM_REF=15 #km

OFFSHORE_SUB_INSTALL_HFO_L_REF=0
OFFSHORE_SUB_INSTALL_DIESEL_L_REF=(32000*3+ 41650*3*2+1666*30)/DIESEL_DENSITY_KG_L #L
OFFSHORE_SUB_INSTALL_FUEL_L_REF=OFFSHORE_SUB_INSTALL_HFO_L_REF+OFFSHORE_SUB_INSTALL_DIESEL_L_REF
```

###  2️⃣ Resized data

```python
offshore_sub_install_hfo_L=OFFSHORE_SUB_INSTALL_HFO_L_REF*(mass_offshore_sub_tot_kg/MASS_OFFSHORE_SUB_TOT_KG_REF)*(d_shore/OFFSHORE_SUB_SHORE_DISTANCE_KM_REF)
offshore_sub_install_diesel_L=OFFSHORE_SUB_INSTALL_DIESEL_L_REF*(mass_offshore_sub_tot_kg/MASS_OFFSHORE_SUB_TOT_KG_REF)*(d_shore/OFFSHORE_SUB_SHORE_DISTANCE_KM_REF)
offshore_sub_install_fuel_L=offshore_sub_install_hfo_L+offshore_sub_install_diesel_L
```

### 4️⃣ Inventory

```python
offshore_sub_install = agb.newActivity(USER_DB,
                       "installation of offshore substation - fuel consumption",
                       unit = "unit",
                       #phase = PHASE_3_INSTALLATION,
                       system_1 = SUBSTATION, 
                       exchanges = {               
                           diesel_consumption:offshore_sub_install_diesel_L*DIESEL_CALORIFIC_VALUE_MJ_PER_L,
                           hfo_consumption: offshore_sub_install_hfo_L*HEAVY_FUEL_CALORIFIC_VALUE_MJ_PER_L,
                       })
```

## Fuel consumption table

```python
#Saint Nazaire reference study

values_table(
    ONE_WIND_TURBINE_INSTALL_FUEL_L_REF=(ONE_WIND_TURBINE_INSTALL_FUEL_L_REF,"L"),
    INTCABLES_INSTALL_PER_WINDTURBINE_FUEL_L_REF=(INTCABLES_INSTALL_PER_WINDTURBINE_FUEL_L_REF,"L"),
        )
```

```python
#RTE Ref study
values_table(
    EXPCABLES_INSTALL_FUEL_L_REF=(EXPCABLES_INSTALL_FUEL_L_REF,"L"),
    OFFSHORE_SUB_INSTALL_FUEL_L_REF=(OFFSHORE_SUB_INSTALL_FUEL_L_REF,"L")
        )
```

```python
#Recalculated data
values_table(
    wind_turbines_install_fuel_L=(wind_turbines_install_fuel_L,"L"),
    intcables_install_fuel_L=(intcables_install_fuel_L,"L"),
    expcables_install_fuel_L=(expcables_install_fuel_L,"L"),
    offshore_sub_install_fuel_L=(offshore_sub_install_fuel_L,"L")
        )
```

# Inventories : Operation and maintenance


##  2️⃣  4️⃣  Wind turbines, wind turbines foundations, inter-array cables

```python
#REF DATA for oil taken from Kouloumpis 
WIND_TURBINE_MAINTENANCE_LIFETIME_YEAR_REF1=20 #years
WIND_TURBINE_MAINTENANCE_POWER_MW_REF1= 5 #MW
LUBRICANT_PER_WT_PER_YEAR_KG_REF1= 15.8 #kg

lubricant_WT_maintenance_kg=LUBRICANT_PER_WT_PER_YEAR_KG_REF1*n_turbines*life_time*turbine_MW/WIND_TURBINE_MAINTENANCE_POWER_MW_REF1

#REF DATA for diesel consumption taken from Bilan Carbone Saint Nazaire
WIND_TURBINE_MAINTENANCE_LIFETIME_YEAR_REF2= 25 #years
WIND_TURBINE_MAINTENANCE_SHORE_DISTANCE_KM_REF2=16 #km
DIESEL_PER_WT_PER_YEAR_L_REF2=7500 #L
HFO_PER_WT_PER_YEAR_L_REF2=0
FUEL_PER_WT_PER_YEAR_L_REF2=HFO_PER_WT_PER_YEAR_L_REF2+ DIESEL_PER_WT_PER_YEAR_L_REF2

wind_turbines_maintenance_diesel_L=DIESEL_PER_WT_PER_YEAR_L_REF2*n_turbines*life_time*(d_shore/WIND_TURBINE_MAINTENANCE_SHORE_DISTANCE_KM_REF2)
wind_turbines_maintenance_hfo_L=HFO_PER_WT_PER_YEAR_L_REF2*n_turbines*(life_time*d_shore/WIND_TURBINE_MAINTENANCE_SHORE_DISTANCE_KM_REF2)
wind_turbines_maintenance_fuel_L=wind_turbines_maintenance_hfo_L+wind_turbines_maintenance_diesel_L
fuel_per_WT_maintenance_L=wind_turbines_maintenance_fuel_L/n_turbines

wind_turbines_maintenance = agb.newActivity(USER_DB,
                                         'operation and maintenance of a reference windturbine for a xxx life time and xxx distance',
                                          unit = 'unit',
                                          phase = PHASE_4_OANDM,
                                          system_1 = WT_WTFOUNDATIONS_INTCABLES,
                                          exchanges = {
                                             lubricating_oil : lubricant_WT_maintenance_kg,
                                             oil_waste: lubricant_WT_maintenance_kg,
                                             
                                             diesel_consumption: wind_turbines_maintenance_diesel_L*DIESEL_CALORIFIC_VALUE_MJ_PER_L,
                                             hfo_consumption:wind_turbines_maintenance_hfo_L*HEAVY_FUEL_CALORIFIC_VALUE_MJ_PER_L,

                                          })
```

##  2️⃣  4️⃣ Wind turbine foundations

```python
foundations_maintenance = agb.newActivity(USER_DB, 
                                          'operation and maintenance of  foundations',
                                          #phase =PHASE_4_OANDM,
                                          #system_1 = WT_FOUNDATIONS,
                                          unit = 'unit', 
                                          exchanges = {
                                              diesel_consumption: 0,
                                              hfo_consumption: 0,
                                          })
```

##  2️⃣  4️⃣ Interarray cables

```python
intcables_maintenance = agb.newActivity(USER_DB, 
                                   'maintenance of the interarray cables',
                                   unit = 'unit',
                                  #phase =PHASE_4_OANDM,
                                  #system_1= INT_CABLES,
                                   exchanges = {
                                              diesel_consumption: 0,
                                              hfo_consumption: 0,
                                   })
```

## 2️⃣  4️⃣ Export cables

```python
EXPCABLES_LIFETIME_REF=40 #year
ONE_EXPCABLE_LENGTH_KM_REF=30000 #m
EXPORT_CABLES_POWER_MW_REF=300 #MW   (source: RTE report)

EXPCABLES_PREVENTIVE_MAINTENANCE_HFO_L_REF=13400*60 #L
EXPCABLES_PREVENTIVE_MAINTENANCE_DIESEL_L_REF=0
EXPCABLES_PREVENTIVE_MAINTENANCE_FUEL_L_REF=EXPCABLES_PREVENTIVE_MAINTENANCE_HFO_L_REF+EXPCABLES_PREVENTIVE_MAINTENANCE_DIESEL_L_REF

expcables_preventive_maintenance_hfo_L=EXPCABLES_PREVENTIVE_MAINTENANCE_HFO_L_REF*(life_time/EXPCABLES_LIFETIME_REF)*(length_1_expcable_tot/ONE_EXPCABLE_LENGTH_KM_REF)*(power_tot_farm_MW/EXPORT_CABLES_POWER_MW_REF)
expcables_preventive_maintenance_diesel_L=EXPCABLES_PREVENTIVE_MAINTENANCE_DIESEL_L_REF*(life_time/EXPCABLES_LIFETIME_REF)*(length_1_expcable_tot/ONE_EXPCABLE_LENGTH_KM_REF)*(power_tot_farm_MW/EXPORT_CABLES_POWER_MW_REF)
expcables_preventive_maintenance_fuel_L=expcables_preventive_maintenance_hfo_L+expcables_preventive_maintenance_diesel_L
```

```python
expcables_maintenance = agb.newActivity(USER_DB, 
                                   'maintenance of the export cables',
                                   unit = 'unit',
                                  phase =PHASE_4_OANDM,
                                  system_1= EXP_CABLES,
                                   exchanges = {
                                       diesel_consumption: expcables_preventive_maintenance_diesel_L*DIESEL_CALORIFIC_VALUE_MJ_PER_L,
                                       hfo_consumption:expcables_preventive_maintenance_hfo_L*HEAVY_FUEL_CALORIFIC_VALUE_MJ_PER_L,
                                   })
```

## 2️⃣  4️⃣ Offshore substation 

```python
SUBSTATION_LIFETIME_REF=25 #year
SUBSTATION_SHORE_DISTANCE_KM_REF=15 #km

OFFSHORE_SUB_PREVENTIVE_MAINTENANCE_DIESEL_L_REF=41650/DIESEL_DENSITY_KG_L #L
OFFSHORE_SUB_PREVENTIVE_MAINTENANCE_HFO_L_REF=0 #L

offshore_sub_preventive_maintenance_diesel_L=OFFSHORE_SUB_PREVENTIVE_MAINTENANCE_DIESEL_L_REF*(life_time/SUBSTATION_LIFETIME_REF)*(power_tot_farm_MW/OFFSHORE_SUB_REF_POWER_MW)*(d_shore/SUBSTATION_SHORE_DISTANCE_KM_REF)
offshore_sub_preventive_maintenance_hfo_L=OFFSHORE_SUB_PREVENTIVE_MAINTENANCE_HFO_L_REF*(life_time/SUBSTATION_LIFETIME_REF)*(power_tot_farm_MW/OFFSHORE_SUB_REF_POWER_MW)*(d_shore/SUBSTATION_SHORE_DISTANCE_KM_REF)
offshore_sub_preventive_maintenance_fuel_L=offshore_sub_preventive_maintenance_diesel_L+offshore_sub_preventive_maintenance_hfo_L

OFFSHORE_SUB_POWER_GENERATOR_DIESEL_L_REF=29155/DIESEL_DENSITY_KG_L #L
offshore_sub_power_generator_diesel_L=OFFSHORE_SUB_POWER_GENERATOR_DIESEL_L_REF*life_time/SUBSTATION_LIFETIME_REF*power_tot_farm_MW/OFFSHORE_SUB_REF_POWER_MW*(d_shore/SUBSTATION_SHORE_DISTANCE_KM_REF)

offshore_sub_maintenance = agb.newActivity(USER_DB, 
                                    'maintenance of offshore substation in the reference study',
                                     unit = 'unit',
                                    phase = PHASE_4_OANDM,
                                    system_1 = SUBSTATION,
                                     exchanges = {
                                         diesel_consumption:offshore_sub_preventive_maintenance_diesel_L*DIESEL_CALORIFIC_VALUE_MJ_PER_KG,
                                         hfo_consumption:offshore_sub_preventive_maintenance_hfo_L*HEAVY_FUEL_CALORIFIC_VALUE_MJ_PER_L,
                                         diesel_maintenance: offshore_sub_power_generator_diesel_L*DIESEL_CALORIFIC_VALUE_MJ_PER_KG
                                     })
```

## Fuel consumption table

```python
#Per wind turbines
#Fuel for Wind turbines, foundations and export cables

values_table(
    FUEL_PER_WT_PER_YEAR_L_REF2=(FUEL_PER_WT_PER_YEAR_L_REF2,"L"),
    fuel_per_WT_maintenance_L=(fuel_per_WT_maintenance_L,"L")
)
```

```python
#At farm level
values_table(
    wind_turbines_maintenance_fuel_L=(wind_turbines_maintenance_fuel_L,"L"),
    expcables_preventive_maintenance_fuel_L=(expcables_preventive_maintenance_fuel_L,"L"),
    offshore_sub_preventive_maintenance_fuel_L=(offshore_sub_preventive_maintenance_fuel_L,"L"),
    offshore_sub_power_generator_diesel_L=(offshore_sub_power_generator_diesel_L,"L")
)
```

 # Inventories : Decommissioning


## Wind turbines and foundations

```python
wind_turbines_decommissioning = agb.copyActivity(USER_DB,
                wind_turbines_install,
               "decomissioning of wind turbines",
                unit="unit",
                #phase=PHASE_5_DECOM,
                #system_1 = WIND_TURBINES,
)


wind_turbines_install["phase"]=PHASE_3_INSTALLATION
wind_turbines_install.save() #we must do that to save this change in the database

wind_turbines_decommissioning["phase"]=PHASE_5_DECOM
wind_turbines_decommissioning.save()
```

## Export cables

```python
expcables_decommissioning = agb.copyActivity(USER_DB,
                expcables_install,
                "decomissioning of export cables",
                unit="unit",
                #phase=PHASE_5_DECOM,
                #system_1 = EXP_CABLES,
)

expcables_install["phase"]=PHASE_3_INSTALLATION
expcables_install.save() #we must do that to save this change in the database

expcables_decommissioning["phase"]=PHASE_5_DECOM
expcables_decommissioning.save()
```

## Interarray cables

```python
intcables_decommissioning = agb.copyActivity(USER_DB,
                intcables_install,
                "decomissioning of interarray cables",
                unit="unit",
                #phase=PHASE_5_DECOM,
                #system_1 = INT_CABLES,
)

intcables_install["phase"]=PHASE_3_INSTALLATION
intcables_install.save() #we must do that to save this change in the database

intcables_decommissioning["phase"]=PHASE_5_DECOM
intcables_decommissioning.save()
```


 ## Offshore substation

```python
offshore_sub_decommissioning = agb.copyActivity(USER_DB,
                offshore_sub_install,
                "decomissioning of offshore substation",
                unit="unit",
                #phase=PHASE_5_DECOM,
                #system_1 = SUBSTATION,
)

offshore_sub_install["phase"]=PHASE_3_INSTALLATION
offshore_sub_install.save() #we must do that to save this change in the database

offshore_sub_decommissioning["phase"]=PHASE_5_DECOM
offshore_sub_decommissioning.save()
```

# Inventories : End of Life


## Wind turbines


### Tower 

```python
one_tower_endoflife = agb.newActivity (USER_DB, 
                           'end of life treatment of one tower ',
                           unit= 'unit',
                           phase = PHASE_6_EOL,
                           system_2 = TOWER,
                           exchanges = {
                                landfill_steel: (1-steel_recycled_share_OUT) * mass_tower_steel_kg,
                                #steel_recycled: steel_recycled_share_OUT* mass_tower_steel_kg*0,

                                landfill_aluminium: alu_landfill_share_correc * mass_tower_alu_kg,
                                incineration_aluminium: alu_incineration_share_correc*mass_tower_alu_kg,
                                #alu_recycled:alu_recycled_share_OUT_correc*mass_tower_alu_kg,

                           })

agb.printAct(one_tower_endoflife)
```

### Rotor 

```python
one_rotor_endoflife = agb.newActivity(USER_DB,
                          'end of life treatment of one rotor',
                          unit = 'unit',
                           phase = PHASE_6_EOL,
                           system_2 = ROTOR,
                          exchanges = {                            
                              landfill_glassfibre:mass_rotor_glass_fiber_kg,
                              landfill_epoxy:mass_rotor_epoxy_kg,
                              landfill_wood:mass_rotor_wood_mix_kg,
                              incineration_plastic : mass_rotor_polypropylene_kg,
                          })
agb.printAct(one_rotor_endoflife)          
```

### Nacelle 

```python
one_nacelle_endoflife = agb.newActivity(USER_DB, 
                            'end of life treatment of one nacelle',
                           unit = 'unit',
                           phase = PHASE_6_EOL,
                           system_2 = NACELLE,
                            exchanges = {
                                landfill_steel:(1-steel_recycled_share_OUT)*(mass_nacelle_cast_iron_kg+mass_nacelle_steel_mix_kg+mass_nacelle_chromium_steel_kg),
                                #steel_recycled: steel_recycled_share_OUT *(mass_nacelle_cast_iron_kg+mass_nacelle_steel_mix_kg+mass_nacelle_chromium_steel_kg),
                                
                                landfill_copper:copper_landfill_share_correc*mass_nacelle_copper_kg,
                                incineration_copper: copper_incineration_share_correc*mass_nacelle_copper_kg,
                                #copper_recycled:*copper_recycled_share_OUT*mass_nacelle_copper_kg,

                                landfill_aluminium:alu_landfill_share_correc*mass_nacelle_aluminium_mix_kg,
                                incineration_aluminium:alu_incineration_share_correc*mass_nacelle_aluminium_mix_kg,
                                #alu_recycled:alu_recycled_share_OUT_correc*mass_nacelle_aluminium_mix_kg,
                                
                                incineration_plastic:mass_nacelle_polyethylene_kg,  
                                landfill_glassfibre:mass_nacelle_glass_fiber_kg,

                            })
agb.printAct(one_nacelle_endoflife)          
```

### Wind Turbines 

```python
wind_turbines_endoflife = agb.newActivity(USER_DB,
                       "end of life of wind turbines",
                        system_1 = WIND_TURBINES,
                       unit = "unit",
                       exchanges = {
                           one_tower_endoflife:n_turbines,
                           one_rotor_endoflife:n_turbines,
                           one_nacelle_endoflife:n_turbines,
                          })
```

## Wind turbines foundations

```python
one_foundation_gbf_endoflife = agb.newActivity(USER_DB,
                                "end of life treatment of one gravity based foundations",
                                 unit = "unit",
                                 phase = PHASE_6_EOL,
                                 system_1 = WT_FOUNDATIONS,
                                exchanges = {
                                    landfill_steel:(1-steel_recycled_share_OUT)*mass_foundation_gbf_steel_reinforcing_kg,
                                    #steel_recycled:steel_recycled_share_OUT*mass_foundation_gbf_steel_reinforcing_kg,
                                    
                                    landfill_concrete:(1-concrete_recycled_share_OUT)*mass_foundation_gbf_concrete_kg,
                                    #recycling_concrete: concrete_recycled_share_OUT* mass_foundation_gbf_concrete_kg,
                                    
                                    #mass_foundation_gbf_gravel_kg
                                    
                                })

#agb.findTechAct("gravel*", single=False)
```

```python
one_foundation_monopile_endoflife = agb.newActivity(USER_DB,
                                      "end of life treatment for one monopile foundation",
                                      unit = 'unit',
                                      phase = PHASE_6_EOL,
                                      system_1 = WT_FOUNDATIONS,
                                      exchanges = {
                                          landfill_steel:(1-steel_recycled_share_OUT)*mass_foundation_monopile_steel_mix_kg,
                                          #steel_recycled:*steel_recycled_share_OUT*mass_foundation_monopile_steel_mix_kg,
                                          
                                          landfill_concrete:(1-concrete_recycled_share_OUT)*mass_foundation_monopile_concrete_kg,
                                          #recycling_concrete: concrete_recycled_share_OUT*mass_foundation_monopile_concrete_kg,
                                      })

```

```python
one_foundation_tripod_endoflife = agb.newActivity(USER_DB,
                                   'end of life treatment of one tripod foundation',
                                   unit = 'unit',
                                   phase = PHASE_6_EOL,
                                   system_1 = WT_FOUNDATIONS,
                                   exchanges = {
                                       landfill_steel:(1-steel_recycled_share_OUT)* mass_foundation_tripod_steel_mix_kg,
                                       #steel_recycled:*steel_recycled_share_OUT* mass_foundation_tripod_steel_mix_kg,
                                       
                                       landfill_concrete:(1-concrete_recycled_share_OUT)*mass_foundation_tripod_concrete_kg,
                                       #recycling_concrete:concrete_recycled_share_OUT*mass_foundation_tripod_concrete_kg,
                                       })

```

```python
one_foundation_jacket_endoflife = agb.newActivity(USER_DB,
                                   'end of life treatment of one jacket foundation',
                                   unit = 'unit',
                                   phase = PHASE_6_EOL,
                                   system_1 = WT_FOUNDATIONS,
                                   exchanges = {
                                       landfill_steel:(1-steel_recycled_share_OUT)* mass_foundation_jacket_steel_mix_kg,
                                       })

```

```python
one_foundation_spar_endoflife = agb.newActivity(USER_DB,
                                     'end of life treatment for floating spar foundation',
                                      unit ='unit',
                                      phase = PHASE_6_EOL,
                                      system_1 = WT_FOUNDATIONS,
                                      exchanges = {
                                         landfill_steel:(1-steel_recycled_share_OUT)*(mass_foundation_spar_steel_low_alloyed_kg+mass_foundation_spar_steel_high_alloyed_kg),
                                         #steel_recycled:steel_recycled_share_OUT*(mass_foundation_spar_steel_low_alloyed_kg+mass_foundation_spar_steel_high_alloyed_kg)

                                          # mass_foundation_spar_gravel_ballast_kg +mass_foundation_spar_gravel_mooring_kg) > end of life of gravel is not considered
                                     })
```

```python
one_foundation_semisub_endoflife = agb.newActivity(USER_DB,
                                   'end of life treatment of one semi submersible foundation',
                                   unit = 'unit',
                                   phase = PHASE_6_EOL,
                                   system_1 = WT_FOUNDATIONS,
                                   exchanges = {
                                       landfill_steel:(1-steel_recycled_share_OUT)* mass_foundation_semisub_steel_mix_kg,
                                       #steel_recycled:*steel_recycled_share_OUT* mass_foundation_tripod_steel_mix_kg,
                                       })
```

```python
one_foundation_custom_endoflife = agb.newActivity(USER_DB,
                                      "end of life treatment of one customesed foundation",
                                      unit = 'unit',
                                      phase = PHASE_6_EOL,
                                      system_1 = WT_FOUNDATIONS,
                                      exchanges = {
                                          landfill_steel:(1-steel_recycled_share_OUT)*mass_foundation_custom_steel_kg,
                                          #steel_recycled:*steel_recycled_share_OUT*mass_foundation_custom_steel_kg,
                                          
                                          landfill_concrete:(1-concrete_recycled_share_OUT)*mass_foundation_custom_concrete_kg,
                                          #recycling_concrete: concrete_recycled_share_OUT*mass_foundation_custom_concrete_kg,
                                          
                                          # mass_foundation_custom_gravel_kg > end of life of gravel is not considered
                                      })
```

```python
one_foundation_endoflife = agb.newSwitchAct(
    USER_DB,
    "end of life of one foundation",
    foundations_type,
    {
         "gbf": one_foundation_gbf_endoflife,
         "monopod": one_foundation_monopile_endoflife ,
         "tripod": one_foundation_tripod_endoflife,
         "jacket": one_foundation_jacket_endoflife,
         "floatingspar":one_foundation_spar_endoflife,
         "semisub": one_foundation_semisub_endoflife,
         "custom":one_foundation_custom_endoflife
    })
```

```python
#We introduce an activity for the transport of the foundations at wind farm level
foundations_endoflife = agb.newActivity(USER_DB,
                       "end of life of foundations of wind turbines",
                       unit = "unit",
                       exchanges = {
                           one_foundation_endoflife:n_turbines,
                          })
```

## Inter-array cables

```python
intcables_endoflife = agb.newActivity(USER_DB,
                       "end of life of interarray cables",
                       unit = "unit",
                       phase = PHASE_6_EOL,
                       system_1 = INT_CABLES,
                       exchanges = {
                           
                            landfill_aluminium: alu_landfill_share_correc*mass_alu_intcables_alu, 
                            incineration_aluminium: alu_incineration_share_correc*mass_alu_intcables_alu,
                            #alu_recycled:alu_recycled_share_OUT_correc*mass_alu_expcables_alu,
                           
                           landfill_steel: (1-steel_recycled_share_OUT)*mass_steel_intcables_alu,
                           #steel_recycled: steel_recycled_share_OUT*mass_steel_intcables_alu,
                           
                           landfill_lead: mass_lead_intcables_alu,
                           landfill_polyethylene : mass_polyethylene_HD_intcables_alu,
                           incineration_plastic : mass_polypropylene_HD_intcables_alu,
                           landfill_glassfibre: mass_glass_fibre_HD_intcables_alu,
                       })
```

## Export Cables

```python
expcables_alu_endoflife = agb.newActivity(USER_DB,
                       "end of life treatment of export aluminium cables",
                       unit = "unit",
                       phase = PHASE_6_EOL,
                       system_2 = ALU_EXP_CABLES,
                       exchanges = {
                                landfill_aluminium: alu_landfill_share_correc*mass_alu_expcables_alu, 
                                incineration_aluminium: alu_incineration_share_correc*mass_alu_expcables_alu,
                                #alu_recycled:alu_recycled_share_OUT_correc*mass_alu_expcables_alu, 
                           
                                landfill_steel: (1-steel_recycled_share_OUT)*mass_steel_expcables_alu,
                                #steel_recycled: steel_recycled_share_OUT *mass_steel_expcables_alu,
                           
                                landfill_lead: mass_lead_expcables_alu,
                                landfill_polyethylene : mass_polyethylene_HD_expcables_alu,
                                incineration_plastic :mass_polypropylene_HD_expcables_alu,
                                landfill_glassfibre:mass_glass_fibre_HD_expcables_alu,                  
                                                       })


```

```python
expcables_cop_endoflife = agb.newActivity(USER_DB,
                       "end of life treatment of export copper cables",
                       unit = "unit",
                       phase = PHASE_6_EOL,
                       system_2 = COP_EXP_CABLES,
                       exchanges = {
                            landfill_copper:copper_landfill_share_correc*mass_cop_expcables_cop,
                            incineration_copper: copper_incineration_share_correc*mass_cop_expcables_cop,
                            #copper_recycled:*copper_recycled_share_OUT*mass_cop_expcables_cop,
                           
                           landfill_steel: (1-steel_recycled_share_OUT)*mass_steel_expcables_cop,
                           #steel_recycled: steel_recycled_share_OUT*mass_steel_expcables_cop*0,
                           
                           landfill_lead: mass_lead_expcables_cop,
                           landfill_polyethylene : mass_polyethylene_HD_expcables_cop,
                           
                           incineration_plastic : mass_polypropylene_HD_expcables_cop,
                           landfill_glassfibre: mass_glass_fibre_HD_expcables_cop,  
                       })
```

```python
# We introduce an activity for the export cables that are composed of aluminium and copper cables
expcables_endoflife = agb.newActivity(USER_DB,
                       "end of life of export cables",
                       unit = "unit",
                       system_1 = EXP_CABLES,
                       exchanges = {
                           expcables_alu_endoflife :1,
                           expcables_cop_endoflife:1,
                          })
```

## Offshore substation


### Offshore substation substructure

```python
sacrificial_anode_eol_ref = agb.newActivity(USER_DB,
                            'end of life treatment for sacrificial anode_offshore substation structure',
                            unit = 'unit',
                            exchanges = {
                                landfill_aluminium: alu_landfill_share_correc*14099/15000,
                                incineration_aluminium:alu_incineration_share_correc*14099/15000,
                                #alu_recycled:alu_recycled_share_OUT_correc*14099/15000,
                                
                               landfill_copper:copper_landfill_share_correc*0.45/15000,
                               incineration_copper: copper_incineration_share_correc*0.45/15000,
                               #copper_recycled:*copper_recycled_share_OUT*0.45/15000,
                                
                                landfill_zinc: 862.5/15000,
                                landfill_inert: (3+0.3)/15000,
                                landfill_steel: 9/15000,
                                landfill_silicon: 18/15000,
                   
                            })

offshore_sub_structure_eol = agb.newActivity(USER_DB,
                                    "end of life treatment for offshore substation structure",
                                    unit = 'unit',                                            
                                    phase =PHASE_6_EOL,
                                    system_2 = OFFSHORE_SUB_STRUCTURE,

                                    exchanges = {
                                        landfill_steel :(1-steel_recycled_share_OUT)* mass_steel_struture_offshore_sub_kg,
                                        #steel_recycled: steel_recycled_share_OUT*(700000 + 875000 + 747000),
                                        
                                        landfill_zinc: (22000*0.85*100/ZINC_COATING)*resizing_mass_offshore_sub_struture,
                                        sacrificial_anode_eol_ref : mass_anode_struture_offshore_sub_kg, 
                                    })
```

### Electric components

```python
TSA_1MVA_eol_ref = agb.newActivity(USER_DB,
                      'end of life treatment for TSA, 1MVA 66/0.4kv',
                      unit= 'kg',
                      exchanges = {
                          landfill_steel :(1-steel_recycled_share_OUT)* (2600+2200)/10250,
                          #steel_recycled: steel_recycled_share_OUT * (2600+2200)/10250,
                          
                          landfill_copper:copper_landfill_share_correc*1450/10250,
                          incineration_copper: copper_incineration_share_correc*1450/10250,
                          #copper_recycled:*copper_recycled_share_OUT*1450/10250,
                        
                          landfill_paperboard : 1000*0.5/10250,
                          oil_waste: 2000/10250,
                          landfill_epoxy: 100/10250,
                      })
```

```python
batteries_eol_ref = agb.newActivity(USER_DB,
                       'end of life treatment of Batteries 15, 20 and 50kw, 8h, 48, 127 and 400 VDC',
                       unit = 'kg',
                       exchanges = {
                           landfill_lead: (5797+5478)/16600,                      
                           incineration_plastic: 1328/16600,
                           landfill_hazard_waste: (1222+115)/16600,                   
                           landfill_inert: 90*2/16600,                  
                       })

cooling_radiators_eol_ref = agb.newActivity(USER_DB, 
                          'end of life treatment for cooling radiators, elevating transformer',
                          unit = 'kg',
                          exchanges = {
                              landfill_steel: 50000/60000,
                              oil_waste: 10000/60000,
                          })

transformers_330MVA_eol_ref = agb.newActivity(USER_DB, 
                                 'end of life treatment for transformers 330MVA-225-66kv',
                                 unit= 'kg',
                                 exchanges = {
                                     landfill_steel: (1-steel_recycled_share_OUT)*130000/275000,
                                     #steel_recycled:steel_recycled_share_OUT * 130000/275000, 

                                    landfill_copper:copper_landfill_share_correc*30000/275000, 
                                    incineration_copper: copper_incineration_share_correc*30000/275000, 
                                    #copper_recycled:*copper_recycled_share_OUT*30000/275000, 

                                     landfill_paperboard: 15000*0.5/275000,                  
                                     oil_waste: 100000/275000,                                   
                                 })


psem_cells_225kv_eol_ref = agb.newActivity(USER_DB,
                        'end of life tratment for PSEM cells 225kv',
                        unit = 'kg',
                        exchanges = {
                            landfill_aluminium:alu_landfill_share_correc*3440/5580,
                            incineration_aluminium: alu_incineration_share_correc*3440/5580,
                            #alu_recycled: alu_recycled_share_OUT_correc*3440/5580,
                            
                            landfill_steel: (1-steel_recycled_share_OUT)* (1380+240)/5580,
                            #steel_recycled:steel_recycled_share_OUT *1380/5580,       
                            
                            landfill_epoxy: 150/5580,
                            landfill_hazard_waste: 150/5580,
                            
                            landfill_copper:copper_landfill_share_correc*90/5580, 
                            incineration_copper: copper_incineration_share_correc*90/5580,
                            #copper_recycled:*copper_recycled_share_OUT*90/5580,,
                            
                            landfill_polyethylene: 80/5580,
                        })


psem_cells_66kv_eol_ref = agb.newActivity(USER_DB,
                             'end of life treatment for PSEM cells 66kv',
                             unit = 'kg',
                             exchanges = {
                                landfill_aluminium:alu_landfill_share_correc*1893/3062,
                                incineration_aluminium: alu_incineration_share_correc*1893/3062,
                                #alu_recycled: alu_recycled_share_OUT_correc*1893/3062,
                                 
                                landfill_steel: (1-steel_recycled_share_OUT)* 645/3062,
                                #steel_recycled:steel_recycled_share_OUT *645/3062,
                                 
                                 landfill_copper:copper_landfill_share_correc*70/3062,
                                 incineration_copper: copper_incineration_share_correc*70/3062,
                                 #copper_recycled:*copper_recycled_share_OUT*70/3062,
                                 
                                 landfill_polyethylene: (230+2)/3062,
                                 landfill_hazard_waste: 101/3062,
                                 landfill_epoxy: 89/3062,
                                 landfill_rubber: 10/3062,
                                 landfill_PTFE:8/3062,
                                 landfill_paperboard: 6/3062,
                                 incineration_plastic: (3+1)/3062,
                                 landfill_zeolite: 2/3062,          
                             })

electric_components_eol_ref = agb.newActivity(USER_DB, 
                                 'end of life treatment for electric components materials of offshore subsation',
                                 unit = 'unit',
                                  phase =PHASE_6_EOL,
                                  system_2 = OFFSHORE_SUB_EQUIPMENT,
                                  exchanges = {
                                     TSA_1MVA_eol_ref: 41000,
                                     batteries_eol_ref: 33000,
                                     cooling_radiators_eol_ref: 120000,
                                     psem_cells_225kv_eol_ref:11000,
                                     psem_cells_66kv_eol_ref:61000,
                                     transformers_330MVA_eol_ref: 5500,
                                 }) 
```

### Manipulation equipment

```python
manipulate_equip_eol_ref = agb.newActivity(USER_DB,
                              'end of life tratment for manipulation equipment',
                              unit = 'unit',
                               phase =PHASE_6_EOL,
                               system_2 = OFFSHORE_SUB_EQUIPMENT,
                              exchanges = {
                                  landfill_steel: (1 - steel_recycled_share_OUT)*1,
                                  #steel_recycled: steel_recycled_share_OUT*1,
                              })
```

### Control instrumentation

```python
diesel_generator_1000_eol_ref = agb.newActivity(USER_DB,
                              'end of life treatment for diesel generator 100kVA',
                                   unit = "kg",
                                   exchanges = {
                                       landfill_aluminium: alu_landfill_share_correc*150/5791,
                                       incineration_aluminium:alu_incineration_share_correc*150/5791,
                                       #alu_recycled:alu_recycled_share_OUT_correc*150/5791,

                                      landfill_copper:copper_landfill_share_correc*250/5791,
                                      incineration_copper: copper_incineration_share_correc*250/5791,
                                      #copper_recycled:*copper_recycled_share_OUT*250/5791,

                                       landfill_alkyd: 25/5791,
                                       landfill_inert: (0.5+190)/5791,                                 
                                       landfill_paperboard: 1.16/5791,
                                       landfill_polyethylene: 14/5791,
                                       landfill_steel: (1 - steel_recycled_share_OUT)*(250+4850)/5791,
                                       #steel_recycled: steel_recycled_share_OUT*(250+4850)/5791    
                                   })

control_instrumentation_eol_ref = agb.newActivity(USER_DB,
                                     'end of life treatment for control instrumentation',
                                     unit = "unit",
                                    phase =PHASE_6_EOL,
                                  system_2 = OFFSHORE_SUB_EQUIPMENT,
                                      exchanges = {
                                          diesel_generator_1000_eol_ref: 6000,                                                         
                                      })
```

### Security scrap equipment

```python
tank_sump_eol_ref = acts = agb.newActivity(USER_DB,
                       'end of life treatment for sump tank drum and pump',
                       unit = 'kg',
                       exchanges = {
                           
                           landfill_copper:copper_landfill_share_correc*158/3830,
                           incineration_copper: copper_incineration_share_correc*158/3830,
                           #copper_recycled:*copper_recycled_share_OUT*158/3830,
            
                           landfill_alkyd: 47/3830,
                           landfill_steel: 11/3830,
                           landfill_inert: (2+47)/3830,          
                           landfill_polyethylene: 4/3830,
                           
                           landfill_steel: (1-steel_recycled_share_OUT)*3560/3830,
                           #steel_recycled: steel_recycled_share_OUT * 3560/3830,
                       })

diesel_tank_eol_ref = agb.copyActivity(USER_DB,
    tank_sump_eol_ref, #initial activity 
    "end of life treatment for diesel tank 3000L")

security_scrap_equipment_eol_ref = agb.newActivity(USER_DB,
                                      'end of life treatment for equipment water-scrap-safety',
                                      unit = 'unit',
                                     phase =PHASE_6_EOL,
                                     system_2 = OFFSHORE_SUB_EQUIPMENT,
                                      exchanges = {
                                          tank_sump_eol_ref:8000,
                                          diesel_tank_eol_ref:12000,
                                      })
```

### HVAC Cooling

```python
HVAC_cooling_eol_ref = agb.newActivity(USER_DB,
                          'end of life treatment for cooling for HVAC equipments',
                          unit = 'kg',
                          phase =PHASE_6_EOL,
                          system_2 = OFFSHORE_SUB_EQUIPMENT,
                          exchanges = {
                              landfill_steel:(1-steel_recycled_share_OUT)*185/430,
                              #steel_recycled: steel_recycled_share_OUT *185/430,
                              
                              landfill_copper:copper_landfill_share_correc*123/430,
                              incineration_copper: copper_incineration_share_correc*123/430,
                              #copper_recycled:*copper_recycled_share_OUT*123/430,
                              
                              landfill_aluminium: alu_landfill_share_correc*18/430,
                              incineration_aluminium: alu_incineration_share_correc*18/430,
                              #alu_recycled: alu_recycled_share_OUT_correc*18/430,
                              
                              landfill_inert: 3/430,
                              landfill_polyethylene: 15/430,
                              incineration_plastic: 9/430,
                              landfill_polystyrene: 1/430,                           
                              landfill_hazard_waste: 17/430,
                              landfill_paperboard: 7/430,                      
                          })
```

### Offshore substation assembly

```python
offshore_sub_endoflife = agb.newActivity(USER_DB,
                       "end of life treatment of offshore substation",
                       unit = "unit",
                       phase = PHASE_6_EOL,
                       system_1 = SUBSTATION,
                       exchanges = {
                           offshore_sub_structure_eol:1,
                           electric_components_eol_ref:resizing_mass_offshore_sub_equipment,
                           manipulate_equip_eol_ref:resizing_mass_offshore_sub_equipment,
                           control_instrumentation_eol_ref:resizing_mass_offshore_sub_equipment,
                           security_scrap_equipment_eol_ref:resizing_mass_offshore_sub_equipment,
                           HVAC_cooling_eol_ref:resizing_mass_offshore_sub_equipment,
                       })

```

# Life Cycle Model assembly per phase 


## Manufacturing and assembly of components

```python
manufacturing_phase1 = agb.newActivity(USER_DB, 
                                    'manufacturing of components, life cycle phase 1',
                                    unit = 'unit',
                                    exchanges = {
                                        wind_turbines_manufacturing:1,
                                        foundations_manufacturing:1,
                                        intcables_manufacturing:1,
                                        expcables_manufacturing:1,
                                        offshore_sub_manufacturing:1,
                                    })
```

## Transport from the manufacturing sites to the onshore area

```python
transport_phase2 = agb.newActivity(USER_DB, 
                                    'transport of components from manufacturing site to onshore site, life cycle phase 2',
                                    unit = 'unit',
                                    exchanges = {
                                        wind_turbines_transport:1,
                                        foundations_transport:1,
                                        intcables_transport:1,
                                        expcables_tranport:1,
                                        offshore_sub_transport:1,
                                    })
```

## Installation on the offshore area

```python
install_phase3 = agb.newActivity(USER_DB, 
                                       'installation on the offshore area, life cycle phase 3',
                                       unit = 'unit',
                                       exchanges = {
                                           wind_turbines_install:1,
                                           #foundations_install:1,
                                           expcables_install:1,
                                           intcables_install:1,
                                           offshore_sub_install:1,
                                       })
```

 ## Operation and maintenance 

```python
maintenance_phase4 = agb.newActivity(USER_DB, 
                                   'operation and maintenance, life cycle phase 4', 
                                   unit = 'unit',
                                   exchanges = {
                                       wind_turbines_maintenance:1,
                                       foundations_maintenance:1,
                                       expcables_maintenance:1,
                                       intcables_maintenance:1,
                                       offshore_sub_maintenance:1,  
                                   })
```

## Decommisioning

```python
decommissioning_phase5 = agb.newActivity(USER_DB, 
                                       'decommissionning, life cycle phase 5',
                                       unit = 'unit',
                                       exchanges = {
                                           wind_turbines_decommissioning:1,
                                           #foundations_decommissioning:1,
                                           intcables_decommissioning:1, 
                                           expcables_decommissioning:1, 
                                           offshore_sub_decommissioning:1,                                       
                                       })
```

## End of life

```python
endoflife_phase6 = agb.newActivity(USER_DB, 
                           'end of life, life cycle phase 6', 
                           unit = 'unit',
                           exchanges = {
                               wind_turbines_endoflife:1,                            
                               foundations_endoflife:1,
                               intcables_endoflife:1,
                               expcables_endoflife:1,
                               offshore_sub_endoflife:1,
                           })
```

 ## Assembly

```python
lca_model_wind_farm = agb.newActivity(USER_DB, 
                                 'complete life cycle assessment model of a wind farm ', 
                                    unit = 'unit',
                                    exchanges = {
                                        manufacturing_phase1:1,
                                        transport_phase2:1,
                                        install_phase3:1,
                                        maintenance_phase4:1,
                                        decommissioning_phase5:1,
                                        endoflife_phase6:1,
                                    })
```

# Life Cycle Impacts Calculation


## Reminder : lca_algebraic parameters and intermediate variables calculated with parameters

```python
# The list of parameters is : 
agb.list_parameters()
```

```python
#All the quantities that are calculated based on parameters are calculated in the table below (with default values of parameters)
agb.intermediate_values_table(globals())
```

## Impact calculations

```python
#Impacts for the whole infrastructure
compute_impacts(
    lca_model_wind_farm,
    impacts_EF_3_0
)
```

```python
#Impacts per MW installed
#We use the function compute_impacts to resize the inventory (division per power_tot_farm_MW)
compute_impacts(
    lca_model_wind_farm,
    impacts_EF_3_0,
    functional_unit=power_tot_farm_MW)
```

```python
#Impacts per kWh of electricity produced
#We use the function compute_impacts to resize the inventory (division per elec_prod_lifetime_kWh)
compute_impacts(
    lca_model_wind_farm,
    impacts_EF_3_0,
    functional_unit=elec_prod_lifetime_kWh)
```

## Climate change impact calculations per life cycle stages

```python
#Impacts for the whole infrastructure
agb.multiLCAAlgebric(
    [lca_model_wind_farm],
    impacts_EF_CO2,
    axis="phase"
)
```

```python
#Impacts per MW installed
compute_impacts(
    lca_model_wind_farm,
    impacts_EF_CO2,
    functional_unit=power_tot_farm_MW,
    axis="phase")
```

```python
#Impacts per kWh of electricity produced
compute_impacts(
    lca_model_wind_farm,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh,
    axis="phase")
```

```python
df=compute_impacts(
    lca_model_wind_farm,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh,
    axis="phase")
```

## Climate change impact calculations per subsystem

```python
#Impacts for the whole infrastructure
agb.multiLCAAlgebric(
    [lca_model_wind_farm],
    impacts_EF_CO2,
    axis="system_1"
)
```

```python
#Impacts per MW installed
compute_impacts(
    lca_model_wind_farm,
    impacts_EF_CO2,
    functional_unit=power_tot_farm_MW,
    axis="system_1")
```

```python
#Impacts per kWh of electricity produced
compute_impacts(
    lca_model_wind_farm,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh,
    axis="system_1")
```

### Climate change impacts per subsystem and per life cycle stages per kWh of electricity produced


#### 1. Manufacturing

```python
compute_impacts(
    manufacturing_phase1,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh,
    axis="system_1")
```

#### 2. Transport

```python
compute_impacts(
    transport_phase2,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh,
    axis="system_1")
```

#### 3. Installation

```python
compute_impacts(
    install_phase3,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh,
    axis="system_1")
```

#### 4. Operation & Maintenance

```python
compute_impacts(
    maintenance_phase4,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh,
    axis="system_1")
```

#### 5. Decommisioning

```python
compute_impacts(
    decommissioning_phase5,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh,
    axis="system_1")
```

#### 6. End of life

```python
compute_impacts(
    endoflife_phase6,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh,
    axis="system_1")
```

## Export of results / excel

```python
parameters=list_parameters_as_df()
```

```python
intermediate_variables_full=agb.intermediate_values_table(globals())
```

```python
intermediate_variables_select=values_table(
    power_tot_farm_MW=(power_tot_farm_MW, "MW"),
    elec_prod_lifetime_kWh=(elec_prod_lifetime_kWh, "kWh"),
    
    rotor_diameter_m=(rotor_diameter_m,"m"),
    mass_tower_tot_kg=(mass_tower_tot_kg,"kg"),
    mass_rotor_tot_kg=(mass_rotor_tot_kg,"kg"),
    mass_nacelle_tot_kg=(mass_nacelle_tot_kg,"kg"),
    
    mass_one_wind_turbine_tot_kg=(mass_one_wind_turbine_tot_kg,"kg"),
    #mass_foundations_gbf_tot_kg=(mass_foundations_gbf_tot_kg,"kg"),
    #mass_foundations_tripod_tot_kg=(mass_foundations_tripod_tot_kg,"kg"),
    mass_foundations_monopile_tot_kg=(mass_foundations_monopile_tot_kg, "kg"),
    #mass_foundations_spar_tot_kg=(mass_foundations_spar_tot_kg, "kg"),
    #mass_foundations_custom_tot_kg=(mass_foundations_custom_tot_kg,"kg"),
    
    mass_wind_turbines_tot_kg=(mass_wind_turbines_tot_kg,"kg"),
    #mass_foundations_gbf_tot_farm_kg=(mass_foundations_gbf_tot_farm_kg,"kg"),
    #mass_foundations_tripod_tot_farm_kg=(mass_foundations_tripod_tot_farm_kg,"kg"),
    mass_foundations_monopile_tot_farm_kg=(mass_foundations_monopile_tot_farm_kg, "kg"),
    #mass_foundations_spar_tot_farm_kg=(mass_foundations_spar_tot_farm_kg, "kg"),
    #mass_foundations_custom_tot_farm_kg=(mass_foundations_custom_tot_farm_kg,"kg"),
    mass_intcables_alu_tot_kg=(mass_intcables_alu_tot_kg,"kg"),
    mass_expcables_tot_kg=(mass_expcables_tot_kg,"kg"),
    mass_offshore_sub_tot_kg=(mass_offshore_sub_tot_kg,"kg"),
    
    wind_turbines_install_fuel_L=(wind_turbines_install_fuel_L,"L"),
    intcables_install_fuel_L=(intcables_install_fuel_L,"L"),
    expcables_install_fuel_L=(expcables_install_fuel_L,"L"),
    offshore_sub_install_fuel_L=(offshore_sub_install_fuel_L,"L"),
    
    wind_turbines_maintenance_fuel_L=(wind_turbines_maintenance_fuel_L,"L"),
    expcables_preventive_maintenance_fuel_L=(expcables_preventive_maintenance_fuel_L,"L"),
    offshore_sub_preventive_maintenance_fuel_L=(offshore_sub_preventive_maintenance_fuel_L,"L"),
    offshore_sub_power_generator_diesel_L=(offshore_sub_power_generator_diesel_L,"L")
)
    
```

```python
impacts_fullsystem_farm=compute_impacts(
        lca_model_wind_farm,
        impacts_EF_3_0)

impacts_fullsystem_farm_phase=compute_impacts(
        lca_model_wind_farm,
        impacts_EF_3_0,
        axis="phase")
    
impacts_fullsystem_farm_systems=compute_impacts(
        lca_model_wind_farm,
        impacts_EF_3_0,
        axis="system_1")
```

```python
impacts_fullsystem_kWh=compute_impacts(
        lca_model_wind_farm,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh)
        
impacts_fullsystem_kWh_phase=compute_impacts(
        lca_model_wind_farm,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh,
        axis="phase")
        
impacts_fullsystem_kWh_systems=compute_impacts(
        lca_model_wind_farm,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh,
        axis="system_1")
```

```python
impacts_manufacturing_kWh=compute_impacts(
        manufacturing_phase1,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh)
    
impacts_manufacturing_kWh_systems=compute_impacts(
        manufacturing_phase1,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh,
        axis="system_1")
```

```python
impacts_installation_kWh=compute_impacts(
        install_phase3,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh)
    
impacts_installation_kWh_systems=compute_impacts(
        install_phase3,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh,
        axis="system_1")
```

```python
#To do : give a name to the excel file. Warning it shall end with .xlsx
xlsx_file_name="export_data.xlsx"

#To do : Define the name of the excel sheet and the table(s) to be exported in this sheet
list_df_to_export=[
    ["parameters",parameters], 
    ["intermediate_variables_full",intermediate_variables_full],
    ["intermediate_variables_select",intermediate_variables_select],
    ["impacts_fullsystem_farm",impacts_fullsystem_farm,impacts_fullsystem_farm_phase,impacts_fullsystem_farm_systems],
    ["impacts_fullsystem_kWh", impacts_fullsystem_kWh,impacts_fullsystem_kWh_phase,impacts_fullsystem_kWh_systems],
    ["impacts_manufacturing_kWh", impacts_manufacturing_kWh,impacts_manufacturing_kWh_systems],
    ["impacts_installation_kWh", impacts_installation_kWh,impacts_installation_kWh_systems],

]

```

```python
export_data_to_excel(list_df_to_export,xlsx_file_name)
```

# Helping section


For the main functions of lca_algebraic, you shall refer to lca_algebraic handbook. 


## Helping section for impacts calculation

All the functionnalities presented in this section work both for the function *agb.multiLCAAlgebraic* and *compute_impacts*, except the **last** sub-section that works only with compute_impacts. 


### How to calculate impacts of an activity ?

```python
agb.multiLCAAlgebric(
                   manufacturing_phase1, #activity to be assessed
                   impacts_EF_CO2,       #list of impact to be calculated
                )
```

### How to calculate the impacts of several activities ?

```python
agb.multiLCAAlgebric([manufacturing_phase1,
                      transport_phase2,
                      install_phase3,
                      maintenance_phase4,
                      decommissioning_phase5,
                      endoflife_phase6],
                   impacts_EF_CO2,  
                )
```

### How to print the impacts of all the life cycle phases or all the subsystem of a system ?

```python
#We can also use the function multiLCAAlgebraic with the "axis" fonction 
agb.multiLCAAlgebric(
                [manufacturing_phase1],
                impacts_EF_CO2,
                axis="system_1"             #specify the axis 
                )
```

```python
#We can also use the function multiLCAAlgebraic with the "axis" fonction 
agb.multiLCAAlgebric(
                [lca_model_wind_farm],
                impacts_EF_CO2,
                axis="phase"             #specify the axis 
                )
```

### How to specify the value of some parameters to calculate the impacts of a specific set of parameters ? 

```python
#We can calculate the total impacts per kWh of electricity produced with some specific values for the parameters (see example below and the list of all parameters below)
#Note : if we don't specify the parameters value, the default values are taken for the calculation

agb.multiLCAAlgebric(
                     lca_model_wind_farm, #model
                     impacts_EF_3_0, #impacts indicators lists   
                     #parameters value
                     turbine_MW = 6,
                     n_turbines = 3,
                     fixed_foundations = 1,
                     d_shore = 50     
                )
```

### How to compare several values of one parameter ?

```python
#To compare impacts for several value of one parameter, you can modify the values chosen for this parameter
#as shown in the example below

agb.multiLCAAlgebric(
    #activity
    lca_model_wind_farm,
    
    #impacts indicators lists
    impacts_EF_3_0, 
    
    #Parameters values
    load_rate=[0.1,0.2,0.4]
    
                )
```

### How to compare several set of values of several parameter ?

```python
#To compare impacts for several value of several parameter, you can modify the values chosen for this parameter
#as shown in the example below
# Warning : all the lists of parameters values must have the same lenght

agb.multiLCAAlgebric(
    #activity
    lca_model_wind_farm,
    
    #impacts indicators lists
    impacts_EF_3_0, 
    
    #Parameters values
    load_rate=[0.1,0.2,0.4],
    n_turbines=[1,2,3],
                )
```

### How to change the functionnal unit ? 

```python
#We use the function compute_impacts to resize the inventory
# Example : Impacts per kWh of electricity produced

compute_impacts(
    lca_model_wind_farm, # activity to be assessed
    impacts_EF_3_0,      # list of 
    functional_unit=elec_prod_lifetime_kWh) # all the impacts are divided per the total electricity produced = elec_prod_lifetime_kWh

```

<!-- #region -->
## Export to excel 


It is possible to export to csv using [df.to_csv](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html) but it is not possible to our knowledge to export several sheets in one file using csv. This is why we did the import in Excel even if it is not an open source software. 
<!-- #endregion -->

### Helping section for export 

```python
# Generate and name the tables you want to export
# Note : tables can be computed with :
# list_parameters_as_df(), agb.intermediate_values_table(globals()), values_table, compute_impacts, agb.multiLCAalgebraic functions
# whose output values are panda dataframes

#Example

df1=values_table(
    resizing_mass_tower=(resizing_mass_tower, " "),
    mass_tower_tot_kg=(mass_tower_tot_kg, "kg"),
    mass_tower_steel_kg=(mass_tower_steel_kg, "kg"),
    mass_tower_alu_kg=(mass_tower_alu_kg, "kg"))

df2=compute_impacts(
    lca_model_wind_farm,
    impacts_EF_CO2,
    functional_unit=elec_prod_lifetime_kWh,
    axis="phase")
```

```python
#To do : give a name to the excel file. Warning it shall end with .xlsx
xlsx_file_name="export_data_test.xlsx"

#To do : Define the name of the excel sheet and the table(s) to be exported in this sheet
list_df_to_export=[
    ["tower mass",df1],     #can be one table 
    ["impact per kWh",df2],
    ["2 or more tables in 1 sheet", df1, df2, df2, df1]    #can be several tables
]

```

```python
#Apply the export function
export_data_to_excel(list_df_to_export,xlsx_file_name)
```

### Customised export of results to excel

```python
parameters=list_parameters_as_df()
```

```python
intermediate_variables_full=agb.intermediate_values_table(globals())
```

```python
intermediate_variables_select=values_table(
    power_tot_farm_MW=(power_tot_farm_MW, "MW"),
    elec_prod_lifetime_kWh=(elec_prod_lifetime_kWh, "kWh"),
    
    rotor_diameter_m=(rotor_diameter_m,"m"),
    mass_tower_tot_kg=(mass_tower_tot_kg,"kg"),
    mass_rotor_tot_kg=(mass_rotor_tot_kg,"kg"),
    mass_nacelle_tot_kg=(mass_nacelle_tot_kg,"kg"),
    
    mass_one_wind_turbine_tot_kg=(mass_one_wind_turbine_tot_kg,"kg"),
    #mass_foundations_gbf_tot_kg=(mass_foundations_gbf_tot_kg,"kg"),
    #mass_foundations_tripod_tot_kg=(mass_foundations_tripod_tot_kg,"kg"),
    mass_foundations_monopile_tot_kg=(mass_foundations_monopile_tot_kg, "kg"),
    #mass_foundations_spar_tot_kg=(mass_foundations_spar_tot_kg, "kg"),
    #mass_foundations_custom_tot_kg=(mass_foundations_custom_tot_kg,"kg"),
    
    mass_wind_turbines_tot_kg=(mass_wind_turbines_tot_kg,"kg"),
    #mass_foundations_gbf_tot_farm_kg=(mass_foundations_gbf_tot_farm_kg,"kg"),
    #mass_foundations_tripod_tot_farm_kg=(mass_foundations_tripod_tot_farm_kg,"kg"),
    mass_foundations_monopile_tot_farm_kg=(mass_foundations_monopile_tot_farm_kg, "kg"),
    #mass_foundations_spar_tot_farm_kg=(mass_foundations_spar_tot_farm_kg, "kg"),
    #mass_foundations_custom_tot_farm_kg=(mass_foundations_custom_tot_farm_kg,"kg"),
    mass_intcables_alu_tot_kg=(mass_intcables_alu_tot_kg,"kg"),
    mass_expcables_tot_kg=(mass_expcables_tot_kg,"kg"),
    mass_offshore_sub_tot_kg=(mass_offshore_sub_tot_kg,"kg"),
    
    wind_turbines_install_fuel_L=(wind_turbines_install_fuel_L,"L"),
    intcables_install_fuel_L=(intcables_install_fuel_L,"L"),
    expcables_install_fuel_L=(expcables_install_fuel_L,"L"),
    offshore_sub_install_fuel_L=(offshore_sub_install_fuel_L,"L"),
    
    wind_turbines_maintenance_fuel_L=(wind_turbines_maintenance_fuel_L,"L"),
    expcables_preventive_maintenance_fuel_L=(expcables_preventive_maintenance_fuel_L,"L"),
    offshore_sub_preventive_maintenance_fuel_L=(offshore_sub_preventive_maintenance_fuel_L,"L"),
    offshore_sub_power_generator_diesel_L=(offshore_sub_power_generator_diesel_L,"L")
)
    
```

```python
impacts_fullsystem_farm=compute_impacts(
        lca_model_wind_farm,
        impacts_EF_3_0)

impacts_fullsystem_farm_phase=compute_impacts(
        lca_model_wind_farm,
        impacts_EF_3_0,
        axis="phase")
    
impacts_fullsystem_farm_systems=compute_impacts(
        lca_model_wind_farm,
        impacts_EF_3_0,
        axis="system_1")
```

```python
impacts_fullsystem_kWh=compute_impacts(
        lca_model_wind_farm,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh)
        
impacts_fullsystem_kWh_phase=compute_impacts(
        lca_model_wind_farm,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh,
        axis="phase")
        
impacts_fullsystem_kWh_systems=compute_impacts(
        lca_model_wind_farm,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh,
        axis="system_1")
```

```python
impacts_manufacturing_kWh=compute_impacts(
        manufacturing_phase1,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh)
    
impacts_manufacturing_kWh_systems=compute_impacts(
        manufacturing_phase1,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh,
        axis="system_1")
```

```python
impacts_installation_kWh=compute_impacts(
        install_phase3,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh)
    
impacts_installation_kWh_systems=compute_impacts(
        install_phase3,
        impacts_EF_CO2,
        functional_unit=elec_prod_lifetime_kWh,
        axis="system_1")
```

```python
#To do : give a name to the excel file. Warning it shall end with .xlsx
xlsx_file_name="export_data.xlsx"

#To do : Define the name of the excel sheet and the table(s) to be exported in this sheet
list_df_to_export=[
    ["parameters",parameters], 
    ["intermediate_variables_full",intermediate_variables_full],
    ["intermediate_variables_select",intermediate_variables_select],
    ["impacts_fullsystem_farm",impacts_fullsystem_farm,impacts_fullsystem_farm_phase,impacts_fullsystem_farm_systems],
    ["impacts_fullsystem_kWh", impacts_fullsystem_kWh,impacts_fullsystem_kWh_phase,impacts_fullsystem_kWh_systems],
    ["impacts_manufacturing_kWh", impacts_manufacturing_kWh,impacts_manufacturing_kWh_systems],
    ["impacts_installation_kWh", impacts_installation_kWh,impacts_installation_kWh_systems],

]

```

```python
export_data_to_excel(list_df_to_export,xlsx_file_name)
```
