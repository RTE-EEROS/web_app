#!/usr/bin/env python
from jinja2 import FileSystemLoader, Environment
import json

TEMPLATE="readme.jinja.md"
MODEL="model.json"

environment = Environment(loader=FileSystemLoader("res/"))
template = environment.get_template(TEMPLATE)

with open(MODEL, "r") as f:
    model = json.load(f)

res = template.render(model=model)

print(res)