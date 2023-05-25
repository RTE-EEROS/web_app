# LIFOWI model

This repository is a pure python export of the lif-owi model.
It does not have dependency to *Brightway2*, *lca_algebraic* nor *ecoinvent*

It only relies on *sympy*.

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
{% for param in model.params.values() -%} 
{{ param.name }} | {{ param.type }} | {{ param.default}} | {{  }} | {{ param.unit }} |
{% endfor %}


### Result

The method returns a tuple :
* **val** : The value of the impact. A single value if *axis*="total", a dictionnary of values otherwize
* **unit** : THe unit made of <methoid unit> / <functional unit>







