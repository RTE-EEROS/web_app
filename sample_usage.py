#!/usr/bin/env python
from lib.common import Model
import json, sys

from lib.utils import timer

INPUT_FILE="model.json"

def pretty_print(val) :
    if isinstance(val, dict) :
        val = json.dumps(val, indent=4)
    print(val)

if __name__ == '__main__':

    # Loading model is long : it should be done only once and kept in memory
    with timer("loading model"):
        with open(INPUT_FILE, "r") as f:
            js = json.load(f)
            model = Model.from_json(js)

    # Evaluation is fast
    with timer("eval model"):

        # Loop on axes
        for axis in ["total", "system_1"] :

            # Loop on impacts
            for impact in ["global warming potential (GWP100)"]:

                # Loop on functional unit
                for fu in ["energy", "power", "system"] :

                    val, unit = model.evaluate(
                        impact = impact,
                        functional_unit=fu,
                        axis=axis)

                    print("Result for axis:[%s], impact:[%s], functional unit:[%s], unit:[%s]" % (axis, impact, fu, unit))
                    pretty_print(val)
                    print()




