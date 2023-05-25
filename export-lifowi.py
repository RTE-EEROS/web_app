#!/usr/bin/env python
import lca_algebraic as agb
from lib.export import export_lca
from lib.common import Model, serialize_model
import json

from settings import IMPACTS, AXES, OUTFILE

PROJECT_NAME = "Parameterized_model_OWF_Original"
USER_DB = "lif-owi"
SYSTEM = "complete life cycle assessment model of a fixed or floating wind farm"

def export():

    agb.initProject(PROJECT_NAME)
    agb.loadParams()

    system = agb.findActivity(code=SYSTEM, db_name=USER_DB)

    FUNCTIONAL_UNITS = {
        "energy": dict(
            quantity=load_rate * availability * 8760 * turbine_MW * 1000 * n_turbines * life_time,
            unit="kWh"),
        "power": dict(
            quantity=turbine_MW * n_turbines,
            unit="MW"
        ),
        "system": dict(
            quantity=1,
            unit=None)
    }

    model = export_lca(
        system=system,
        functional_units=FUNCTIONAL_UNITS,
        methods_dict=IMPACTS,
        axes=AXES)

    model.to_file(OUTFILE)


if __name__ == '__main__':
    export()





