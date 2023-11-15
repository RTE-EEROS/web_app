from collections import defaultdict
from typing import Dict, Union, List
import streamlit as st

def group_params(params) :
    groups = defaultdict(list)

    for param in params:
        groups[param.group].append(param)
    return groups

def select_dict(label, options:Union[Dict, List], default=None, **kwargs) :
    """Select box taking dict of key=>label as option"""

    if isinstance(options, list):
        options = {val:val for val in options}


    keys = list(options.keys())
    default_index = keys.index(default) if default in keys else 0

    res = st.selectbox(
        label=label,
        options=options.items(),
        index=default_index,
        format_func = lambda x : x[1],
        **kwargs)

    return res[0]



