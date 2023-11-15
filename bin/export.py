#!/usr/bin/env python
import os
import sys
import dataclasses

# Add current dir to PATH
sys.path.insert(0, os.getcwd())


import lca_algebraic as agb
from lib.export import export_lca
from lib.settings import settings, OUTFILE


def export():

    agb.initProject(settings.project)
    agb.loadParams()

    try:
        system = agb.findActivity(code=settings.root_activity, db_name=settings.database)
    except:
        system = agb.findActivity(name=settings.root_activity, db_name=settings.database)

    dict_settings = dataclasses.asdict(settings)

    # Parse quantity
    for fu in dict_settings["functional_units"].values() :
        fu["quantity"] = eval(str(fu["formula"]))

    print(dict_settings)

    model = export_lca(
        system=system,
        functional_units=dict_settings["functional_units"],
        methods_dict=dict_settings["impacts"],
        axes=settings.axes)

    model.to_file(OUTFILE)


if __name__ == '__main__':
    export()





