#!/usr/bin/env python
from jinja2 import FileSystemLoader, Environment
import json

TEMPLATE="readme.jinja.md"
MODEL="data/model.json"
OUT="README.md"

environment = Environment(loader=FileSystemLoader("static/"))
template = environment.get_template(TEMPLATE)

with open(MODEL, "r") as f:
    model = json.load(f)

# Set param "ranges"
for param in model["params"].values() :
    if "values" in param :
        param["range"] = ", ".join(param["values"])
    elif param.get("min", None) :
        param["range"] = "[%.15g, %.15g]" % (param["min"], param["max"])


with open(OUT, "w") as out :
    res = template.render(model=model)
    out.write(res)