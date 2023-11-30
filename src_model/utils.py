# +
import lca_algebraic as agb
import pandas as pd

from sympy import Expr
from lca_algebraic.params import _param_registry
from pandas import DataFrame
from typing import List

from bw2data.backends.peewee import ActivityDataset, Activity
from lca_algebraic import DbContext
from lca_algebraic.lca import _preMultiLCAAlgebric, _postMultiLCAAlgebric
from lca_algebraic.params import _fixed_params
from lca_algebraic.base_utils import error, _actName
from lca_algebraic import NameType
from lca_algebraic.params import _param_name, _param_registry


# -
def compute_value(formula, **params):
    """ Compute actual value for a given formula, with possible parameters (or default ones) """
    if isinstance(formula, float) or isinstance(formula, int) :
        return formula
    
    symbols = {str(free):free for free in formula.free_symbols}
    replace_vals = {symbol: symbol.default for name, symbol in symbols.items()}
    replace_vals.update({symbols[name]: value for name, value in params.items() if name in symbols})

    return formula.evalf(subs=replace_vals)


def values_table(**variables) :
    """
    Display a table of all intermediate formula : their name, formula and value.
    
    variables: dict of variables (either formula or python variable). Value can be tuple (value, unit)
    """

    res = []
    has_unit = False
    
    for name, variable in list(variables.items()):
        
        if isinstance(variable, list) or isinstance(variable, tuple) :
            variable, unit = variable
            has_unit = True
        else:
            unit = None
        
        if isinstance(variable, Expr) :
            value = compute_value(variable)
        elif isinstance(variable, float) or isinstance(variable, int) :
            value = variable
        else:
            raise Exception("%s is neither a numeric value nor a Sympy Expression" % name)
        
        res.append(dict(
            name=name,
            formula=variable,
            value=float(value),
            unit=unit))

    res = DataFrame.from_dict(res)
    
    if not has_unit :
        res = res.drop(columns="unit")

    if len(res) > 0 :
        res = res.set_index("name")

    return res



def compute_impacts(
        models, 
        methods,
        functional_unit=1,
        extract_activities:List[Activity]=None,
        axis=None,
        **params):
    """
    Main parametric LCIA method : Computes LCA by expressing the foreground model as symbolic expression of background activities and parameters.
    Then, compute 'static' inventory of the referenced background activities.
    This enables a very fast recomputation of LCA with different parameters, useful for stochastic evaluation of parametrized model

    Parameters
    ----------
    models :
        Single model or
        List of model or
        List of (model, alpha)
        or Dict of model:amount
        In case of several models, you cannot use list of parameters
    methods : List of methods / impacts to consider
    extract_activities : Optionnal : list of foregound or background activities. If provided, the result only integrate their contribution
    params : You should provide named values of all the parameters declared in the model. \
             Values can be single value or list of samples, all of the same size
    axis: Designates the name of an attribute of user activities to split impacts by their value. This is usefull to get impact by phase or sub modules
    """
    dfs = dict()

    if isinstance(models, list):
        def to_tuple(item) :
            if isinstance(item, tuple) :
                return item
            else:
                return (item, 1)
        models = dict(to_tuple(item) for item in models)
    elif not isinstance(models, dict):
        models = {models:1}

    for model, alpha in models.items():

        if type(model) is tuple:
            model, alpha = model

        dbname = model.key[0]
        with DbContext(dbname):

            # Check no params are passed for FixedParams
            for key in params:
                if key in _fixed_params() :
                    error("Param '%s' is marked as FIXED, but passed in parameters : ignored" % key)


            lambdas = _preMultiLCAAlgebric(model, methods, extract_activities=extract_activities, axis=axis)

            if functional_unit != 1 :
                alpha = alpha / compute_value(functional_unit, **params)

            df = _postMultiLCAAlgebric(methods, lambdas, alpha=alpha, **params)

            model_name = _actName(model)
            while model_name in dfs :
                model_name += "'"

            # param with several values
            list_params = {k: vals for k, vals in params.items() if isinstance(vals, list)}

            # Shapes the output / index according to the axis or multi param entry
            if axis :
                df[axis] = lambdas[0].axis_keys
                df = df.set_index(axis)
                df.index.set_names([axis])

                # Filter out line with zero output
                df = df.loc[
                    df.apply(
                        lambda row: not (row.name is None and row.values[0] == 0.0),
                        axis=1)]

                # Rename "None" to others
                df = df.rename(index={None: "*other*"})

                # Add "total" line
                df.loc['Total'] = df.sum(numeric_only=True)


            elif len(list_params) > 0:
                for k, vals in list_params.items():
                    df[k] = vals
                df = df.set_index(list(list_params.keys()))

            else :
                # Single output ? => give the single row the name of the model activity
                df = df.rename(index={0: model_name})

            dfs[model_name] = df

    if len(dfs) == 1:
        df = list(dfs.values())[0]
        return df
    else:
        # Concat several dataframes for several models
        return pd.concat(list(dfs.values()))


def list_parameters_as_df(name_type=NameType.NAME):

    """ Print a pretty list of all defined parameters """
    params = [dict(
        group=param.group or "",
        name=_param_name(param, name_type),
        label=param.get_label(),
        default=param.default,
        min=param.min,
        max=param.max,
        std=getattr(param, "std", None),
        distrib=param.distrib,
        unit=param.unit,
        db=param.dbname or "[project]") for  param in _param_registry().all()]

    groups = list({p["group"] for p in params})
    groups = sorted(groups)

    # Sort by Group / name
    def keyf(param) :
        return (groups.index(param["group"]), param["name"])

    sorted_params = sorted(params, key=keyf)

    return pd.DataFrame(sorted_params)


def export_data_to_excel_0(list_df_to_export, xlsx_file_name):
    """Export dataframe to excel files, each dataframe in an excel sheet"""
    # list_df_to_export is a list of ["name", df]
    # df is the dataframe to be exported, "name" is the name of the sheet in the excel file
    # xlsx_file_name is the name of the excel file. It shall end with .xlsx
    with pd.ExcelWriter(xlsx_file_name,engine="xlsxwriter") as writer:
        for [name,df] in list_df_to_export:
            df.to_excel(writer,sheet_name=name)


def export_data_to_excel(list_df_to_export, xlsx_file_name):
    """Export dataframe to excel files in several excel sheet"""
    # list_df_to_export is a list that looks like ["name", df1, df2, df3...]
    # "name" is the name of the sheet in the excel file where df1, df2, df3 will be exporter
    # df1, df2, df3 are the dataframe to be exported in the same excel sheet. 
    # xlsx_file_name is the name of the excel file. It shall end with .xlsx
    with pd.ExcelWriter(xlsx_file_name,engine="xlsxwriter") as writer:
        for list_name_tables in list_df_to_export:
            if len(list_name_tables)==2:
                list_name_tables[1].to_excel(writer,sheet_name=list_name_tables[0])
                #list_name_tables[1] = df, list_name_tables[0]=sheet_name
            elif len(list_name_tables)>2:
                a=0
                for i in range((len(list_name_tables)-1)):
                    list_name_tables[i+1].to_excel(writer,sheet_name=list_name_tables[0],startcol=0,startrow=a,header=True,index=True)
                    a=a+len(list_name_tables[i+1].index)+2

