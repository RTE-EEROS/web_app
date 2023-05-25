
from typing import Dict
from lca_algebraic import SymDict, ParamDef
from lca_algebraic.base_utils import _method_unit
from lca_algebraic.lca import _preMultiLCAAlgebric
from lca_algebraic.params import _param_registry
from lca_algebraic.stats import _round_expr
from lib.common import FunctionalUnit, Lambda, Impact, Model, Param


def round_expr(exp_or_dict, num_digits):
    if isinstance(exp_or_dict, dict) :
        return dict({key: _round_expr(val, num_digits) for key, val in exp_or_dict.items()})
    else:
        return _round_expr(exp_or_dict, num_digits)

def paramDef_to_param(paramDef:ParamDef):
    return Param(
        name=paramDef.name,
        type=paramDef.type,
        unit=paramDef.unit,
        default=paramDef.default,
        label=paramDef.label,
        values=getattr(paramDef, "values", None),
        min=paramDef.min,
        max=paramDef.max,
        description=paramDef.description)

def export_lca(
        system,
        functional_units : Dict[str, Dict],
        methods_dict,
        axes=None,
        num_digits=3):
    """
    :param system: Root inventory
    :param functional_units : Dict of Dict{unit, quantity}
    :param methods_dict: dict of method_name => method tuple
    :param axes: List of axes
    :param num_digits: Number of digits
    :return: an instance of "Model"
    """

    if axes is None:
        axes = [None]

    # Transform all lca_algebraic parameters to exported ones
    all_params = {param.name: paramDef_to_param(param) for param in _param_registry().all()}

    impacts_by_axis = dict()

    for axis in axes :
        print("Processing axis %s" % axis)

        lambdas = _preMultiLCAAlgebric(
            system,
            list(methods_dict.values()),
            axis=axis)

        if axis is None:
            axis = "total"

        # Simplify
        for lambd, method_name  in zip(lambdas, methods_dict.keys()):

            if isinstance(lambd.expr, SymDict):
                lambd.expr = lambd.expr.dict
            lambd.expr = round_expr(lambd.expr, num_digits=num_digits)

        # Save
        impacts_by_axis[axis] = {
            method: Lambda(lambd.expr, all_params)
            for method, lambd in zip(methods_dict.keys(), lambdas)}

    # Dict of functional units
    functional_units = {
        name: FunctionalUnit(
            quantity=Lambda(fu["quantity"], all_params),
            unit=fu["unit"])
        for name, fu in functional_units.items()}

    # Build list of impacts
    impacts = {key: Impact(
        name = str(method),
        unit = _method_unit(method)
    ) for key, method in methods_dict.items()}

    return Model(
        params=all_params,
        functional_units=functional_units,
        expressions=impacts_by_axis,
        impacts=impacts)



