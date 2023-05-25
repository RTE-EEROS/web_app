# Settings common to both export and import, for lifowi

OUTFILE = "model.json"

AXES = [None, "system_1"] # "phase" not working yet

LCIA_method = 'EF v3.0'

IMPACTS = {
    "climate_change" : (LCIA_method,'climate change','global warming potential (GWP100)'), # Climate change total
    "particules" : (LCIA_method,'particulate matter formation','impact on human health'),
    "mineral_depletion" : (LCIA_method,'material resources: metals/minerals','abiotic depletion potential (ADP): elements (ultimate reserves)'),
    "acidification" : (LCIA_method,'acidification','accumulated exceedance (ae)'),
    "toxicity_non_carcinogenic" : (LCIA_method,'human toxicity: non-carcinogenic','comparative toxic unit for human (CTUh) '),
    "toxicity_carcinogenic" : (LCIA_method,'human toxicity: carcinogenic','comparative toxic unit for human (CTUh) '),
    "land_use" : (LCIA_method, 'land use', 'soil quality index')
}
