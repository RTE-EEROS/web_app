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
n_turbines | the number of wind turbines in the wind farm |float | 46.0 | [1, 100] | turbines |
turbine_MW |  the unit capacity of one wind turbine |float | 13.0 | [5, 15] | MW |
life_time | the life time of wind farm |float | 25.0 | [20, 30] | years |
availability | ratio of time when the windturbines are not stopped for maintenance |float | 1.0 | [0.9, 1] |  |
elec_losses | ratio of electricity losses between the production (wind turbines) and the landfall junction |float | 0.017 | [0.002, 0.02] |  |
load_rate | ratio of the total electricity produced against the theoretical one for a year |float | 0.4 |  |  |
fixed_foundations | the type of foundations fixed/floating |bool | 1.0 |  |  |
water_depth | the water depth of the wind farm site |float | 30.0 | [10, 200] | m |
length_1_expcable_tot | the total length of one export cables |float | 30000.0 | [10000, 40000] | m |
length_1_expcable_cop | the length of one copper export cables |float | 1000.0 |  | m |
d_manufacturingsite_onshoresite_lorry | the distance between manufacturing site and onshore site that is done by lorry |float | 500.0 | [20, 1000] | km |
d_manufacturingsite_onshoresite_ship | the distance between manufacturing site and onshore site that is done by container ship |float | 500.0 | [20, 1000] | km |
d_shore | The distance between the port (onshore area) and the windturbines in the sea (offshore area) |float | 15.0 | [5, 50] | km |
steel_recycled_share_IN | The share of recycled steel used as an input to manufacture the wind farm components |float | 0.76 |  |  |
alu_recycled_share_IN | The share of recycled aluminium used as an input to manufacture the wind farm components |float | 0.3 |  |  |
copper_recycled_share_IN | The share of recycled copper used as an input to manufacture the wind farm components |float | 0.2 |  |  |
steel_recycled_share_OUT | The share of steel going to recycling after the wind farm decommissioning |float | 0.0 |  |  |
alu_recycled_share_OUT | The share of aluminium going to recycling after the wind farm decommissioning |float | 0.0 |  |  |
alu_landfill_share | The share of aluminium going to landfilling after the wind farm decommissioning |float | 1.0 |  |  |
alu_incineration_share | The share of aluminium going to incineration after the wind farm decommissioning |float | 0.0 |  |  |
copper_recycled_share_OUT | The share of copper going to recycling after the wind farm decommissioning |float | 0.0 |  |  |
copper_landfill_share | The share of copper going to landfilling after the wind farm decommissioning |float | 1.0 |  |  |
copper_incineration_share | The share of copper going to incineration after the wind farm decommissioning |float | 0.0 |  |  |
concrete_recycled_share_OUT | The share of concrete going to recycling after the wind farm decommissioning |float | 0.0 |  |  |
foundations_type | the type of foundations. Warning : water depth and foundation type are correlated |enum | tripod | gbf, monopod, tripod, floatingspar, custom |  |
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







