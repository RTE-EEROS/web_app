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
{% for code, impact in model.impacts.items() -%}
| {{ code }} | {{ impact.name }} | {{ impact.unit}} | 
{% endfor %}


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
{% for param in model.params.values() -%} 
{{ param.name }} | {{ param.label }} |{{ param.type }} | {{ param.default}} | {{ param.range }} | {{ param.unit }} |
{% endfor %}


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








