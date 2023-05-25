# LIFOWI model

This repository is a pure python export of the lif-owi model.
It does not have dependency to *Brightway2*, *lca_algebraic* nor *ecoinvent*

It only relies on *sympy* and *numpy*.

# Installation 

Install the dependencies 

> pip install -r requirements.txt

# Usage 

The model is encoded into [model.json](./model.json) .

The class *Model* can parse it and evaluate impacts.

The file [sample_usage.py](./sample_usage.py) shows typical usage.

## Loading the model

Parsing the model is long (around 20 seconds).  

Do it only once and keep it in memory.

```python
model = Model.from_file(FILENAME)
```

## Evaluate the model

```python
val, unit = model.evaluate(
    impact,
    functional_unit,
    axis,
    **params)   
```

### Arguments :

#### impact

The code of the chosen impact.

List of impacts :

| Code | Name | Unit |
|------|------|------|
| climate_change | ["('EF v3.0', 'climate change', 'global warming potential (GWP100)')"] | kg CO2-Eq | 
| particules | ["('EF v3.0', 'particulate matter formation', 'impact on human health')"] | disease incidence | 
| mineral_depletion | ["('EF v3.0', 'material resources: metals/minerals', 'abiotic depletion potential (ADP): elements (ultimate reserves)')"] | kg Sb-Eq | 
| acidification | ["('EF v3.0', 'acidification', 'accumulated exceedance (ae)')"] | mol H+-Eq | 
| toxicity_non_carcinogenic | ["('EF v3.0', 'human toxicity: non-carcinogenic', 'comparative toxic unit for human (CTUh) ')"] | CTUh | 
| toxicity_carcinogenic | ["('EF v3.0', 'human toxicity: carcinogenic', 'comparative toxic unit for human (CTUh) ')"] | CTUh | 
| land_use | ["('EF v3.0', 'land use', 'soil quality index')"] | dimensionless | 



#### functional unit 

3 functional units are supported :
* **"system"** : Whole system (no unit)
* **"energy"** : Per energy produced during lifetime (kWh)
* **"power"** : Per installed power (MW)

#### axis 

One of :
* **"total"** [default] : Only total impact computed. Asingle value will be returned
* **"system_1"** : By system part (level 1). A dictionnary of impacts per sub system is returned
* **"phase"** [NO WORKING YET]: By phase. A dictionnary of impacts per lifecycle phase will be returned

#### params

Any other argument is threated as a parameter :

| Name | Description  | Type | Default | Range | Unit |
|------|--------------|------|---------|-------|------|
n_turbines | the number of turbines in the wind farm |float | 30.0 | [1, 100] | turbines |
turbine_MW |  the unit capacity of one wind turbine |float | 5.0 | [2, 15] | MW |
life_time | the life time of wind farm |float | 20.0 | [20, 25] | years |
availability | ratio of the number of days per year when the windturbines are not stopped for maintenance |float | 1.0 | [0.9, 1] |  |
load_rate | ratio of the total electricity produced against the theoretical one for a year |float | 0.4 |  |  |
fixed_foundations | the type of foundations fixed/floating |bool | 1.0 |  |  |
steel_recycled_share_IN | The share of recycled steel used as an input to manufacture the wind farm components |float | 0.42 |  |  |
steel_recycled_share_OUT | The share of steel going to recycling after the wind farm decommissioning |float | 0.9 |  |  |
alu_recycled_share_IN | The share of recycled aluminium used as an input to manufacture the wind farm components |float | 0.39 |  |  |
alu_recycled_share_OUT | The share of aluminium going to recycling after the wind farm decommissioning |float | 0.9 |  |  |
alu_landfill_share | The share of landfilling aluminium waste in the wind farm |float | 0.05 |  |  |
alu_incineration_share | The share of incinerated aluminium waste in the wind farm |float | 0.05 |  |  |
concrete_recycled_share_IN | The share of recycled concrete used as an input to manufacture the wind farm components |float | 0.0 |  |  |
concrete_recycled_share_OUT | The share of concrete going to recycling after the wind farm decommissioning |float | 0.3 |  |  |
copper_recycled_share_IN | The share of recycled copper used as an input to manufacture the wind farm components |float | 0.0 |  |  |
copper_recycled_share_OUT | The share of copper going to recycling after the wind farm decommissioning |float | 0.0 |  |  |
mass_tower_steel | the mass of steel in the tower |float | 217022.0 |  | kg |
mass_tower_alu | the mass of aluminium in the tower |float | 3978.0 |  | kg |
mass_tower_concrete | the mass of concrete in the tower |float | 0.0 |  | kg |
mass_glass_fibre_rotor | the mass of glass fibre in the rotor |float | 43837.0 |  | kg |
mass_steel_personalised_foundations | the mass of steel for manufacturing the personalised foundations   |float | 742500.0 |  | kg |
mass_concrete_personalised_foundations | the mass of concrete for manufacturing the personalised foundations  |float | 35500.0 |  | kg |
mass_gravel_personalised_foundations | the mass of gravel for manufacturing the personalised foundations   |float | 0.0 |  | kg |
d_onshoresite_land | the distance between manufacturing and onshore site by road |float | 200.0 | [20, 1000] | km |
d_shore | The distance between the port (onshore area) and the windturbines in the sea (offshore area) |float | 12.3 | [5, 100] | km |
d_riprap | distance related to export cables being embedded (enrochement en français) |float | 1.0 | [1, 30] | km |
d_offshoresite_eol | the distance between the offshore site and the waste treatment center by road |float | 500.0 | [20, 1000] | km |
emission_ratio_anode | sacrificial anode degradation emission ratio for offshore substation |float | 0.0196 |  |  |
hub_height | the hub height (the height of the tower) |float | 120.0 | [90, 150] | m |
rotor_diameter | the rotor diameter of the wind turbine |float | 128.0 | [39, 154] | m |
steel_ratio_tower | the mass ratio of steel in tower |float | 0.98 |  |  |
aluminium_ratio_tower | the mass ratio of aluminium in tower |float | 0.02 |  |  |
concrete_ratio_tower | the mass ratio of concrete in tower |float | 0.0 |  |  |
water_depth | the water depth of the wind farm site |float | 20.0 | [10, 300] | m |
copper_ratio_intcable | the copper mass ratio in interarray cable |float | 0.33 |  |  |
lead_ratio_intcable | the lead mass ratio in interarray cable |float | 0.25 |  |  |
steel_ratio_intcable | the steel mass ratio in interarray cable |float | 0.33 |  |  |
HDPE_ratio_intcable | the high density polyehtylene mass ratio in interarray cable |float | 0.06 |  |  |
PP_ratio_intcable | the polypropylene mass ratio in interarray cable |float | 0.06 |  |  |
alu_ratio_expcable_alu | the aluminium mass ratio in aluminium export cable |float | 0.13 |  |  |
lead_ratio_expcable_alu | the lead mass ratio in aluminium export cable |float | 0.28 |  |  |
steel_ratio_expcable_alu | the steel mass ratio in aluminium export cable |float | 0.28 |  |  |
HDPE_ratio_expcable_alu | the high density polyethylene mass ratio in aluminium export cable |float | 0.21 |  |  |
PP_ratio_expcable_alu | the polypropylene mass ratio in aluminium export cable |float | 0.09 |  |  |
glass_ratio_expcable_alu | the glass fibre mass ratio in aluminium export cable |float | 0.01 |  |  |
copper_ratio_expcable_cop | the copper mass ratio in copper export cable |float | 0.28 |  |  |
lead_ratio_expcable_cop | the lead mass ratio in copper export cable |float | 0.22 |  |  |
steel_ratio_expcable_cop | the steel mass ratio in copper export cable |float | 0.28 |  |  |
HDPE_ratio_expcable_cop | the high density polyethylene mass ratio in copper export cable |float | 0.15 |  |  |
PP_ratio_expcable_cop | the polypropylene mass ratio in copper export cable |float | 0.07 |  |  |
glass_ratio_expcable_cop | the glass fibre mass ratio in copper export cable |float | 0.01 |  |  |
length_expcables_tot | the length of the path of one export cables that connect the offshore substation and the landfall junction (jonction d atterrage) : there are two types of export cables, aluminium and copper. Warning : this is not the total length of cables than can be doubled or tripled if there are 2 or 3 cables |float | 30000.0 | [10000, 100000] | m |
length_expcables_copper | the length of the path of one copper export cables. There are two types of cables : aluminium and copper. The sum of both lengths equals the total export cable length |float | 1000.0 |  | m |
foundations | the type of foundations |enum | tripod | gbf, monopod, tripod, floating, personalised |  |
preassembly |  the type of assembly method used for wind turbines moving parts |enum | bunnyear | bunnyear, separate, rotor |  |



### Result

The method returns a tuple :
* **val** : The value of the impact. A single value if *axis*="total", a dictionnary of values otherwize
* **unit** : The unit made of `method_unit / functional_unit`

### Example calls


#### Total axis
```python
model.evaluate(
    "climate_change",
    "power",
    "total",
    n_turbines=2) # Example of setting a parameter
```

Returns a single value and the unit :

```python
(17375068.714683194, 'kg CO2-Eq/MW')
```

#### System axis 

```python
model.evaluate(
    "climate_change",
    "energy",
    "system_1",
    n_turbines=2)
```

Should return a dictionnary of values, and the unit :
```python
({'foundations': 0.01047987290239726,
  'interarray-cables': 5.607305936073059e-07,
  'offshore substation': 0.00199266754489728,
  'export cables': 0.22898922381096948,
  'wind turbine': 0.003643896989155251},
 'kg CO2-Eq/kWh')
```








