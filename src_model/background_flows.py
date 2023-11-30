# -*- coding: utf-8 -*-
import lca_algebraic as agb
import pandas as pd
USER_DB='lif-owi'


# **Warning** 
# Activities with negative flows are corrected with **negAct function**.
# We use negAct function to correct the sign of some activities that are accounted as negative in brightway (mostly waste treatment activities)
# Warning, if you print activities defined with negAct, the reference flow will still appear as negative
# when you print them with agb.printAct
# but it will be accounted as a positive flow (you can compute a basic impact calcultation to check that)

def negAct(act) :
    """Correct the sign of some activities that are accounted as negative in brightway. """
    return agb.newActivity(USER_DB, act["name"] + "_neg", act["unit"], {
        act:-1,
    })


def import_background() :
    
    steel_low_alloyed = agb.findTechAct('market for steel, low-alloyed','GLO')
    steel_unalloyed = agb.findTechAct('market for steel, unalloyed', 'GLO')
    aluminium = agb.findTechAct('market for aluminium, wrought alloy','GLO')
    concrete = agb.findTechAct('market group for concrete, normal','GLO')
    glass_fibre = agb.findTechAct('market for glass fibre','GLO')
    epoxy = agb.findTechAct('market for epoxy resin, liquid','RER')
    wood_mix = agb.findTechAct('sawnwood, paraná pine, dried (u=10%), import from BR', 'RER')
    polypropylene = agb.findTechAct('market for polypropylene, granulate', 'GLO')
    cast_iron = agb.findTechAct('market for cast iron', 'GLO')
    chromium_steel = agb.findTechAct('market for steel, chromium steel 18/8', 'GLO')
    sand = agb.findTechAct('market for silica sand', 'GLO')
    copper = agb.findTechAct('market for copper, cathode', 'GLO')
    polyethylene_HD = agb.findTechAct('market for polyethylene, high density, granulate', 'GLO')
    steel_reinforcing = agb.findTechAct('market for reinforcing steel', 'GLO')
    lubricating_oil = agb.findTechAct('market for lubricating oil', 'RER')
    lead = agb.findTechAct('market for lead', 'GLO')
    hfo_consumption = agb.findTechAct("heavy fuel oil, burned in refinery furnace*",loc="Europe without Switzerland")
    paper_printed = agb.findTechAct('market for printed paper', 'GLO')
    wood_board = agb.findTechAct('market for three and five layered board', 'RER')
    gravel = agb.findTechAct('market for gravel, crushed', 'CH')
    gravel_riprap = agb.findTechAct('market for gravel, round', 'CH')
    tin = agb.findTechAct('market for tin', 'GLO')
    zinc = agb.findTechAct('market for zinc', 'GLO')
    indium = agb.findTechAct('market for indium', 'GLO')
    silicon = agb.findTechAct('market for silicon, electronics grade', 'GLO')
    cadmium = agb.findTechAct('market for cadmium','GLO')
    zinc_coat = agb.findTechAct('zinc coating, pieces', 'RER')

    concrete_found = agb.findTechAct('market for concrete, sole plate and foundation', 'CH')

    pet = agb.findTechAct('market for polyethylene terephthalate, granulate, amorphous', 'GLO')
    synthetic_rubber = agb.findTechAct('market for synthetic rubber', 'GLO')
    nylon_6 = agb.findTechAct('market for nylon 6-6, glass-filled', 'RER')
    zeolite = agb.findTechAct('market for zeolite, powder', 'GLO')
    pmma = agb.findTechAct('market for polymethyl methacrylate, sheet') ### Control instrumentation
    brass = agb.findTechAct('market for brass', 'CH')
    polystyrene= agb.findTechAct('market for polystyrene, general purpose','GLO')
    stone_wool = agb.findTechAct('market for stone wool', 'GLO')

    #chemicals
    sulfuric_acid = agb.findTechAct('market for sulfuric acid','RER')
    phosphoric_acid = agb.findTechAct('market for phosphoric acid, industrial grade, without water, in 85% solution state', 'GLO')
    antimony = agb.findTechAct('market for antimony', 'GLO')
    sf_6 = agb.findTechAct('market for sulfur hexafluoride, liquid','RER')
    tetrafluoroethylene = agb.findTechAct('market for tetrafluoroethylene', 'GLO')
    co_2 = agb.findTechAct('market for carbon dioxide, liquid', 'RER')
    refrigerant = agb.findTechAct('market for refrigerant R134a','GLO')

    #Energy
    electricity_UCTE = agb.findTechAct('market group for electricity, medium voltage', 'UCTE')
    diesel_consumption = agb.findTechAct('market for diesel, burned in fishing vessel','GLO')
    diesel_process = agb.findTechAct('market for diesel, burned in building machine', 'GLO')
    diesel_maintenance = agb.findTechAct('market for diesel, burned in diesel-electric generating set, 10MW', 'GLO')
    district_heating = agb.findTechAct('heat, non-market, at cogen 160kWe Jakobsberg, allocation exergy', 'CH')
    welding_gas = agb.findTechAct('market for welding, gas, steel', 'GLO')
    fuel_oil_process = agb.findTechAct('market for heavy fuel oil, burned in refinery furnace', 'GLO')
    natural_gas = agb.findTechAct('market for natural gas, high pressure', 'DE')
    heat = agb.findTechAct('heat production, natural gas, at industrial furnace >100kW', 'Europe without Switzerland')
    welding = agb.findTechAct('market for welding, gas, steel', 'GLO')
    kerosene = agb.findTechAct("market for kerosene", 'Europe without Switzerland')

    #Processing materials
    copper_process = agb.findTechAct('wire drawing, copper', 'RER')
    steel_process = agb.findTechAct('sheet rolling, steel', 'RER')
    steel_process_2=agb.findTechAct("market for wire drawing, steel")
    steel_weld = agb.findTechAct('welding, arc, steel', 'RER')
    zinc_process = agb.findTechAct('zinc coating, coils', 'RER')
    alu_process = agb.findTechAct('market for sheet rolling, aluminium')
    lead_process = agb.findTechAct('market for drawing of pipe, steel')
    plastic_process = agb.findTechAct('market for extrusion, plastic pipes')

    #transport
    lorry_transp = agb.findTechAct('transport, freight, lorry >32 metric ton, EURO6', 'RER')
    rotor_nacelle_transp = agb.findTechAct('transport, freight, lorry 7.5-16 metric ton, EURO5','RER')
    container_ship = agb.findTechAct('transport, freight, sea, container ship', 'GLO')
    barge_transp = agb.findTechAct('transport, freight, inland waterways, barge', 'RER')
    transformers_transport = agb.findTechAct('transport, freight, sea, container ship', 'GLO')
    equip_transport = agb.findTechAct('transport, freight, lorry 16-32 metric ton, EURO6','RER')

    #others
    excavation = agb.findTechAct('excavation, hydraulic digger','RER')
    water = agb.findTechAct('market for tap water', 'Europe without Switzerland')
    alkyd = agb.findTechAct('market for alkyd paint, white, without solvent, in 60% solution state', 'RER')
    electric_comp = agb.findTechAct('market for printed wiring board, surface mounted, unspecified, Pb free','GLO')
    linerboard = agb.findTechAct('market for containerboard, linerboard', 'RER')
    brazing = agb.findTechAct('market for brazing solder, cadmium free', 'GLO')

    #end-of-life treatment 
    landfill_copper=negAct(agb.findTechAct('treatment of copper slag, residual material landfill','GLO'))
    landfill_lead = negAct(agb.findTechAct('treatment of lead smelter slag, residual material landfill', 'GLO'))
    landfill_silicon = negAct(agb.findTechAct('treatment of waste, from silicon wafer production, inorganic, residual material landfill', 'CH'))
    landfill_zinc = negAct(agb.findTechAct('treatment of zinc slag, residual material landfill', 'GLO'))
    landfill_inert = negAct(agb.findTechAct('treatment of inert waste, sanitary landfill', 'Europe without Switzerland'))
    landfill_polyethylene = negAct(agb.findTechAct('treatment of waste polyethylene, sanitary landfill', 'CH'))
    landfill_rubber = negAct(agb.findTechAct('market for waste rubber, unspecified','CH'))
    landfill_PTFE = negAct(agb.findTechAct('treatment of waste polyvinylchloride, sanitary landfill', 'CH'))
    landfill_polystyrene = negAct(agb.findTechAct('treatment of waste polystyrene, sanitary landfill', 'CH'))
    landfill_hazard_waste = negAct(agb.findTechAct('treatment of hazardous waste, underground deposit', 'RoW'))
    landfill_paperboard = negAct(agb.findTechAct('treatment of waste paperboard, sanitary landfill', 'RoW'))
    landfill_zeolite = negAct(agb.findTechAct('treatment of waste zeolite, inert material landfill', 'CH'))
    landfill_steel = negAct(agb.findTechAct('treatment of scrap steel, inert material landfill','CH'))
    landfill_aluminium = negAct(agb.findTechAct('treatment of waste aluminium, sanitary landfill','CH'))
    landfill_concrete = negAct(agb.findTechAct('treatment of waste concrete, inert material landfill', 'CH'))
    landfill_wood=negAct(agb.findTechAct("treatment of waste wood, untreated, sanitary landfill",loc="RoW"))
    landfill_glassfibre = negAct(agb.findTechAct('treatment of waste glass, inert material landfill','CH'))
    landfill_epoxy = negAct(agb.findTechAct('treatment of waste plastic, mixture, sanitary landfill', 'CH'))
    
    incineration_aluminium = negAct(agb.findTechAct('treatment of aluminium in car shredder residue, municipal incineration','CH'))
    incineration_copper = negAct(agb.findTechAct('treatment of copper in car shredder residue, municipal incineration','CH'))
    incineration_plastic = negAct(agb.findTechAct('treatment of waste plastic, industrial electronics, municipal incineration','CH'))
    
    wastewater_treatment = negAct(agb.findTechAct('treatment of wastewater, average, capacity 1.6E8l/year','CH'))
    waste_unspecified = negAct(agb.findTechAct('treatment of inert waste, inert material landfill', 'CH'))
    waste_hazardous = negAct(agb.findTechAct ('treatment of hazardous waste, underground deposit', 'DE'))
    oil_waste = negAct(agb.findTechAct ('treatment of waste mineral oil, hazardous waste incineration', 'CH'))

    #Recycled materials for end of life (not used as end of life is modeled with cut-off approach).
    #We let this in the model if someone wants to use another end of life modeling (Circular Footprint Formula for example)
    alu_recycled=agb.findTechAct('treatment of aluminium scrap, new, at remelter','RoW')
    steel_recycled = agb.findTechAct('steel production, electric, low-alloyed', 'Europe without Switzerland and Austria')
    recycling_concrete = negAct(agb.findTechAct('treatment of waste concrete, not reinforced, recycling', 'CH')) #not to produce recycled concrete
    
    #As there are 3 activities with the same name but different units in ecoinvent
    # we generate a list of these activities and then pick the one with the chosen unit
    copper_recycled = agb.findTechAct('treatment of used cable', loc="GLO", single = False)
    copper_recycled = next(act for act in copper_recycled if act["unit"] == 'kilogram')
    copper_recycled = negAct(copper_recycled)
    
    landfill_alkyd = agb.findTechAct('treatment of waste paint, municipal incineration', loc = 'Europe without Switzerland', single = False)
    landfill_alkyd = next(act for act in landfill_alkyd if act["unit"] == 'kilogram')
    landfill_alkyd=negAct(landfill_alkyd)
    
    return locals()


def print_background(acts):
    df=pd.DataFrame([dict(
        name=key,
        background_flow=act["name"],
        loc=act["location"],
        unit=act["unit"]) 
                  for key, act in acts.items()])
    return df
