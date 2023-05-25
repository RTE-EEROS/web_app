# LIFOWI model

This repository is a pure python export of the lif-owi model.

It does not have dependency to *Brightway2*, *lca_algebraic* nor *ecoinvent*

It only relies on *Sympy*.

# Installation 

> pip install -r requirements.txt

# Usage 

The model is encoded into `model.json`.
The class *Model* can parse and evaluate it

The file [sample_usage.py](./sample_usage.py) shows typical usage.

## Loading the model

Parsing the model is long (around 20 seconds). Do it only once and keep it in memory.

```python
with open(INPUT_FILE, "r") as f:
    js = json.load(f)
    model = Model.from_json(js)
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

#### functional unit 

3 functional units are supported :
* `system` : Whole system (no unit)
* `energy` : Per energy produced during lifetime (kWh)
* `power` : Per installed power (MW)

#### params

Any other argument is threated as a parameter :

| Name | Type | Default | Range | Unit |
|------|------|---------|-------|------|
n_turbines | float | 30.0 | turbines   |
turbine_MW | float | 5.0 | MW         |
life_time | float | 20.0 | years      |
availability | float | 1.0 |            |
load_rate | float | 0.4 |            |
fixed_foundations | bool | 1.0 |            |
steel_recycled_share_IN | float | 0.42 |            |
steel_recycled_share_OUT | float | 0.9 |            |
alu_recycled_share_IN | float | 0.39 |            |
alu_recycled_share_OUT | float | 0.9 |            |
alu_landfill_share | float | 0.05 |            |
alu_incineration_share | float | 0.05 |            |
concrete_recycled_share_IN | float | 0.0 |            |
concrete_recycled_share_OUT | float | 0.3 |            |
copper_recycled_share_IN | float | 0.0 |            |
copper_recycled_share_OUT | float | 0.0 |            |
mass_tower_steel | float | 217022.0 | kg         |
mass_tower_alu | float | 3978.0 | kg         |
mass_tower_concrete | float | 0.0 | kg         |
mass_glass_fibre_rotor | float | 43837.0 | kg         |
mass_steel_personalised_foundations | float | 742500.0 | kg         |
mass_concrete_personalised_foundations | float | 35500.0 | kg         |
mass_gravel_personalised_foundations | float | 0.0 | kg         |
d_onshoresite_land | float | 200.0 | km         |
d_shore | float | 12.3 | km         |
d_riprap | float | 1.0 | km         |
d_offshoresite_eol | float | 500.0 | km         |
emission_ratio_anode | float | 0.0196 |            |
hub_height | float | 120.0 | m          |
rotor_diameter | float | 128.0 | m          |
steel_ratio_tower | float | 0.98 |            |
aluminium_ratio_tower | float | 0.02 |            |
concrete_ratio_tower | float | 0.0 |            |
water_depth | float | 20.0 | m          |
copper_ratio_intcable | float | 0.33 |            |
lead_ratio_intcable | float | 0.25 |            |
steel_ratio_intcable | float | 0.33 |            |
HDPE_ratio_intcable | float | 0.06 |            |
PP_ratio_intcable | float | 0.06 |            |
alu_ratio_expcable_alu | float | 0.13 |            |
lead_ratio_expcable_alu | float | 0.28 |            |
steel_ratio_expcable_alu | float | 0.28 |            |
HDPE_ratio_expcable_alu | float | 0.21 |            |
PP_ratio_expcable_alu | float | 0.09 |            |
glass_ratio_expcable_alu | float | 0.01 |            |
copper_ratio_expcable_cop | float | 0.28 |            |
lead_ratio_expcable_cop | float | 0.22 |            |
steel_ratio_expcable_cop | float | 0.28 |            |
HDPE_ratio_expcable_cop | float | 0.15 |            |
PP_ratio_expcable_cop | float | 0.07 |            |
glass_ratio_expcable_cop | float | 0.01 |            |
length_expcables_tot | float | 30000.0 | m          |
length_expcables_copper | float | 1000.0 | m          |
foundations | enum | tripod |            |
preassembly | enum | bunnyear |            |



### Result

The method returns a tuple :
* **val** : The value of the impact. A single value if *axis*="total", a dictionnary of values otherwize
* **unit** : THe unit made of <methoid unit> / <functional unit>







