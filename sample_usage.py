#!/usr/bin/env python
from lca_algebraic.export import export_lca, serialize_model, Model
import json, sys

INPUT_FILE=sys.argv[1]

if __name__ == '__main__':

    with open(INPUT_FILE, "r") as f:
        js = json.load(f)
        model = Model.from_json(js)

    val = model.evaluate(
        impact = "global warming potential (GWP100)",
        functional_unit="system",
        axis="system_1",
        n_turbines=3)

    print(val)




