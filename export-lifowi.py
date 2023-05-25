#!/usr/bin/env python
import lca_algebraic as agb
from lib.export import export_lca, serialize_model, Model
import json

OUTFILE = "model.json"
PROJECT_NAME = "Parameterized_model_OWF_Original"
USER_DB = "lif-owi"
SYSTEM = "complete life cycle assessment model of a fixed or floating wind farm"
AXES = [None, "system_1"] # "phase" not working yet

LCIA_method = 'EF v3.0'

#climate_tot = (LCIA_method,'climate change no LT','global warming potential (GWP100) no LT')
climate_tot = (LCIA_method,'climate change','global warming potential (GWP100)')

#climate_bio = (LCIA_method,'climate change: biogenic no LT','global warming potential (GWP100) no LT')
climate_bio = (LCIA_method,'climate change: biogenic','global warming potential (GWP100)')

#climate_foss = (LCIA_method,'climate change: fossil no LT','global warming potential (GWP100) no LT')
climate_foss = (LCIA_method,'climate change: fossil','global warming potential (GWP100)')

#climate_land = (LCIA_method,'climate change: land use and land use change no LT','global warming potential (GWP100) no LT')
climate_land = (LCIA_method,'climate change: land use and land use change','global warming potential (GWP100)')

#ecosystem_quality_ecotox= (LCIA_method,'ecotoxicity: freshwater no LT','comparative toxic unit for ecosystems (CTUe)  no LT')
ecosystem_quality_ecotox= (LCIA_method,'ecotoxicity: freshwater','comparative toxic unit for ecosystems (CTUe) ')

#ecosystem_quality_acid = (LCIA_method,'acidification no LT','accumulated exceedance (ae) no LT')
ecosystem_quality_acid = (LCIA_method,'acidification','accumulated exceedance (ae)')

#ecosystem_quality_fresh_eut = (LCIA_method,'eutrophication: freshwater no LT','fraction of nutrients reaching freshwater end compartment (P) no LT')
ecosystem_quality_fresh_eut = (LCIA_method,'eutrophication: freshwater','fraction of nutrients reaching freshwater end compartment (P)')

#ecosystem_quality_mar_eut = (LCIA_method,'eutrophication: marine no LT','fraction of nutrients reaching marine end compartment (N) no LT'),
ecosystem_quality_mar_eut = (LCIA_method,'eutrophication: marine','fraction of nutrients reaching marine end compartment (N)')

#ecosystem_quality_ter_eut=(LCIA_method,'eutrophication: terrestrial no LT','accumulated exceedance (AE)  no LT')
ecosystem_quality_ter_eut=(LCIA_method,'eutrophication: terrestrial','accumulated exceedance (AE) ')

#human_health_io= (LCIA_method,'ionising radiation: human health no LT','human exposure efficiency relative to u235 no LT')
human_health_io= (LCIA_method,'ionising radiation: human health','human exposure efficiency relative to u235')

#human_health_oz= (LCIA_method,'ozone depletion no LT','ozone depletion potential (ODP)  no LT')
human_health_oz= (LCIA_method,'ozone depletion','ozone depletion potential (ODP) ')

#human_health_pht= (LCIA_method, 'photochemical ozone formation: human health no LT','tropospheric ozone concentration increase no LT')
human_health_pht= (LCIA_method, 'photochemical ozone formation: human health','tropospheric ozone concentration increase')

#human_health_res= (LCIA_method,'particulate matter formation no LT','impact on human health no LT')
human_health_res= (LCIA_method,'particulate matter formation','impact on human health')

#human_health_noncar= (LCIA_method,'human toxicity: non-carcinogenic no LT','comparative toxic unit for human (CTUh)  no LT')
human_health_noncar= (LCIA_method,'human toxicity: non-carcinogenic','comparative toxic unit for human (CTUh) ')

#human_health_car= (LCIA_method,'human toxicity: carcinogenic no LT','comparative toxic unit for human (CTUh)  no LT')
human_health_car= (LCIA_method,'human toxicity: carcinogenic','comparative toxic unit for human (CTUh) ')

#resources_foss =(LCIA_method,  'energy resources: non-renewable no LT',  'abiotic depletion potential (ADP): fossil fuels no LT')
resources_foss =(LCIA_method,  'energy resources: non-renewable',  'abiotic depletion potential (ADP): fossil fuels')

#resources_land = (LCIA_method, 'land use no LT', 'soil quality index no LT')
resources_land = (LCIA_method, 'land use', 'soil quality index')

#resources_min_met =(LCIA_method,'material resources: metals/minerals no LT','abiotic depletion potential (ADP): elements (ultimate reserves) no LT')
resources_min_met =(LCIA_method,'material resources: metals/minerals','abiotic depletion potential (ADP): elements (ultimate reserves)')

# resources_water = (LCIA_method,  'water use no LT',  'user deprivation potential (deprivation-weighted water consumption) no LT')
resources_water = (LCIA_method,  'water use',  'user deprivation potential (deprivation-weighted water consumption)')

impacts_EF_3_0 = {impact[2]: impact for impact in [climate_tot, climate_bio, climate_foss, climate_land, ecosystem_quality_ecotox,ecosystem_quality_acid,
                  ecosystem_quality_fresh_eut,
                  ecosystem_quality_mar_eut,
                  ecosystem_quality_ter_eut, human_health_io,
                  human_health_oz, human_health_pht, human_health_res, human_health_noncar, human_health_car, resources_foss,
                  resources_land, resources_min_met, resources_water]}

impacts_EF_CO2 = {climate_tot[2]:climate_tot}


def export():

    agb.initProject(PROJECT_NAME)
    agb.loadParams()

    system = agb.findActivity(code=SYSTEM, db_name=USER_DB)

    FUNCTIONAL_UNITS = {
        "energy": dict(
            quantity=load_rate * availability * 8760 * turbine_MW * 1000 * n_turbines * life_time,
            unit="kWh"),
        "installed_power": dict(
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
        methods_dict=impacts_EF_3_0,
        axes=AXES)

    js = serialize_model(model)

    with open(OUTFILE, "w") as f:
        json.dump(js, f, indent=4)

if __name__ == '__main__':
    export()





