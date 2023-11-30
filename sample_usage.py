#!/usr/bin/env python
from lib.common import Model
import json, sys

from lib.utils import timer
from lib.settings import settings, OUTFILE


def pretty_print(val) :
    if isinstance(val, dict) :
        val = json.dumps(val, indent=4)
    print(val)

if __name__ == '__main__':

    # Loading model is long : it should be done only once and kept in memory
    with timer("loading model"):
        model = Model.from_file(OUTFILE)

    # Evaluation is fast
    with timer("eval model"):

        # Loop on axes
        for axis in settings.axes :

            if axis is None :
                axis = "total"

            # Loop on impacts
            for impact in settings.impacts.keys():

                # Loop on functional unit
                for fu in ["energy", "power", "system"] :

                    val, unit = model.evaluate(
                        impact = impact,
                        functional_unit=fu,
                        axis=axis)

                    print("Result for axis:[%s], impact:[%s], functional unit:[%s], unit:[%s]" % (axis, impact, fu, unit))
                    pretty_print(val)
                    print()




