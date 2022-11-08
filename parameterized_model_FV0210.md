---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Initialization of the model (import of packages and librairies) 

```python
### %matplotlib inline
from init import *

# Setup new project
initProject('Parameterized_model_OWF_Original')

# Import Ecoinvent DB (if not already done)
# Update the PATH to suit your installation
importDb("ecoinvent", '/var/local/ecoinvent/ecoinvent3.7/datasets')

# We use a separate DB for defining our model, reset it beforehand
USER_DB='lif-owi'

#resetDb(USER_DB)

# Reset the definition of all parameters 
resetParams()
```

# Finding LCIA methods 
To find impacts assessment methods available in Brightway2

```python
bw.methods
```

Variable `ILCD` and `IPCC` to select the **LCIA method** \
Function `findMethods(...)` to find impacts categories available in the selected method. 

```python
ILCD = 'ILCD 2.0 2018 midpoint no LT'

findMethods("terrestrial ecotoxicity",ILCD)
```

# Selection of impacts categories 

```python
climate_bio = (ILCD, 'climate change', 'climate change biogenic')
climate_foss = (ILCD, 'climate change', 'climate change fossil')
climate_land = (ILCD, 'climate change', 'climate change land use and land use change')
climate_tot = (ILCD, 'climate change', 'climate change total')
ecosystem_quality_ecotox= (ILCD,'ecosystem quality','freshwater ecotoxicity')
ecosystem_quality_acid= (ILCD,'ecosystem quality','freshwater and terrestrial acidification')
ecosystem_quality_fresh_eut= (ILCD,'ecosystem quality','freshwater eutrophication')
ecosystem_quality_mar_eut= (ILCD,'ecosystem quality','marine eutrophication')
ecosystem_quality_ter_eut= (ILCD,'ecosystem quality','terrestrial eutrophication')
human_health_io= (ILCD, 'human health', 'ionising radiation')
human_health_oz= (ILCD, 'human health', 'ozone layer depletion')
human_health_pht= (ILCD, 'human health', 'photochemical ozone creation')
human_health_res= (ILCD, 'human health', 'respiratory effects, inorganics')
human_health_noncar= (ILCD, 'human health', 'non-carcinogenic effects')
human_health_car= (ILCD, 'human health', 'carcinogenic effects')
resources_foss = (ILCD, 'resources','fossils')
resources_land = (ILCD, 'resources','land use')
resources_min_met = (ILCD, 'resources','minerals and metals')
resources_water = (ILCD,'resources','dissipated water')

impacts_ILCD = [climate_bio, climate_foss, climate_land, climate_tot, ecosystem_quality_ecotox,ecosystem_quality_acid,
              ecosystem_quality_fresh_eut, ecosystem_quality_mar_eut, ecosystem_quality_ter_eut, human_health_io,
               human_health_oz, human_health_pht, human_health_res, human_health_noncar, human_health_car, resources_foss,
               resources_land, resources_min_met, resources_water]
impacts_ILCD
```

# Manufacture and assembly of components
## Materials and processing 

```python
#materials 
steel_low_alloyed = findTechAct('market for steel, low-alloyed','GLO')
aluminium = findTechAct('market for aluminium, wrought alloy','GLO')
concrete = findTechAct('market group for concrete, normal','GLO')
glass_fibre = findTechAct('market for glass fibre','GLO')
epoxy = findTechAct('market for epoxy resin, liquid','RER')
wood_mix = findTechAct('sawnwood, paraná pine, dried (u=10%), import from BR', 'RER')
polypropylene = findTechAct('market for polypropylene, granulate', 'GLO')
cast_iron = findTechAct('market for cast iron', 'GLO')
chromium_steel = findTechAct('market for steel, chromium steel 18/8', 'GLO')
sand = findTechAct('market for silica sand', 'GLO')
copper = findTechAct('market for copper, cathode', 'GLO')
polyethylene_HD = findTechAct('market for polyethylene, high density, granulate', 'GLO')
steel_electric = findTechAct('steel production, electric, low-alloyed', 'Europe without Switzerland and Austria')
steel_reinforcing = findTechAct('market for reinforcing steel', 'GLO')
lubricating_oil = findTechAct('market for lubricating oil', 'RER')
lead = findTechAct('market for lead', 'GLO')

#Processing 
electricity_UCTE = findTechAct('market group for electricity, medium voltage', 'UCTE')
diesel_process = findTechAct('market for diesel, burned in building machine', 'GLO')
district_heating = findTechAct('heat, non-market, at cogen 160kWe Jakobsberg, allocation exergy', 'CH')
welding_gas = findTechAct('market for welding, gas, steel', 'GLO')
fuel_oil_process = findTechAct('market for heavy fuel oil, burned in refinery furnace', 'GLO')
waste_unspecified = findTechAct('treatment of inert waste, inert material landfill', 'CH')
waste_hazardous = findTechAct ('treatment of hazardous waste, underground deposit', 'DE')
oil_waste = findTechAct ('treatment of waste mineral oil, hazardous waste incineration', 'CH')
water = findTechAct('market for tap water', 'Europe without Switzerland')
natural_gas = findTechAct('market for natural gas, high pressure', 'DE')
heat = findTechAct('heat production, natural gas, at industrial furnace >100kW', 'Europe without Switzerland')

copper_process = findTechAct('wire drawing, copper', 'RER')
steel_process = findTechAct('sheet rolling, steel', 'RER')
steel_weld = findTechAct('welding, arc, steel', 'RER')
zinc_process = findTechAct('zinc coating, coils', 'RER')

#transport
lorry_transp = findTechAct('transport, freight, lorry >32 metric ton, EURO6', 'RER')
rotor_nacelle_transp = findTechAct('transport, freight, lorry 7.5-16 metric ton, EURO5','RER')
container_ship = findTechAct('transport, freight, sea, container ship', 'GLO')
barge_transp = findTechAct('transport, freight, inland waterways, barge', 'RER')

#installation of cables 
excavation = findTechAct('excavation, hydraulic digger','RER')
```


[one leter of diesel = 38,68 MJ = 10,74 kWh = 0.832kg = 0.001m3](https://fr.wikipedia.org/wiki/Discussion:Empreinte_carbone#:~:text=1%20litre%20de%20diesel%20%3D%2038,68%20MJ%20%3D%2010%2C74%20kWh) <br>
[1 kWh of energy = 3.6 MJ](https://www.inchcalculator.com/convert/kilowatt-hour-to-megajoule/) <br>
[steel 507 x 7.92 = 4015 = 4.01 kg/meter](https://www.twi-global.com/technical-knowledge/job-knowledge/calculating-weld-volume-and-weight-095) <br>
[1l of heavy fuel oil = 38.3MJ](https://www.researchgate.net/publication/305438099_Forecasting_port-level_demand_for_LNG_as_a_ship_fuel_the_case_of_the_port_of_Antwerp/figures?lo=1)


## Parameters related 

```python
n_turbines = newFloatParam(
    "n_turbines",
    default=30, min=1, max=100,
    group="wind farm",
    label="number of turbines",
    description="the number of turbines in the wind farm",
    unit="turbines")
```

```python
turbine_MW = newFloatParam(
    "turbine_MW",
    default = 5, min = 2, max = 15,
    group = "wind farm",
    label = "turbine capacity",
    description = " the unit capacity of the wind turbine",
    unit ="MW")
```

```python
load_rate = newFloatParam(
    'load_rate',
    default = 0.4, min = 0, max = 1,
    group = 'wind farm',
    label = 'load factor', 
    description = 'ratio of the total electricity produced against the theoretical one for a year')
```

```python
hub_height = newFloatParam (
    "hub_height",
    default = 120, min = 90, max = 150,
    group = "wind farm",
    label = "hub height",
    description = "the height of the tower",
    unit = "m")
```

```python
steel_ratio_tower = newFloatParam(
    "steel_ratio_tower",
    default = 0.98, min=0, max = 1,
    group = "materials",
    label = "ratio steel in tower",
    description = "the share of steel in the tower")
```

```python
d_onshoresite_land = newFloatParam(
    "d_onshoresite_land",
    default = 200, min = 20, max = 1000,
    group = "Site specific",
    description = "the distance between manufacturing and onshore site by road",
    unit = "km")
```

```python
life_time = newFloatParam(
    'life_time',
    default = 20, min = 20, max = 25,
    group = 'wind farm',
    label = 'life time of wind farm',
    unit = 'years',
    description = "life time of the wind farm")
```

## Recyclable materials activities 

```python
steel_recycled_share = newFloatParam(
    "steel_recycled_share",
    default =0.9, min=0, max=1,
    group = 'Recycling',
    description = 'The share of recycled steel in the wind farm')
```

```python
alu_recycled_share = newFloatParam(
    "alu_recycled_share",
    default =0.9, min=0, max=1,
    group = 'Recycling',
    description = 'The share of recycled aluminium in the wind farm')
```

```python
aluminium_recycled = findTechAct('aluminium scrap, post-consumer, Recycled Content cut-off','GLO')
steel_recycled = copyActivity(
    USER_DB, # user database
    aluminium_recycled, #itial activity 
    "steel scrap, post-consumer, Recycled content cut-off") # New name

steel_mix = newActivity(USER_DB, 
                    "steel mix primary and recycled",
                    unit = 'kg',
                    exchanges = {
                        steel_low_alloyed:1 - steel_recycled_share,
                        steel_recycled:steel_recycled_share,
                    })
aluminium_mix = newActivity (USER_DB,
                        'aluminium mix primary and recycled',
                        unit ='kg',
                        exchanges = {
                            aluminium: 1 - alu_recycled_share,
                            aluminium_recycled: alu_recycled_share,
                        })

```

[the rate of recyclability of concrete is limited to 30%](https://www.archdaily.com/972748/concrete-recycling-is-already-a-reality)

```python
concrete_recycled = copyActivity(
                USER_DB, 
                aluminium_recycled,
                "concrete scrap, recycled content cut-off")

concrete_recycled_share = newFloatParam(
    'concrete_recycled_share',
    default = 0.3, min = 0, max = 0.3,
    group = 'Recycling',
    description = 'The share of concrete in the wind turbine')

concrete_mix = newActivity(USER_DB,
                          'Concrete mix primary and recycled',
                          unit = 'kg',
                          exchanges = {
                              concrete:1 - concrete_recycled_share,
                              concrete_recycled:concrete_recycled_share,
                          })
```

## Tower activity


Density of steel =   8500 kg/m3 <br>
Density of concrete =  2300  kg/m3 <br>
[1 cubic meter of concrete = 2406.53kg](https://www.traditionaloven.com/building/masonry/concrete/convert-cubic-metre-m3-concrete-to-kilogram-kg-of-concrete.html#:~:text=The%20answer%20is%3A%20The%20change,for%20the%20same%20concrete%20type.) <br>
[volume of a truncated hollow cone = height * Pi*(base radius * wall thickness- (wall thickness ²)+ base radius * wall thickness)](https://rechneronline.de/pi/truncated-hollow-cone.php)

```python
tower_act_MW = newActivity(USER_DB,
                       "materials and transport for turbine tower",
                       unit = "unit/MW",
                       exchanges = {
                           steel_mix: steel_ratio_tower*hub_height* (pi/3)*0.343172*8500/turbine_MW,
                           aluminium_mix : 0.02 * hub_height* (pi/3)*0.343172*2710/turbine_MW ,
                           concrete_mix: ((1-steel_ratio_tower-0.02)* hub_height* (pi/3)*0.343172* 2300 /2406.53)/turbine_MW,
                           electricity_UCTE:  22564.1/5,
                           diesel_process: 110.5*38.68/5,
                           district_heating: 4265.3*3.6/5, 
                           welding_gas:22.1/4.01/5,
                           fuel_oil_process: 1790.1*38.3/5,
                           waste_unspecified: 3049.8/5,
                           waste_hazardous: 22.1/5,
                           oil_waste: 4.42/5,
                           lorry_transp:0.001* d_onshoresite_land * hub_height * (pi/3)*0.343172*(8500*steel_ratio_tower+2710*0.02+2300*(1-steel_ratio_tower))/turbine_MW,
                       }) 
printAct(tower_act_MW)

```

## Rotor activity


[Density of wood pine 600,5kg/m3](https://matmatch.com/learn/property/density-of-wood) (Mean value for the range 352-849) <br>
[1 m3 = 10.55 kWh](https://learnmetrics.com/m3-gas-to-kwh/)

```python
rotor_diameter= newFloatParam(
   'rotor_diameter',
    default = 128, min = 39, max = 154,
    group = "wind farm",
    label = "rotor diameter",
    description = "the rotor diameter of the wind turbine",
    unit = "m")   
```

```python
rotor_act_MW = newActivity(USER_DB,
                       "materials and processing for rotor per MW",
                       unit = "unit/MW",
                       exchanges = {
                           glass_fibre:0.0023*((rotor_diameter/2)**2.17)*3/turbine_MW,
                           epoxy:17325/5,
                           wood_mix:(3215.625/600.5)/5, 
                           polypropylene:1246.875/5,
                           water: ( 67462.5+ 25946.875)/5,
                           natural_gas:((22509.375+29687.5)/10.55)/5,
                           electricity_UCTE:(45018.75+ 72081.25)/5,
                           district_heating:12862.5*3.6/5,
                           cast_iron:27371.875/5,
                           chromium_steel: 15971.875/5,
                           steel_mix:14428.125/5,
                           sand:237500/5,
                           lorry_transp:0.001 * d_onshoresite_land * (0.0023*((rotor_diameter/2)**2.17)*3/turbine_MW+406468.75/5) 
                       })
printAct(rotor_act_MW)
```

```python
nacelle_act_MW = newActivity(USER_DB,
                       "materials and processing for the nacelle  per MW",
                       unit = "unit/MW",
                       exchanges = {
                           cast_iron: 130024.44/5, 
                           steel_mix:(124467.84 + 19365.57)/5, 
                           chromium_steel: 7779.24/5,
                           steel_electric :(6945.75 + 7248.15)/5,
                           copper: (5000.94 + 7099.47)/5,
                           aluminium_mix: (3611.79 + 2007.18)/5,
                           electricity_UCTE: 41674.5/5,
                           natural_gas: (229020.833/10.55)/5,
                           polyethylene_HD: 1449.63/5,
                           copper_process: 7099.47/5,
                           steel_process: 26613.72/5,
                           lorry_transp:0.001 * d_onshoresite_land * 445024.44/5,
                       })
printAct(nacelle_act_MW)
```

## Foundations activity


[tsai et al. 2016](https://onlinelibrary.wiley.com/doi/10.1111/jiec.12400)

```python
gravel = findTechAct('market for gravel, crushed', 'CH')
foundations_gbf_MW = newActivity(USER_DB,
                                "materials for gravity based foundations at depth 15m per MW",
                                 unit = "unit/MW",
                                exchanges = {
                                    steel_reinforcing:336000/3,
                                    concrete: 1027/3,
                                    gravel:12200000/3,
                                    lorry_transp: 0.001 * d_onshoresite_land * 15007506.3/3
                                })
```

```python
foundations_monopile_MW = newActivity(USER_DB,
                                      "materials for monopile foundations at depth 20m per MW",
                                      unit = 'unit/MW',
                                      exchanges = {
                                          steel_mix: (276000+169500)/3,
                                          steel_process : 445500/3,
                                          concrete:21.3/3,
                                          lorry_transp: 0.001 * d_onshoresite_land * 942259.089/3
                                      })
```

```python
foundations_tripod_MW = newActivity(USER_DB,
                                   'materials for tripod foundations at depth 50m per MW',
                                   unit = 'unit/MW',
                                   exchanges = {
                                       steel_mix:(807000+847000)/3,
                                       steel_process : 1971630/3,
                                       concrete: (63900/2406.53)/3,
                                       lorry_transp : 0.001 * d_onshoresite_land * 3689530/3
                                   })
```

```python
foundations_floating_MW = newActivity(USER_DB,
                                     'materials for floating foundations per MW',
                                     unit ='unit/MW',
                                     exchanges = {
                                         steel_mix: (1000000+(5000*3))/3,
                                         steel_process: 1000000/3,
                                         gravel: 2500000/3,    
                                         lorry_transp : 0.001 * d_onshoresite_land * 3515000/3
                                     })
```

```python
water_depth = newFloatParam(
    "water_depth",
    default = 20, min = 10, max = 300,
    group="Site specific",
    label="water depth",
    description="water depth of the wind farm site",
    unit="m")
```

```python
fixed_foundations = newBoolParam(
    "fixed_foundations",
    1, # defaut value : fixed-bottom foundations
    group="foundations",
    description="identification of the type of foundations fixed/floating")

floating_foundations = 1 - fixed_foundations
```

to choose the type of fixed foundations depending on the water depth

```python
from sympy import Piecewise 
gbf = Piecewise((1, water_depth <= 15), (0, True))
monop = Piecewise((1, (15 < water_depth) & (water_depth <= 40)), (0, True))
tripod = Piecewise((1, water_depth > 40), (0, True))
```

```python
foundations_act_MW = newActivity (USER_DB,
                                 'foundations activity per MW',
                                 unit = 'unit/MW',
                                 exchanges = {
                                     foundations_gbf_MW:fixed_foundations * gbf,
                                     foundations_monopile_MW:fixed_foundations * monop, 
                                     foundations_tripod_MW: fixed_foundations * tripod,
                                     foundations_floating_MW: floating_foundations,
                                 })
printAct(foundations_act_MW)
tripod
```

## Inter-array cables activity

```python
copper_ratio_intcable = newFloatParam(
    'copper_ratio_intcable',
    default = 0.33, min = 0, max = 1,
    group = 'materials',
    label = 'copper share in interarray cable',
    description = 'the share of copper in the interarray cable')
```

```python
lead_ratio_intcable = newFloatParam(
    'lead_ratio_intcable',
    default = 0.25, min = 0, max=1,
    group = 'materials',
    label = 'lead share in interarray cable',
    description = 'the share of lead in the interarray cable')
```

```python
steel_ratio_intcable = lead_ratio_intcable = newFloatParam(
    'steel_ratio_intcable',
    default = 0.33, min = 0, max=1,
    group = 'materials',
    label = 'steel share in interarray cable',
    description = 'the share of steel in the interarray cable')
```

cable diameter = 27 cm, linear mass = 100kg/linear meter (RTE report)<br>
density of copper = 8960 kg/m3 <br>
density of lead = 11 342 kg/m³ <br>
density of steel = 7850 kg/m³ <br>
density of high density polyethylene = 970 kg/m3 <br>
density of polypropelene = 946 kg/m³

```python
interarray_cables_fixed_act_MW = newActivity( USER_DB,
                       "materials and processing for fixed inter-array cables per MW installed",
                       unit = "unit/MW",
                       exchanges = {
                           steel_mix: steel_ratio_intcable * 7850 * pi *0.135**2 * 8.5 * rotor_diameter * (n_turbines -1)/(n_turbines*turbine_MW),
                           copper: copper_ratio_intcable * 8960 * pi*0.135**2  * 8.5 * rotor_diameter * (n_turbines -1)/(n_turbines*turbine_MW),
                           lead : lead_ratio_intcable * 11342* pi *0.135**2 * 8.5 * rotor_diameter * (n_turbines -1)/(n_turbines*turbine_MW),
                           polyethylene_HD : 0.06 * 970* pi * 8.5 *0.135**2 * rotor_diameter * (n_turbines -1)/(n_turbines*turbine_MW) ,
                           polypropylene : 0.03 * 946 * pi * 8.5 * 0.135**2 * rotor_diameter * (n_turbines -1)/(n_turbines*turbine_MW)  ,
                           zinc_process : 12064.823/27000/5,
                           electricity_UCTE: 1105552.800/27000/5,
                           heat: 7551331.92/27000/5,
                           lorry_transp:d_onshoresite_land*(steel_ratio_intcable * 7850+ copper_ratio_intcable * 8960 + lead_ratio_intcable * 11342 + 86.58)*pi * 0.135**2 * 8.5 * rotor_diameter *0.001*(n_turbines -1)/(n_turbines*turbine_MW),
                       })
printAct(interarray_cables_fixed_act_MW)
```

```python
interarray_cables_floating_act_MW = newActivity( USER_DB,
                       "materials and processing for floating inter-array cables per MW installed",
                       unit = "unit/MW",
                       exchanges = {
                           steel_mix: steel_ratio_intcable * 7850 * pi *0.135**2 * (4* water_depth +8.5 * rotor_diameter) * (n_turbines -1)/(n_turbines*turbine_MW),
                           copper: copper_ratio_intcable * 8960 * pi*0.135**2  * (4* water_depth +8.5 * rotor_diameter)* (n_turbines -1)/(n_turbines*turbine_MW),
                           lead : lead_ratio_intcable * 11342* pi *0.135**2 * (4* water_depth +8.5 * rotor_diameter) * (n_turbines -1)/(n_turbines*turbine_MW),
                           polyethylene_HD : 0.06 * 970* pi *0.135**2 * (4* water_depth +8.5 * rotor_diameter) * (n_turbines -1)/(n_turbines*turbine_MW) ,
                           polypropylene : 0.03 * 946 * pi *0.135**2 * (4* water_depth +8.5 * rotor_diameter) * (n_turbines -1)/(n_turbines*turbine_MW)  ,
                           zinc_process : 12064.823/27000/5,
                           electricity_UCTE: 1105552.800/27000/5,
                           heat: 7551331.92/27000/5,
                           lorry_transp:d_onshoresite_land*(steel_ratio_intcable * 7850+ copper_ratio_intcable * 8960 + lead_ratio_intcable * 11342 + 86.58)*pi * 0.135**2 *(4* water_depth +8.5 * rotor_diameter)*0.001*(n_turbines -1)/(n_turbines*turbine_MW),
                       })
printAct(interarray_cables_floating_act_MW)
```

Configuration Floating/fixed for interarray cables

```python
interarray_cables_act_MW = newActivity (USER_DB, 
                                       "materials and processing for inter-array cables per MW installed",
                                       unit = "unit/MW",
                                       exchanges = {
                                           interarray_cables_fixed_act_MW:fixed_foundations,
                                           interarray_cables_floating_act_MW:floating_foundations,
                                       })
printAct(interarray_cables_act_MW)
```

## Export cables activity

```python
d_shore_substation = newFloatParam(
                'd_shore_substation',
            default = 30000, min = 10000, max = 100000,
            group = 'Site specific', 
            label = 'distance shore substation', 
            description = 'the distance between the shore and substation',
            unit = 'm')
```

```python
alu_ratio_expcable = newFloatParam(
    'alu_ratio_expcable',
    default = 0.13, min = 0, max = 1,
    group = 'materials',
    label = 'aluminium share in export cable',
    description = 'the share of aluminium in the export cable')
```

```python
copper_ratio_expcable = newFloatParam(
    'copper_ratio_expcable',
    default = 0.28, min = 0, max = 1,
    group = 'materials',
    label = 'copper share in export cable',
    description = 'the share of copper in the export cable')
```

```python
lead_ratio_expcable = newFloatParam(
    'lead_ratio_expcable',
    default = 0.28, min = 0, max = 1,
    group = 'materials',
    label = 'lead share in export cable',
    description = 'the share of lead in the export cable')
```

```python
steel_ratio_expcable = newFloatParam(
    'steel_ratio_expcable',
    default = 0.28, min = 0, max = 1,
    group = 'materials',
    label = 'steel share in export cable',
    description = 'the share of steel in the export cable')
```

Density of aluminium = 2710 kg/m3 <br>
Density of glass_fibre = 1.7 kg/m3 

```python
export_cables_alu_MW = newActivity(USER_DB,
                       "materials and processing for export aluminium cables",
                       unit = "unit\MW",
                       exchanges = {
                           aluminium_mix: alu_ratio_expcable * 2710 * pi * 0.135**2 *(d_shore_substation-1000)/(n_turbines*turbine_MW), 
                           steel_mix: steel_ratio_expcable * 7850 * pi * 0.135**2 *(d_shore_substation-1000)/(n_turbines*turbine_MW),
                           lead: lead_ratio_expcable * 11342 * pi * 0.135**2 *(d_shore_substation-1000)/(n_turbines*turbine_MW),
                           polyethylene_HD : 0.21 * 970 * pi * 0.135**2 *(d_shore_substation-1000)/(n_turbines*turbine_MW),
                           polypropylene : 0.09 * 946 * pi * 0.135**2 *(d_shore_substation-1000)/(n_turbines*turbine_MW),
                           glass_fibre:0.01 * 1.7 * pi * 0.135**2 *(d_shore_substation-1000)/(n_turbines*turbine_MW),
                           zinc_process : 198011.742 /43000/5 ,
                           electricity_UCTE: 3596200.940/43000/5,
                           heat : 24563385.360/43000/5,
                           lorry_transp:d_onshoresite_land*(alu_ratio_expcable * 2710+steel_ratio_expcable *7850 + lead_ratio_expcable * 11342 + 288.857)*pi*0.001 * 0.135**2 *(d_shore_substation-1000)/(n_turbines*turbine_MW),
                       })
printAct(export_cables_alu_MW)
```

```python
export_cables_cop_MW = newActivity(USER_DB,
                       "materials and processing for export copper cables",
                       unit = "unit\MW",
                       exchanges = {
                           copper: copper_ratio_expcable * 8960 * pi * 1000 * 0.135**2 /(n_turbines*turbine_MW), 
                           steel_mix: steel_ratio_expcable * 7850 * pi * 1000 * 0.135**2 /(n_turbines*turbine_MW),
                           lead: 0.22 * 11342 * pi *1000 * 0.135**2/(n_turbines*turbine_MW) ,
                           polyethylene_HD : 0.15 * 970 * pi * 1000 *0.135**2 /(n_turbines*turbine_MW),
                           polypropylene : 0.07 * 946 * pi * 1000 *0.135**2 /(n_turbines*turbine_MW),
                           glass_fibre:0.01 * 1.7 * 1000 *pi * 0.135**2 /(n_turbines*turbine_MW),
                           zinc_process : 198011.742 /43000/5 ,
                           electricity_UCTE: 3596200.940/43000/5,
                           heat : 24563385.360/43000/5,
                           lorry_transp:d_onshoresite_land*(copper_ratio_expcable*8960+steel_ratio_expcable *7850 + lead_ratio_expcable 
                                                            * 11342 + 211.737)*0.001*pi *1000 * 0.135**2 /(n_turbines*turbine_MW),
                       })
printAct(export_cables_cop_MW)
```

## Offshore substation


[zinc coating for foundations structure 30*7.14=214.2g/m²](https://itemscatalogue.redcross.int/detail.aspx?productcode=EMEAGAUG01#:~:text=The%20density%20of%20the%20zinc,equivalent%20to%207.14%20g%2Fm2.&text=Example%3A%20zinc%20coating%20thickness%20measured,of%20zinc%20on%20one%20side.)

```python
zinc = findTechAct('market for zinc', 'GLO')
indium = findTechAct('market for indium', 'GLO')
silicon = findTechAct('market for silicon, electronics grade', 'GLO')
cadmium = findTechAct('market for cadmium','GLO')

sacrificial_anode = newActivity(USER_DB,
                            'sacrificial anode for offshore substation structure',
                            unit = 'kg',
                            exchanges = {
                                aluminium_mix: 14099/15000,
                                zinc: 862.5/15000,
                                indium: 3/15000,
                                cast_iron: 9/15000,
                                silicon: 18/15000,
                                copper: 0.45/15000,
                                cadmium: 0.3/15000,                      
                            })

zinc_coat = findTechAct('zinc coating, pieces', 'RER')

offshore_sub_structure = newActivity(USER_DB,
                                    "materials and processing for offshore substation structure",
                                    unit = 'unit\MW',
                                    exchanges = {
                                        steel_mix : (700000 + 875000 + 747000),
                                        gravel : (130000 + 3000000),
                                        zinc_coat: (22000*0.85*100/214.2),
                                        sacrificial_anode : 15000, 
                                    })
printAct(offshore_sub_structure)
```

```python
paper_printed = findTechAct('market for printed paper', 'GLO')
wood_board = findTechAct('market for three and five layered board', 'RER')

TSA_1MVA = newActivity(USER_DB,
                      'TSA, 1MVA 66/0.4kv',
                      unit= 'kg',
                      exchanges = {
                          steel_mix : (2600+2200)/10250,
                          copper: 1450/10250,
                          paper_printed : 1000*0.5/10250,
                          wood_board :  1000*0.5/600/10250, #density = 600kg/m3
                          lubricating_oil: 2000/10250,
                          epoxy: 100/10250,
                      }) 

sulfuric_acid = findTechAct('market for sulfuric acid','RER')
phosphoric_acid = findTechAct('market for phosphoric acid, industrial grade, without water, in 85% solution state', 'GLO')
tin = findTechAct('market for tin', 'GLO')
antimony = findTechAct('market for antimony', 'GLO')

batteries = newActivity(USER_DB,
                       'Batteries 15, 20 and 50kw, 8h, 48, 127 and 400 VDC',
                       unit = 'kg',
                       exchanges = {
                           lead: (5797+5478)/16600,
                           water: 2482/16600, 
                           polypropylene: 1328/16600,
                           sulfuric_acid: 1222/16600, 
                           phosphoric_acid: 115/16600,
                           tin: 90/16600, 
                           antimony: 90/16600, 
                       })
steel_unalloyed = findTechAct('market for steel, unalloyed', 'GLO')

cooling_radiators = newActivity(USER_DB, 
                          'cooling radiators, elevating transformer',
                          unit = 'kg',
                          exchanges = {
                              steel_unalloyed: 50000/60000,
                              lubricating_oil: 10000/60000,
                          })

transformers_330MVA = newActivity(USER_DB, 
                                 'transformers 330MVA-225-66kv',
                                 unit= 'kg',
                                 exchanges = {
                                     steel_mix: 130000/275000,
                                     copper: 30000/275000, 
                                     paper_printed: 15000*0.5/275000,
                                     wood_board:15000*0.5/275000,
                                     lubricating_oil: 100000/275000,
                                     electricity_UCTE: 154110/275000,
                                     district_heating: 655944*3.6/275000,   
                                 })

sf_6 = findTechAct('market for sulfur hexafluoride, liquid','RER')

psem_cells_225kv = newActivity(USER_DB,
                        'PSEM cells 225kv',
                        unit = 'kg',
                        exchanges = {
                            aluminium_mix:3440/5580,
                            steel_mix: 1380/5580,
                            chromium_steel: 240/5580,
                            epoxy: 150/5580,
                            sf_6: 150/5580,
                            copper: 90/5580,
                            polyethylene_HD: 80/5580,
                        })

pet = findTechAct('market for polyethylene terephthalate, granulate, amorphous', 'GLO')
synthetic_rubber = findTechAct('market for synthetic rubber', 'GLO')
tetrafluoroethylene = findTechAct('market for tetrafluoroethylene', 'GLO')
nylon_6 = findTechAct('market for nylon 6-6, glass-filled', 'RER')
zeolite = findTechAct('market for zeolite, powder', 'GLO')
pmma = findTechAct('market for polymethyl methacrylate, sheet')

psem_cells_66kv = newActivity(USER_DB,
                             'PSEM cells 66kv',
                             unit = 'kg',
                             exchanges = {
                                 aluminium_mix: 1893/3062,
                                 steel_mix: 645/3062,
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

electric_components = newActivity(USER_DB, 
                                 'electric components materials',
                                 unit = 'unit', 
                                 exchanges = {
                                     TSA_1MVA: 41000,
                                     batteries: 33000,
                                     cooling_radiators: 120000,
                                     psem_cells_225kv:11000,
                                     psem_cells_66kv:61000,
                                     transformers_330MVA: 5500,
                                 })
```

```python
manipulate_equip = newActivity(USER_DB,
                              'manipulation equipment',
                              unit = 'kg',
                              exchanges = {
                                  steel_mix: 1,
                              })
```

```python
alkyd = findTechAct('market for alkyd paint, white, without solvent, in 60% solution state', 'RER')
brass = findTechAct('market for brass', 'CH')
brazing = findTechAct('market for brazing solder, cadmium free', 'GLO')
linerboard = findTechAct('market for containerboard, linerboard', 'RER')
stone_wool = findTechAct('market for stone wool', 'GLO')
co_2 = findTechAct('market for carbon dioxide, liquid', 'RER')

diesel_generator_1000 = newActivity(USER_DB,
                              'diesel generator 100kVA',
                                   unit = "kg",
                                   exchanges = {
                                       alkyd: 25/5791,
                                       aluminium_mix: 150/5791,
                                       brass: 0.5/5791,
                                       brazing:60/5791,
                                       copper: 250/5791,
                                       linerboard: 1.16/5791,
                                       polyethylene_HD: 14/5791,
                                       steel_mix: (250+4850)/5791,
                                       stone_wool: 190/5791,
                                   })
control_instrumentation = newActivity(USER_DB,
                                     'control instrumentation',
                                     unit = "unit",
                                      exchanges = {
                                          diesel_generator_1000: 6000,
                                          water: 8000+60000,
                                          co_2: 100,                                         
                                      })
```

```python
concrete_found = findTechAct('market for concrete, sole plate and foundation', 'CH')

tank_sump = newActivity(USER_DB,
                       'sump tank drum and pump',
                       unit = 'kg',
                       exchanges = {
                           alkyd: 47/3830,
                           brass: 11/3830,
                           cast_iron: 47/3830,
                           concrete_found: (2/3830)/2406.53,
                           copper: 158/3830,
                           polyethylene_HD: 4/3830,
                           steel_mix: 3560/3830,
                       })

diesel_tank = copyActivity(USER_DB,
    tank_sump, #itial activity 
    "diesel tank 3000L")

security_scrap_equipment = newActivity(USER_DB,
                                      'equipment water-scrap-safety',
                                      unit = 'unit',
                                      exchanges = {
                                          tank_sump:8000,
                                          diesel_tank:12000,
                                      })
```

```python
electric_comp = findTechAct('market for printed wiring board, surface mounted, unspecified, Pb free','GLO')

dc_board = newActivity(USER_DB,
                      'Direct Current DC boards',
                      unit = 'kg',
                      exchanges = {
                          steel_mix:180/300,
                          electric_comp:120/300,                         
                      })

telecom_board = copyActivity(USER_DB,
                            dc_board,
                            'telecom boards')
telecom_board.updateExchanges({
    'steel mix primary and recycled':120/200,
    'market for printed wiring board, surface mounted, unspecified, Pb free#GLO':80/200,})
count_board = copyActivity(USER_DB,
                            dc_board,
                            'counting boards')
count_board.updateExchanges({
    'steel mix primary and recycled':240/400,
    'market for printed wiring board, surface mounted, unspecified, Pb free#GLO':160/400,})

supervision_board = copyActivity(USER_DB,
                            telecom_board,
                            'supervision boards')

command_control = newActivity(USER_DB,
                             'Telecom and control command',
                             unit = 'unit',
                             exchanges = {
                                 dc_board:11000,
                                 telecom_board:1000,
                                 count_board:1000,
                                 supervision_board:1000,
                             })
```

```python
polystyrene= findTechAct('market for polystyrene, general purpose','GLO')
refrigerant = findTechAct('market for refrigerant R134a','GLO')

HVAC_cooling = newActivity(USER_DB,
                          'cooling for HVAC equipments',
                          unit = 'kg',
                          exchanges = {
                              steel_mix: 185/430,
                              copper: 123/430,
                              aluminium_mix: 18/430,
                              brass: 3/430,
                              polyethylene_HD: 15/430,
                              polypropylene: 9/430,
                              polystyrene: 1/430,
                              wood_board: 42/430,
                              refrigerant: 17/430,
                              linerboard: 7/430,
                              electric_comp: 4/430,
                          })
```

```python
offshore_sub_act = newActivity(USER_DB,
                       "materials and processing for offshore substation",
                       unit = "unit",
                       exchanges = {
                           offshore_sub_structure:1,
                           electric_components:1,
                           manipulate_equip:1,
                           control_instrumentation:1,
                           security_scrap_equipment:1,
                           command_control:1,
                           HVAC_cooling:1, })
```

```python
offshore_sub_act_MW = newActivity(USER_DB,
                                 'materials and processing for offshore substation per MW',
                                 unit = 'unit\MW',
                                 exchanges = {
                                     offshore_sub_act:1/600, #LCA study is performed for a 600MW offshore substation
                                 })
```

# Transportation to the onshore area and installation


## Foundations 

```python
diesel_consumption = findTechAct('market for diesel, burned in fishing vessel','GLO')
hfo_consumption = findTechAct('market for heavy fuel oil', 'Europe without Switzerland')
```

```python
foundations_gbf_install_MW = newActivity(USER_DB,
                                     'Installation and transport for gravity based foundations per MW',
                                     unit = 'unit\MW',
                                     exchanges = {
                                         gravel: (1668970 + 1794480)/3,
                                         diesel_consumption: (846.65+43700.8+580.63+846.65)*38.68/3,
                                         hfo_consumption:(7200+32.76+846.65+7200+4080+7200)*0.983/3,
                                     })
```

```python
foundations_monop_install_MW = newActivity(USER_DB, 
                                          'Installation and transport for monopile foundations at depth 20m per MW',
                                          unit = 'unit\MW', 
                                          exchanges = {
                                              gravel:687510/3,
                                              diesel_consumption: (3311.93+513.32)*38.68/3,
                                              hfo_consumption: (2400+4440+1161.27+4080+2911.8)*0.983/3,
                                          })
```

```python
foundations_tripod_install_MW = newActivity(USER_DB,
                                           'installation and transport for tripod foundations at depth 50m per MW',
                                           unit = 'unit\MW',
                                           exchanges = {
                                               diesel_consumption:9935.8*38.68/3,
                                               hfo_consumption:(13320 + 1161.27 + 4080)*0.983/3
                                           })
```

```python
foundations_floating_install_MW = newActivity(USER_DB, 
                                             'installation and transport for floating foundations per MW',
                                             unit = 'unit\MW',
                                             exchanges = {
                                                 diesel_consumption: 16559.67*38.68/3,
                                                 hfo_consumption: (1161.27 + 8160)*0.983/3,
                                             })
```

```python
foundations_install_act_MW = newActivity (USER_DB,
                                 'foundations install activity per MW',
                                 unit = 'unit/MW',
                                 exchanges = {
                                     foundations_gbf_install_MW:fixed_foundations * gbf,
                                     foundations_monop_install_MW:fixed_foundations * monop, 
                                     foundations_tripod_install_MW: fixed_foundations * tripod,
                                     foundations_floating_install_MW: floating_foundations,
                                 })
```

## Offshore substation

```python
#Transportation 

transformers_transport = findTechAct('transport, freight, sea, container ship', 'GLO')
equip_transport = findTechAct('transport, freight, lorry 16-32 metric ton, EURO6','RER')
topside_transport_fuel = findTechAct('diesel, burned in fishing vessel', 'GLO')

#welding
welding = findTechAct('market for welding, gas, steel', 'GLO')

offshoresub_transport = newActivity(USER_DB,
                       "Offshore substation transport to the onshore area",
                       unit = "unit",
                       exchanges = {transformers_transport : 550000,
                                    equip_transport : 2193431,
                                    topside_transport_fuel :2* 150* 1000*38.68,})  
```

```python
offshoresub_install = newActivity(USER_DB, 
                             'topside installation fuel consumption',
                             unit='unit',
                                 exchanges = {
                                     topside_transport_fuel: 3 * (32000 + 41650) + 30 * 1666 + (0.5/24)*83.3* 45
                                 })
# (320000 + 41650) Fuel consumption for lifting per day
# 1666 Fuel consumption of the Autoelevation platform for commissioning
# 83.3 fuel consumption for the crew transfer vessel

offshoresub_install_model = newActivity (USER_DB, 
                                        'offshore substation transport and installation model',
                                        unit = 'unit', 
                                        exchanges = {
                                            offshoresub_transport:1,
                                            welding: 60,
                                            offshoresub_install:1,
                                        })
```

```python
offshoresub_install_MW = newActivity(USER_DB,
                                    'offshore substation transport and installation model per MW',
                                    unit = 'unit/MW',
                                    exchanges = {
                                        offshoresub_install_model:1/600,
                                    })
```

## Moving parts assembly

```python
d_shore = newFloatParam(
                     "d_shore",
    default =12.3, min=5, max=100,
    group = 'Site specific',
    description = 'The distance to shore')
```

Fuel consumption: RTE report average value 

```python

bunnyear_assembly_MW= newActivity(USER_DB,
                       "Moving parts bunny ear assembly per MW",
                       unit = "unit/MW",
                       exchanges = {
                           water: 49906.34/5,
                           natural_gas : (17197.455/10.55)/5,
                           electricity_UCTE : 22*(22929.94/24)/5,
                           district_heating : (50580.75*3.6)/5, 
                           rotor_nacelle_transp: d_onshoresite_land * (125+315)/5,
                           container_ship: d_shore * (125+315+221)/5,  
                           diesel_consumption: 4/2 * (32000+4650)* 5.1* (38.68/0.832)/600, # 4 is the number of lifts 5.1 installation days
                       })
```

```python
rotorstar_assembly_MW= newActivity(USER_DB,
                       "Moving parts rotorstar assembly per MW",
                       unit = "unit/MW",
                       exchanges = {
                           water: 49906.34/5,
                           natural_gas : (17197.455/10.55)/5,
                           electricity_UCTE : 16*(22929.94/24)/5,
                           district_heating : (50580.75*3.6)/5, 
                           rotor_nacelle_transp: d_onshoresite_land * (125+315)/5,
                           container_ship: 2*d_shore * (125+315+221)/5,  
                           diesel_consumption: 4 * (32000+4650)*7.1 * (38.68/0.832)/600, # 4 is the number of lifts
                       })
```

```python
seperateparts_assembly_MW= newActivity(USER_DB,
                       "Moving parts seperate parts assembly per MW",
                       unit = "unit/MW",
                       exchanges = {
                           water: 49906.34/5,
                           natural_gas : (17197.455/10.55)/5,
                           electricity_UCTE : 6*(22929.94/24)/5,
                           district_heating : (50580.75*3.6)/5, 
                           rotor_nacelle_transp: d_onshoresite_land * (125+315)/5,
                           container_ship: 2/3*d_shore * (125+315+221)/5,  
                           diesel_consumption: 6/3 * (32000+4650)*1.9 * (38.68/0.832)/600, 
                       })
```

### Installation of cables

```python
gravel_riprap = findTechAct('market for gravel, round', 'CH')

d_riprap = newFloatParam(
    'd_riprap',
    default = 1, min = 1, max = 100,
    unit = 'km',
    group = 'Site specific',
    label = 'distance related to cables being embedded',
    description = 'distance related to cables being embedded')
```

```python
riprap_activity_expcables_MW = newActivity(USER_DB, 
                                       'Rip rap of the export cables posing per MW',
                                       unit='unit\MW',
                                       exchanges ={
                                           gravel_riprap: 20000000 * d_riprap/600, 
                                           excavation : 51.06/600,
                                       })
```

```python
posing_expcables_MW = newActivity (USER_DB, 
                               'fuel consumption for export cables posing per MW', 
                               unit = 'unit\MW', 
                               exchanges = {
                                   diesel_consumption: (42.6*10+28.4*200)*38.68/600,
                                   hfo_consumption: (5000*80+2000*10+13400*45+16000*10+23800*2+20000*10+5000*10)*0.983/600,
                               })

```

## Inter-array cables

```python
posing_interarraycables_fixed_MW = newActivity (USER_DB, 
                                             'fuel consumption for fixed inter-array cables posing per MW',
                                             unit='unit\MW', 
                                             exchanges = {
                                                 posing_expcables_MW:(1/30)*(8.5*rotor_diameter*(n_turbines - 1)),
                                             })
posing_interarraycables_floating_MW = newActivity (USER_DB, 
                                                'fuel consumption for floating inter-array cables posing per MW',
                                                unit='unit\MW',
                                                exchanges = {
                                                    posing_expcables_MW:(1/30)*(4*water_depth + 8.5*rotor_diameter*(n_turbines - 1)),
                                                })
posing_interraycables_act_MW= newActivity(USER_DB, 
                                           'Fuel consumption for the interray cables posing per MW',
                                           unit = 'unit\MW',
                                           exchanges = {
                                               posing_interarraycables_fixed_MW:fixed_foundations,
                                               posing_interarraycables_floating_MW:floating_foundations,
                                           })
```

# Operation and maintenance


## Wind turbines

```python
turbines_maintenance_act_MW = newActivity(USER_DB,
                                         'maintenance activity for turbines per MW',
                                         unit = 'unit\MW',
                                         exchanges = {
                                             lubricating_oil : 15.8/5,
                                             oil_waste:15.8/5,
                                             barge_transp: d_shore * 500 *0.001*31*2/5,
                                                })
```

## export cables 

```python
life_time_cables = newFloatParam(
    'life_time_cables',
    default = 40, min = 20, max = 40,
    group = 'wind farm',
    label = 'life time of the export cables',
    unit = 'years',
    description = "life time of the export cables")
```

```python
maintenance_expcables_MW = newActivity(USER_DB, 
                                   'preventive and corrective maintenance of the export cables per MW',
                                   unit = 'unit\MW',
                                   exchanges = {
                                       hfo_consumption: (20*13400*0.983 * ((life_time_cables/10)-1)) + 2*(60*5000+20*13400+2*10)*0.983/600 ,
                                       diesel_consumption: 60*28.4*38.68/600
                                   })
```

# Interarray cables

```python
maintenance_interarraycables_fixed_MW = newActivity(USER_DB,
                                          'Preventive and corrective maintenance of the interarray cables for fixed wind farm per MW',
                                          unit = 'unit\MW', 
                                          exchanges = {
                                              maintenance_expcables_MW: (1/30)*(8.5*rotor_diameter*(n_turbines - 1)),
                                          })
maintenance_interarraycables_floating_MW = newActivity(USER_DB, 
                                        'Preventive and corrective maintenance of the interray cables for floating wind farm per MW',
                                          unit = 'unit\MW',
                                            exchanges = {
                                                maintenance_expcables_MW: (1/30)*(4*water_depth + 8.5*rotor_diameter*(n_turbines - 1))
                                            })
maintenance_interraycables_act_MW= newActivity(USER_DB, 
                                           'Preventive and corrective maintenance of the interray cables per MW',
                                           unit = 'unit\MW',
                                           exchanges = {
                                               maintenance_interarraycables_fixed_MW:fixed_foundations,
                                               maintenance_interarraycables_floating_MW:floating_foundations,
                                           })
```

## Offshore substation 

```python
life_time_substation = newFloatParam(
    'life_time_substation',
    default = 25, min = 20, max = 30,
    group = 'wind farm',
    label = 'life time of the offshore substation',
    unit = 'years',
    description = 'life time of the offshore substation')
```

```python
emission_ratio_anode = newFloatParam(
    'emission_ratio_anode',
    default = 0.0196, min = 0, max = 100,
    group = 'offshore substation',
    label = 'sacrificial anode degradation emission ratio', 
    description = 'sacrificial anode degradation emission ratio')
```

```python
diesel_maintenance = findTechAct('market for diesel, burned in diesel-electric generating set, 10MW', 'GLO')

sacrificial_anode_deg = newActivity(USER_DB, 
                    'Sacrificial anode degradation during use', 
                                   unit = 'unit',
                                       exchanges = {
                                           sacrificial_anode: 1 * emission_ratio_anode,
                                       })
substation_maintenance = newActivity(USER_DB, 
                                    'fuel consumption during maintenance activities',
                                    unit = 'unit',
                                     exchanges = {
                                         diesel_maintenance: 38.68 * (2000 * life_time_substation/15) + 100 * 24 * 5 * 4 * life_time_substation + 35000,
                                         HVAC_cooling:1,
                                         sf_6: 58 + 53,
                                         electricity_UCTE: 82455 + 164910 * 1000,
                                         sacrificial_anode_deg: 1, 
                                     })
substation_maintenance_MW = newActivity(USER_DB,
                                       'fuel consumption during maintenance activities per MW',
                                       unit = 'unit\MW',
                                       exchanges = {
                                           substation_maintenance : 1/600,
                                       })

```

 # Decommissioning

```python
d_offshoresite_eol = newFloatParam(
    "d_offshoresite_eol",
    default = 500, min = 20, max = 1000,
    group = "Site specific",
    description = "the distance between the offshore site and the waste treatment center by road",
    unit = "km")
```

## Wind turbines

```python
decommissioning_turbines_MW = newActivity(USER_DB,
                                         'Decommissioning of wind turbines per MW',
                                         unit = 'unit\MW',
                                         exchanges = {
                                             lorry_transp:0,
                                             diesel_consumption:0,
                                             hfo_consumption:0,
                                         })
```

## Foundations

```python
decommissioning_gbf_foundations_MW = newActivity(USER_DB, 
                                                'Decommissioning of gravity based foundations at depth 15m per MW',
                                                unit = 'unit\MW',
                                                exchanges = {
                                                    lorry_transp: d_offshoresite_eol * 0.001 * 15007506.3/3,
                                                    diesel_consumption: (580.63+43700.8)* 38.68/3,
                                                    hfo_consumption:4080 * 0.983/3,
                                                })
```

```python
decommissioning_monop_foundations_MW = newActivity(USER_DB, 
                                                  'Decommissioning of monopile foundations at depth 20m per MW',
                                                  unit = 'unit\MW',
                                                  exchanges = {
                                                      lorry_transp:d_offshoresite_eol * 0.001 * 942259.089/3,
                                                      diesel_consumption: 3311.93 * 38.68/3,
                                                      hfo_consumption: (2400+4440+1161.27 + 4080)*0.983/3,
                                                  })
```

```python
decommissioning_tripod_foundations_MW = newActivity(USER_DB, 
                                       'Decommissioning of tripod foundations at depth 50m per MW',
                                       unit = 'unit/MW',
                                       exchanges = {
                                           lorry_transp:d_offshoresite_eol * 0.001 * 3689530/3,
                                           diesel_consumption: 16903.4*38.683/3,
                                           hfo_consumption:(2400 + 13320+3483.8+4080)*0.983/3,
                                           
                                       })
```

```python
decommissioning_floating_foundations_MW = newActivity(USER_DB, 
                                                     'Decommissioning of floating foundations per MW', 
                                                     unit = 'unit/MW',
                                                     exchanges = {
                                                         lorry_transp: d_offshoresite_eol * 0.001 * 3515000/3,
                                                         diesel_consumption: 13247.74 * 38.68/3,
                                                         hfo_consumption: (1161.27 + 8160) * 0.983/3,
                                                     })
```

```python
decommissioning_foundations_act_MW = newActivity (USER_DB,
                                 'decommissioning of foundations activity per MW',
                                 unit = 'unit/MW',
                                 exchanges = {
                                     decommissioning_gbf_foundations_MW:fixed_foundations * gbf,
                                     decommissioning_monop_foundations_MW:fixed_foundations * monop, 
                                     decommissioning_tripod_foundations_MW: fixed_foundations * tripod,
                                     decommissioning_floating_foundations_MW: floating_foundations,
                                 })
```

 ## Export cables 

```python
decommissioning_expcables_MW = copyActivity(
   USER_DB, # user database
  posing_expcables_MW, # initial activity 
   "Fuel consumption of export cables decommissioning per MW") # New name 
    
decommissioning_expcables_MW.updateExchanges({
    'market for diesel, burned in fishing vessel#GLO':(42.6*9.67+28.4*193)*38.68/600,
    'market for heavy fuel oil#Europe without Switzerland':(5000*77.33+23800*0.15+13400*24.2+16000*9.67)*0.983/600,
})
```

## Inter-array cables

```python
decommissioning_interarraycables_fixed_MW = newActivity(USER_DB, 
                                        'fuel consumption of fixed inter-array cables decommissioning per MW',
                                        unit = 'unit\MW', 
                                        exchanges = {
                                            decommissioning_expcables_MW:(1/29)*(8.5*rotor_diameter*(n_turbines - 1)),
                                        })
decommissioning_interarraycables_floating_MW = newActivity(USER_DB,
                                        'fuel consumption of floating inter-array cables decommissioning per MW',
                                        unit = 'unit\MW', 
                                        exchanges = {
                                            decommissioning_expcables_MW:(1/29)*(4*water_depth + 8.5*rotor_diameter*(n_turbines - 1)),
                                        })
decommissioning_interarraycables_act_MW = newActivity(USER_DB,
                                                  'fuel consumption of inter-array cables decommissioning per MW',
                                                  unit = 'unit\MW', 
                                                  exchanges = {
                                                      decommissioning_interarraycables_fixed_MW:fixed_foundations,
                                                      decommissioning_interarraycables_floating_MW:floating_foundations,
                                                  })
```


 ## Offshore substation

```python
kerosene = findTechAct("market for kerosene", 'Europe without Switzerland')

offshore_substation_decom = newActivity(USER_DB, 
                                       'Offshore substation decommissioning activity',
                                       unit = 'unit', 
                                       Exchanges = {
                                           kerosene: (16*3893 + 24 * 32000)/24,
                                           topside_transport_fuel: 2.5* ((32000 + 41650+ 3893)* 38.68/0.832),        
                                       })
offshore_substation_decom_MW = newActivity(USER_DB, 
                                       'offshore substation decommissioning activity per MW',
                                           unit = 'unit\MW',
                                          exchanges = {
                                              offshore_substation_decom:1/600,
                                          })
```

# End-of-life


## Wind turbines
### Tower 

```python
alu_landfill_share = newFloatParam(
    "alu_landfill_share",
    default =0.05, min=0, max=1,
    group = 'Landfill',
    description = 'The share of landfilling aluminium waste in the wind farm')

alu_incineration_share = 1- alu_recycled_share -alu_landfill_share
```

```python
landfill_steel = findTechAct('treatment of scrap steel, inert material landfill','CH')
landfill_aluminium = findTechAct('treatment of waste aluminium, sanitary landfill','CH')
landfill_concrete = findTechAct('treatment of waste concrete, inert material landfill', 'CH')
incineration_aluminium = findTechAct('treatment of aluminium in car shredder residue, municipal incineration','CH')
recycling_aluminium = findTechAct('treatment of aluminium scrap, post-consumer, prepared for recycling, at remelter','RER')
recycling_steel = findTechAct('treatment of waste reinforcement steel, recycling', 'CH')
recycling_concrete = findTechAct('treatment of waste concrete, not reinforced, recycling', 'CH')

tower_eol_MW = newActivity (USER_DB, 
                           'end of life treatment of tower per MW',
                           unit= 'unit\MW',
                           exchanges = {
landfill_steel: (1-steel_recycled_share)* steel_ratio_tower*hub_height* (pi/3)*0.343172*8500/turbine_MW,
landfill_aluminium:alu_landfill_share*0.02 * hub_height* (pi/3)*0.343172*2710/turbine_MW,
landfill_concrete: (1-concrete_recycled_share)*(1-steel_ratio_tower-0.02)* hub_height* (pi/3)*0.343172* 2300/turbine_MW,
incineration_aluminium:alu_incineration_share*0.02 * hub_height* (pi/3)*0.343172*2710/turbine_MW,
recycling_aluminium:alu_recycled_share*0.02 * hub_height* (pi/3)*0.343172*2710/turbine_MW,
recycling_steel: steel_recycled_share*steel_ratio_tower*hub_height* (pi/3)*0.343172*8500/turbine_MW,
recycling_concrete: concrete_recycled_share*(1-steel_ratio_tower-0.02)* hub_height* (pi/3)*0.343172* 2300/turbine_MW,
                           })
```

### Rotor 

```python
landfill_glassfibre = findTechAct('treatment of waste glass, inert material landfill','CH')
landfill_epoxy = findTechAct('treatment of waste plastic, mixture, sanitary landfill', 'CH')
incineration_plastic = findTechAct('treatment of waste plastic, industrial electronics, municipal incineration','CH')

rotor_eol_MW = newActivity(USER_DB,
                          'End of life treatment of rotor per MW',
                          unit = 'unit/MW',
                          exchanges = {
                              landfill_glassfibre:0.0023*((rotor_diameter/2)**2.17)*3/turbine_MW,
                              landfill_epoxy:17325/5,
                              incineration_plastic:1246.875/5,
                              landfill_steel:(1-steel_recycled_share)* (14428.125+ 27371.875 +15971.875) /5,
                              recycling_steel: steel_recycled_share * (14428.125+ 27371.875 +15971.875) /5,          
                          })
```

### Nacelle 

```python
incineration_copper = findTechAct('treatment of copper in car shredder residue, municipal incineration','CH')

nacelle_eol_MW = newActivity(USER_DB, 
                            'end of life treatment of nacelle per MW',
                            unit = 'unit/MW',
                            exchanges = {
                                landfill_steel:(1-steel_recycled_share)*(124467.84 + 19365.57 + 7779.24+6945.75 + 7248.15)/5, 
                                recycling_steel: steel_recycled_share *(124467.84 + 19365.57 + 7779.24+6945.75 + 7248.15)/5,
                                incineration_copper: (5000.94 + 7099.47)/5,
                                incineration_aluminium:alu_incineration_share*(3611.79 + 2007.18)/5,
                                landfill_aluminium:alu_landfill_share*(3611.79 + 2007.18)/5,
                                recycling_aluminium:alu_recycled_share*(3611.79 + 2007.18)/5,
                                incineration_plastic:1449.63/5,         
                            })
```

## Offshore substation

```python
landfill_silicon = findTechAct('treatment of waste, from silicon wafer production, inorganic, residual material landfill', 'CH')
landfill_zinc = findTechAct('treatment of zinc slag, residual material landfill', 'GLO')
landfill_inert = findTechAct('treatment of inert waste, sanitary landfill', 'Europe without Switzerland')
landfill_polyethylene = findTechAct('treatment of waste polyethylene, sanitary landfill', 'CH')
landfill_rubber = findTechAct('market for waste rubber, unspecified','CH')
landfill_PTFE = findTechAct('treatment of waste polyvinylchloride, sanitary landfill', 'CH')
landfill_polystyrene = findTechAct('treatment of waste polystyrene, sanitary landfill', 'CH')
landfill_hazard_waste = findTechAct('treatment of hazardous waste, underground deposit', 'RoW')
landfill_paperboard = findTechAct('treatment of waste paperboard, sanitary landfill', 'RoW')
landfill_zeolite = findTechAct('treatment of waste zeolite, inert material landfill', 'CH')
```

```python
sacrificial_anode_eol = newActivity(USER_DB,
                            'end of life treatment for sacrificial anode_offshore substation structure',
                            unit = 'kg',
                            exchanges = {
                                landfill_aluminium: alu_landfill_share*14099/15000,
                                incineration_aluminium:alu_incineration_share*14099/15000,
                                recycling_aluminium:alu_recycled_share*14099/15000,  
                                landfill_zinc: 862.5/15000,
                                landfill_inert: (3+0.3)/15000,
                                landfill_steel: 9/15000,
                                landfill_silicon: 18/15000,
                                incineration_copper: 0.45/15000,                     
                            })
offshore_sub_structure_eol_MW = newActivity(USER_DB,
                                    "end of life treatment for offshore substation structure",
                                    unit = 'unit\MW',
                                    exchanges = {
                                        landfill_steel :(1-steel_recycled_share)* (700000 + 875000 + 747000)/600,
                                        recycling_steel: steel_recycled_share*(700000 + 875000 + 747000)/600,
                                        landfill_zinc: (22000*0.85*100/214.2)/600,
                                        sacrificial_anode_eol : 15000/600, 
                                    })
```

```python
TSA_1MVA_eol = newActivity(USER_DB,
                      'end of life treatment for TSA, 1MVA 66/0.4kv',
                      unit= 'kg',
                      exchanges = {
                          landfill_steel :(1-steel_recycled_share)* (2600+2200)/10250,
                          recycling_steel: steel_recycled_share * (2600+2200)/10250,
                          incineration_copper: 1450/10250,
                          landfill_paperboard : 1000*0.5/10250,
                          oil_waste: 2000/10250,
                          landfill_epoxy: 100/10250,
                      })
```

```python
landfill_lead = findTechAct('treatment of lead smelter slag, residual material landfill', 'GLO')
batteries_eol = newActivity(USER_DB,
                       'end of life treatment of Batteries 15, 20 and 50kw, 8h, 48, 127 and 400 VDC',
                       unit = 'kg',
                       exchanges = {
                           landfill_lead: (5797+5478)/16600,                      
                           incineration_plastic: 1328/16600,
                           landfill_hazard_waste: (1222+115)/16600,                   
                           landfill_inert: 90*2/16600,                  
                       })

cooling_radiators_eol = newActivity(USER_DB, 
                          'end of life treatment for cooling radiators, elevating transformer',
                          unit = 'kg',
                          exchanges = {
                              landfill_steel: 50000/60000,
                              oil_waste: 10000/60000,
                          })

transformers_330MVA_eol = newActivity(USER_DB, 
                                 'end of life treatment for transformers 330MVA-225-66kv',
                                 unit= 'kg',
                                 exchanges = {
                                     landfill_steel: (1-steel_recycled_share)*130000/275000,
                                     recycling_steel:steel_recycled_share * 130000/275000, 
                                     incineration_copper: 30000/275000, 
                                     landfill_paperboard: 15000*0.5/275000,                  
                                     oil_waste: 100000/275000,                                   
                                 })


psem_cells_225kv_eol = newActivity(USER_DB,
                        'end of life tratment for PSEM cells 225kv',
                        unit = 'kg',
                        exchanges = {
                            landfill_aluminium:alu_landfill_share*3440/5580,
                            incineration_aluminium: alu_incineration_share*3440/5580,
                            recycling_aluminium: alu_recycled_share*3440/5580,
                            landfill_steel: (1-steel_recycled_share)* (1380+240)/5580,
                            recycling_steel:steel_recycled_share *1380/5580,                     
                            landfill_epoxy: 150/5580,
                            landfill_hazard_waste: 150/5580,
                            incineration_copper: 90/5580,
                            landfill_polyethylene: 80/5580,
                        })


psem_cells_66kv_eol = newActivity(USER_DB,
                             'end of life treatment for PSEM cells 66kv',
                             unit = 'kg',
                             exchanges = {
                                landfill_aluminium:alu_landfill_share*1893/3062,
                                incineration_aluminium: alu_incineration_share*1893/3062,
                                recycling_aluminium: alu_recycled_share*1893/3062,
                                landfill_steel: (1-steel_recycled_share)* 645/3062,
                                recycling_steel:steel_recycled_share *645/3062,                     
                                 landfill_polyethylene: (230+2)/3062,
                                 landfill_hazard_waste: 101/3062,
                                 landfill_epoxy: 89/3062,
                                 incineration_copper:70/3062,
                                 landfill_rubber: 10/3062,
                                 landfill_PTFE:8/3062,
                                 landfill_paperboard: 6/3062,
                                 incineration_plastic: (3+1)/3062,
                                 landfill_zeolite: 2/3062,          
                             })

electric_components_eol = newActivity(USER_DB, 
                                 'end of life treatment for electric components materials',
                                 unit = 'unit', 
                                 exchanges = {
                                     TSA_1MVA_eol: 41000,
                                     batteries_eol: 33000,
                                     cooling_radiators_eol: 120000,
                                     psem_cells_225kv_eol:11000,
                                     psem_cells_66kv_eol:61000,
                                     transformers_330MVA_eol: 5500,
                                 }) 
```

```python
manipulate_equip_eol = newActivity(USER_DB,
                              'end of life tratment for manipulation equipment',
                              unit = 'kg',
                              exchanges = {
                                  landfill_steel: 1 - steel_recycled_share,
                                  recycling_steel: steel_recycled_share,
                              })
```

```python
acts = findTechAct('treatment of waste paint, municipal incineration', loc = 'Europe without Switzerland', single = False)
landfill_alkyd = next(act for act in acts if act["unit"] == 'kilogram')

diesel_generator_1000_eol = newActivity(USER_DB,
                              'end of life treatment for diesel generator 100kVA',
                                   unit = "kg",
                                   exchanges = {
                                       landfill_alkyd: 25/5791,
                                       landfill_aluminium: alu_landfill_share*150/5791,
                                       recycling_aluminium:alu_recycled_share*150/5791,
                                       incineration_aluminium:alu_incineration_share*150/5791,
                                       landfill_inert: (0.5+190)/5791,                                 
                                       incineration_copper: 250/5791,
                                       landfill_paperboard: 1.16/5791,
                                       landfill_polyethylene: 14/5791,
                                       landfill_steel: (1 - steel_recycled_share)*(250+4850)/5791,
                                       recycling_steel: steel_recycled_share*(250+4850)/5791    
                                   })

control_instrumentation_eol = newActivity(USER_DB,
                                     'end of life treatment for control instrumentation',
                                     unit = "unit",
                                      exchanges = {
                                          diesel_generator_1000_eol: 6000,                                                         
                                      })
```

```python
tank_sump_eol = newActivity(USER_DB,
                       'end of life treatment for sump tank drum and pump',
                       unit = 'kg',
                       exchanges = {
                           landfill_alkyd: 47/3830,
                           landfill_steel: 11/3830,
                           landfill_inert: (2+47)/3830,          
                           incineration_copper: 158/3830,
                           landfill_polyethylene: 4/3830,
                           landfill_steel: (1-steel_recycled_share)*3560/3830,
                           recycling_steel: steel_recycled_share * 3560/3830,
                       })

diesel_tank_eol = copyActivity(USER_DB,
    tank_sump_eol, #itial activity 
    "end of life treatment for diesel tank 3000L")

security_scrap_equipment_eol = newActivity(USER_DB,
                                      'end of life treatment for equipment water-scrap-safety',
                                      unit = 'unit',
                                      exchanges = {
                                          tank_sump_eol:8000,
                                          diesel_tank_eol:12000,
                                      })
```

```python
HVAC_cooling_eol = newActivity(USER_DB,
                          'end of life treatment for cooling for HVAC equipments',
                          unit = 'kg',
                          exchanges = {
                              landfill_steel:(1-steel_recycled_share)*185/430,
                              recycling_steel: steel_recycled_share *185/430,
                              incineration_copper: 123/430,
                              landfill_aluminium: alu_landfill_share*18/430,
                              incineration_aluminium: alu_incineration_share*18/430,
                              recycling_aluminium: alu_recycled_share*18/430,
                              landfill_inert: 3/430,
                              landfill_polyethylene: 15/430,
                              incineration_plastic: 9/430,
                              landfill_polystyrene: 1/430,                           
                              landfill_hazard_waste: 17/430,
                              landfill_paperboard: 7/430,                      
                          })
```

```python
offshore_sub_act_eol = newActivity(USER_DB,
                       "end of life treatment for offshore substation",
                       unit = "unit",
                       exchanges = {
                           offshore_sub_structure_eol_MW:1,
                           electric_components_eol:1,
                           manipulate_equip_eol:1,
                           control_instrumentation_eol:1,
                           security_scrap_equipment_eol:1,
                           HVAC_cooling_eol:1, 
                       })
offshore_sub_eol_MW = newActivity(USER_DB, 
                                 'end of life treatment for offshore substation per MW',
                                 unit = 'unit\MW',
                                 exchanges = {
                                     offshore_sub_act_eol:1/600,
                                 })
```

## Foudations

```python
foundations_gbf_eol_MW = newActivity(USER_DB,
                                "end of life treatment for gravity based foundations at depth 15m per MW",
                                 unit = "unit/MW",
                                exchanges = {
                                    landfill_steel:(1-steel_recycled_share)*336000/3,
                                    recycling_steel:steel_recycled_share*336000/3,
                                    landfill_concrete:(1-concrete_recycled_share)* 1027*2406.53/3,
                                    recycling_concrete: concrete_recycled_share*1027*2406.53/3,
                                })
```

```python
foundations_monopile_eol_MW = newActivity(USER_DB,
                                      "end of life treatment for monopile foundations at depth 20m per MW",
                                      unit = 'unit/MW',
                                      exchanges = {
                                          landfill_steel:(1-steel_recycled_share)*(276000+169500)/3,
                                          recycling_steel:steel_recycled_share*(276000+169500)/3,
                                          landfill_concrete:(1-concrete_recycled_share)* 21.3*2406.53/3,
                                          recycling_concrete: concrete_recycled_share*21.3*2406.53/3,
                                      })
```

```python
foundations_tripod_eol_MW = newActivity(USER_DB,
                                   'end of life treatment for tripod foundations at depth 50m per MW',
                                   unit = 'unit/MW',
                                   exchanges = {
                                       landfill_steel:(1-steel_recycled_share)*(807000+847000)/3,
                                       recycling_steel:steel_recycled_share*(807000+847000)/3,
                                       landfill_concrete:(1-concrete_recycled_share)* 63900/3,
                                       recycling_concrete: concrete_recycled_share*63900/3,
                                       })
```

```python
foundations_floating_eol_MW = newActivity(USER_DB,
                                     'end of life treatment for floating foundations per MW',
                                     unit ='unit/MW',
                                     exchanges = {
                                         landfill_steel:(1-steel_recycled_share)*(1000000+(5000*3))/3,
                                         recycling_steel:steel_recycled_share*(1000000+(5000*3))/3,
                                     })
```

```python
foundations_act_eol_MW = newActivity (USER_DB,
                                 'end of life treatment of foundations activity per MW',
                                 unit = 'unit/MW',
                                 exchanges = {
                                     foundations_gbf_eol_MW:fixed_foundations * gbf,
                                     foundations_monopile_eol_MW:fixed_foundations * monop, 
                                     foundations_tripod_eol_MW: fixed_foundations * tripod,
                                     foundations_floating_eol_MW: floating_foundations,
                                 })
```

## Export Cables

```python
export_cables_alu_eol_MW = newActivity(USER_DB,
                       "end of life treatment for export aluminium cables",
                       unit = "unit/MW",
                       exchanges = {
landfill_aluminium: alu_landfill_share*alu_ratio_expcable * 2710 * pi * 0.135**2 *(d_shore_substation-1)/(n_turbines*turbine_MW), 
incineration_aluminium: alu_incineration_share*alu_ratio_expcable * 2710 * pi * 0.135**2 *(d_shore_substation-1)/(n_turbines*turbine_MW),
recycling_aluminium:alu_recycled_share*alu_ratio_expcable * 2710 * pi * 0.135**2 *(d_shore_substation-1)/(n_turbines*turbine_MW),
landfill_steel: (1-steel_recycled_share)*steel_ratio_expcable * 7850 * pi * 0.135**2 *(d_shore_substation-1)/(n_turbines*turbine_MW),
recycling_steel: steel_recycled_share * steel_ratio_expcable * 7850 * pi * 0.135**2 *(d_shore_substation-1)/(n_turbines*turbine_MW),
landfill_lead: lead_ratio_expcable * 11342 * pi * 0.135**2 *(d_shore_substation-1)/(n_turbines*turbine_MW),
landfill_polyethylene : 0.21 * 970 * pi * 0.135**2 *(d_shore_substation-1)/(n_turbines*turbine_MW),
incineration_plastic : 0.09 * 946 * pi * 0.135**2 *(d_shore_substation-1)/(n_turbines*turbine_MW),
landfill_glassfibre:0.01 * 1.7 * pi * 0.135**2 *(d_shore_substation-1)/(n_turbines*turbine_MW),                        
                       })
```

```python
export_cables_cop_eol_MW = newActivity(USER_DB,
                       "end of life treatment for export copper cables",
                       unit = "unit",
                       exchanges = {
                           incineration_copper: copper_ratio_expcable * 8960 * pi * 0.135**2/(n_turbines*turbine_MW), 
                           landfill_steel: (1-steel_recycled_share)*steel_ratio_expcable * 7850 * pi * 0.135**2/(n_turbines*turbine_MW),
                           recycling_steel: steel_recycled_share*steel_ratio_expcable * 7850 * pi * 0.135**2/(n_turbines*turbine_MW),
                           landfill_lead: 0.22 * 11342 * pi * 0.135**2/(n_turbines*turbine_MW) ,
                           landfill_polyethylene : 0.15 * 970 * pi * 0.135**2/(n_turbines*turbine_MW),
                           incineration_plastic : 0.07 * 946 * pi * 0.135**2/(n_turbines*turbine_MW),
                           landfill_glassfibre:0.01 * 1.7 * pi * 0.135**2/(n_turbines*turbine_MW),
                           
                       })
```

## Inter-array cables

```python


interarray_cables_fixed_eol_MW = newActivity( USER_DB,
                       "end of life treatment for fixed inter-array cables per MW installed",
                       unit = "unit/MW",
                       exchanges = {
landfill_steel: (1-steel_recycled_share)*steel_ratio_intcable * 7850 * pi *0.135**2 * 8.5 * rotor_diameter * (n_turbines -1)/(n_turbines*turbine_MW),
recycling_steel:  steel_recycled_share*steel_ratio_intcable * 7850 * pi *0.135**2 * 8.5 * rotor_diameter * (n_turbines -1)/(n_turbines*turbine_MW),
incineration_copper: copper_ratio_intcable * 8960 * pi*0.135**2  * 8.5 * rotor_diameter * (n_turbines -1)/(n_turbines*turbine_MW),
landfill_lead : lead_ratio_intcable * 11342* pi *0.135**2 * 8.5 * rotor_diameter * (n_turbines -1)/(n_turbines*turbine_MW),
landfill_polyethylene : 0.06 * 970* pi * 8.5 *0.135**2 * rotor_diameter * (n_turbines -1)/(n_turbines*turbine_MW) ,
incineration_plastic : 0.03 * 946 * pi * 8.5 * 0.135**2 * rotor_diameter * (n_turbines -1)/(n_turbines*turbine_MW)  ,
                         
                       })
```

```python
interarray_cables_floating_eol_MW = newActivity( USER_DB,
                       "end of life treatment for floating inter-array cables per MW installed",
                       unit = "unit/MW",
                       exchanges = {
landfill_steel: steel_ratio_intcable * 7850 * pi *0.135**2 * (4* water_depth +8.5 * rotor_diameter) * (n_turbines -1)/(n_turbines*turbine_MW),
recycling_steel:steel_ratio_intcable * 7850 * pi *0.135**2 * (4* water_depth +8.5 * rotor_diameter) * (n_turbines -1)/(n_turbines*turbine_MW),
incineration_copper: copper_ratio_intcable * 8960 * pi*0.135**2  * (4* water_depth +8.5 * rotor_diameter)* (n_turbines -1)/(n_turbines*turbine_MW),
landfill_lead : lead_ratio_intcable * 11342* pi *0.135**2 * (4* water_depth +8.5 * rotor_diameter) * (n_turbines -1)/(n_turbines*turbine_MW),
landfill_polyethylene : 0.06 * 970* pi *0.135**2 * (4* water_depth +8.5 * rotor_diameter) * (n_turbines -1)/(n_turbines*turbine_MW) ,
incineration_plastic : 0.03 * 946 * pi *0.135**2 * (4* water_depth +8.5 * rotor_diameter) * (n_turbines -1)/(n_turbines*turbine_MW)  ,
                       })
```

```python
interarray_cables_eol_MW = newActivity (USER_DB, 
                                       "end of life treatment for inter-array cables per MW installed",
                                       unit = "unit/MW",
                                       exchanges = {
                                           interarray_cables_fixed_eol_MW:fixed_foundations,
                                           interarray_cables_floating_eol_MW:floating_foundations,
                                       })
```

# Life Cycle Model per phase 


Configuration of the choice of the preassembly method

```python
preassembly = newEnumParam(
    "preassembly", 
    values=["bunnyear", "separate", "rotor"], 
    default="bunnyear")
```

```python
movingparts_assembly_MW = newSwitchAct(
    USER_DB,
    "Moving parts assembly and shipping",
    preassembly,
    {
         "bunnyear": bunnyear_assembly_MW,
         "rotor": rotorstar_assembly_MW,
         "separate": seperateparts_assembly_MW,
    })

printAct(movingparts_assembly_MW)
```

#### Production and transport of raw materials

```python
raw_material_phase1_MW = newActivity(USER_DB, 
                                    'modelling of life cycle phase 1 per MW, production an transport of raw materials',
                                    unit = 'unit\MW',
                                    exchanges = {
                                        tower_act_MW :1,
                                        rotor_act_MW:1,
                                        nacelle_act_MW:1,
                                        foundations_act_MW:1,
                                        interarray_cables_act_MW:1,
                                        export_cables_alu_MW:1, 
                                        export_cables_cop_MW:1,
                                        offshore_sub_act_MW:1,
                                    })
```

## Transport to the onshore area and installation

```python
transp_onshore_install_MW = newActivity(USER_DB, 
                                       'modelling of life cycle phase 2 per MW, transport to the onshore area and installation',
                                       unit = 'unit\MW',
                                       exchanges = {
                                           foundations_install_act_MW:1,
                                           offshoresub_install_MW:1,
                                           movingparts_assembly_MW:1,
                                           riprap_activity_expcables_MW:1,
                                           posing_expcables_MW:1,
                                           posing_interraycables_act_MW :1,       
                                       })
```

 ## Operation and maintenance 

```python
maintenance_phase3_MW = newActivity(USER_DB, 
                                   'modelling of life cycle phase 3 per MW, operation and maintenance', 
                                   unit = 'unit\MW',
                                   exchanges = {
                                       turbines_maintenance_act_MW:1,
                                       maintenance_expcables_MW:1,
                                       maintenance_interraycables_act_MW:1,
                                       substation_maintenance_MW:1,  
                                   })
```

## Decommisioning

```python
decommissioning_phase4_MW = newActivity(USER_DB, 
                                       'modelling of life cycle phase 4 per MW, decommissioning',
                                       unit = 'unit\MW',
                                       exchanges = {
                                           decommissioning_turbines_MW:1,
                                           decommissioning_foundations_act_MW:1, 
                                           decommissioning_expcables_MW:1, 
                                           decommissioning_interarraycables_act_MW:1, 
                                           offshore_substation_decom_MW:1,                                       
                                       })
```

# En of life

```python
eol_phase5_MW = newActivity(USER_DB, 
                           'modelling of life cycle phase 5 per MW, end of life', 
                           unit = 'unit\MW',
                           exchanges = {
                               tower_eol_MW:1, 
                               rotor_eol_MW:1,
                               nacelle_eol_MW:1,
                               offshore_sub_eol_MW:1,
                               foundations_act_eol_MW:1,
                               export_cables_alu_eol_MW:1,
                               export_cables_cop_eol_MW:1,
                               interarray_cables_eol_MW:1,
                           })
```

# Parameterized model

```python
lca_model_wind_farm_MW = newActivity(USER_DB, 
                                 'complete life cycle assessment model of a fixed or floating wind farm per MW', 
                                    unit = 'unit\MW',
                                    exchanges = {
                                        raw_material_phase1_MW:1,
                                        transp_onshore_install_MW:1,
                                        maintenance_phase3_MW:1,
                                        decommissioning_phase4_MW:1,
                                        eol_phase5_MW:1,
                                    })
```

```python
lca_model_wind_farm_total = newActivity(USER_DB, 
                                       'complete life cycle assessment model of a fixed or floating wind farm',
                                       unit = 'unit',
                                       exchanges = {
                                           lca_model_wind_farm_MW: turbine_MW * n_turbines,
                                       })
```

```python
lca_model_wind_farm_fu = newActivity(USER_DB,
                                    'impact model per kwh electricity produced over life time',
                                    unit = 'unit\kwh', 
                                    exchanges = {
                                        lca_model_wind_farm_total: 1/(load_rate*8760*turbine_MW*1000*n_turbines*life_time),
                                    })
```

```python
multiLCAAlgebric(lca_model_wind_farm_fu, #model
                 impacts_ILCD, #impacts indicators lists   
                  #parameters
                #turbine_MW = 6,n_turbines = 3, water_depth = 70, fixed_foundations = 0, d_shore = 50
                )
```

```python
list_parameters()
```

```python

```
