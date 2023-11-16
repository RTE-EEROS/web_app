#!/usr/bin/env python

import streamlit as st
from lib.common import Model
from lib.app_utils import group_params, select_dict

from lib.settings import settings, OUTFILE
import plotly.express as px
from tornado.web import RequestHandler
from lib.api import setup_api_handler

CSS_FILE = "static/style.css"

def init_app():

    st.set_page_config(
        page_title=settings.title,
        page_icon=settings.icon)
    st.title(settings.title)

    @st.cache_resource()
    def load_model():
        return Model.from_file(OUTFILE)

    # Load CSS within page
    with open(CSS_FILE, 'r') as f:
        css = f.read()
        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True)

    # Setup API
    class HelloHandler(RequestHandler):
        def get(self):
            self.write({'message': 'hello world'})

    setup_api_handler('/api/hello', HelloHandler)


    # Load model once
    return load_model()

def display_settings(model):

    st.header('Settings')

    # Selection of impact
    impact = select_dict("Impact category", options=list(model.impacts.keys()))

    # Selection of functional units
    fu_options = {key: "%s %s" % (key, "[%s]" % fu.unit if fu.unit else "") for key, fu in model.functional_units.items()}
    functional_unit = select_dict("Functional unit", options=fu_options)

    return impact, functional_unit

def display_params(model):
    """ Display params and return current values """

    st.header("Parameters")

    param_groups = group_params(model.params.values())

    # Gather param values by name
    param_values = dict()

    first_group = True
    for group_name, params in param_groups.items():

        expander = st.expander(group_name, expanded=first_group) if group_name else None
        first_group = False

        with expander :

            for param in params:

                param_label = param.name
                if param.unit :
                    param_label += " [%s]" % param.unit

                if param.type == "bool" :

                    param_values[param.name] = st.checkbox(
                        key=param.name,
                        label=param_label,
                        help=param.label,
                        value=param.default)

                elif param.type == "enum" :

                    default_index = param.values.index(param.default) if param.default in param.values else None

                    param_values[param.name] = st.selectbox(
                        label=param_label,
                        help=param.label,
                        key=param.name,
                        options=param.values,
                        index=default_index)

                else:

                    param_values[param.name] = st.slider(
                        key=param.name,
                        label=param_label,
                        help=param.label,
                        min_value=float(param.min),
                        max_value=float(param.max),
                        value=param.default)
    return param_values


def display_header():
    # Read header from 'static/header.md'
    with open("static/header.md", "r") as f:
        st.markdown(f.read())

def display_results(model, impact, functional_unit, param_values):

    st.header("📊 Results")

    val, unit = model.evaluate(
            impact = impact,
            functional_unit=functional_unit,
            axis="total",
            **param_values)

    # Total impacts
    st.subheader("Total")
    st.markdown("Total impact for *%s* by functional unit *%s*" % (impact, functional_unit))

    st.metric(label=impact, value="%.3g [%s]" % (val, unit))

    # Impact by axes
    for axis in settings.axes:
        if axis is None :
            continue

        st.subheader("Axis : %s" % axis)

        st.markdown("Impact for *%s* by functional unit *%s*, splitted by *%s*" % (impact, functional_unit, axis))
        res, unit = model.evaluate(
            impact=impact,
            functional_unit=functional_unit,
            axis=axis,
            **param_values)

        # Cleanup
        res = dict(sorted(res.items()))
        for key in [None, "null"] :
            if key in res:
                del res[key]

        # Prepare for plotly
        data = dict(
            key=list(res.keys()),
            val=list(res.values()))

        # Display chart
        st.plotly_chart(px.bar(
            data,
            x="key",
            y="val",
            labels=dict(
                key=axis,
                val="%s [%s]" % (impact, unit)
            )))



def main():

    model = init_app()

    with st.sidebar:

        impact, functional_unit = display_settings(model)

        param_values = display_params(model)

    display_header()

    display_results(model, impact, functional_unit, param_values)


main()

