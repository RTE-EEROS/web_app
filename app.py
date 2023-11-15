#!/usr/bin/env python

import streamlit as st
from lib.common import Model


IN_FILE = "model.json"

@st.cache_resource()
def load_model():
    return Model.from_file(IN_FILE)

model = load_model()

with st.sidebar:

    st.header('Settings')

    st.selectbox("Impact category", options=model.impacts.values())

    st.header("Parameters")

    param_values = dict()
    for key, param in model.params.items():

        #st.text(param.name, help=param.label)

        if param.type == "bool" :

            param_values[key] = st.checkbox(
                key=param.name,
                label=param.name,
                help=param.label,
                value=param.default)

        elif param.type == "enum" :

            default_index = param.values.index(param.default) if param.default in param.values else None

            param_values[key] = st.selectbox(
                label=param.name,
                help=param.label,
                key=param.name,
                options=param.values,
                index=default_index)

        else:

            param_values[key] = st.slider(
                key=param.name,
                label=param.name,
                help=param.label,
                min_value=float(param.min),
                max_value=float(param.max),
                value=param.default)




# Read header from 'static/header.md'
with open("static/header.md", "r") as f:
    st.markdown(f.read())

st.header("Results")
st.metric(label="CO2", value="12 gCO2/kWh")

st.json(param_values)





