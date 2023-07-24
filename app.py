import time

import dash
from dash import dcc
from dash import html
import numpy as np
from dash.dependencies import Input, Output, State
import json
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


import utils.dash_reusable_components as drc
import utils.figures as figs
import utils.bmex as bmex
from utils.bmex_views import *
import utils.views_class as views
import utils.gpe as gpe
import utils.rbm as rbm

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import random as rand
import h5py
import base64, io
import re
import base64

TAB_STYLE = {
    'width': '72px',
    'border': 'none',
    #'boxShadow': 'inset 0px -1px 0px 0px lightgrey',
    'background': '#a5b1cd',
    'paddingTop': 0,
    'paddingBottom': 0,
    'height': '60px',
    'font-size': 32,
    'color': '#282b38',
    'borderTop': '3px  #ffffff solid',
}

SELECTED_STYLE = {
    'width': '72px',
    'boxShadow': 'none',
    'borderLeft': '3px #ffffff solid',
    'borderRight': '3px #282b38 solid',
    'borderTop': '3px #ffffff solid',
    'borderBottom': '3px #282b38 solid',
    'background': '#a5b1cd',
    'paddingTop': 0,
    'paddingBottom': 0,
    'height': '60px',
    'font-size': 32,
    'color': '#282b38'
}

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

app.config.suppress_callback_exceptions=True

app.title = "Bayesian Mass Explorer"

server = app.server

app.layout = html.Div(
    children=[
        dcc.Location(id='url', refresh=False),
        # .container class is fixed, .container.scalable is scalable
        html.Div(
            className="banner",
            children=[
                # Change App Name here
                html.Div(
                    className="container scalable",
                    children=[
                        # Change App Name here
                        html.H2(
                            id="banner-title",
                            children=[
                                html.A(
                            id="banner-logo",
                            children=[
                                html.Img(src=app.get_asset_url("BMEX-logo-3.png"))
                            ],
                            href="https://bmex.dev",
                        )
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(id='page-content'),
        dcc.Store(id='intermediate-value'),
        dcc.Store(id='nextgraphid', data=2),
        dcc.Store(id='viewsmemory', storage_type='memory',
        data=json.dumps([{"graphstyle": 'landscape', "quantity": 'BE', "dataset": 'EXP', "colorbar": 'linear', "wigner": 0, "id": 1, 
        "ZRange": {"zmin": None, "zmax": None, "protons": 40}, "NRange": {"nmin": None, "nmax": None, "neutrons": 40}}]),
        ),
        dcc.Store(id='triggerGraph', data=json.dumps("update")),
    ]
)

@app.callback(
    Output('page-content','children'),
    [Input('url','pathname')]
    )
def display_page(pathname):
    if(pathname == "/emulator"):
        out = emu_view()
    else:
        out = html.Div(
            id="body",
            className="container scalable",
            children=[html.P("How did you get here? Click the banner to make it back to safety!")])
    return out

# @app.callback(
#     [
#         Output(component_id='dropdown-select-quantity', component_property='options'),
#         #Output(component_id='dropdown-select-quantity', component_property='value'),
#         Output(component_id='protons-card', component_property='style'),
#         Output(component_id='neutrons-card', component_property='style'),
#         # Output(component_id='zmin-card', component_property='style'),
#         # Output(component_id='zmax-card', component_property='style'),
#         # Output(component_id='nmin-card', component_property='style'),
#         # Output(component_id='nmax-card', component_property='style'),
#         Output(component_id='colorbar-card', component_property='style'),
#         Output(component_id='Wigner-card', component_property='style'),
#     ],
#     [
#         Input(component_id='dropdown-iso-chain', component_property='value'),
#         Input('url','pathname'),
#     ]
# )
# def quantity_options(is_chain,url):
#     show = {'display': 'block'}
#     hide = {'display': 'none'}
#     if url == "/masses":
#         if is_chain == 'single':
#             return [[
#                 # Options for Dropdown
#                 {"label": "All", "value": "All"},
#                 {"label": "Binding Energy", "value": "BE"},
#                 {"label": "One Neutron Separation Energy", "value": "OneNSE",},
#                 {"label": "One Proton Separation Energy", "value": "OnePSE",},
#                 {"label": "Two Neutron Separation Energy", "value": "TwoNSE",},
#                 {"label": "Two Proton Separation Energy", "value": "TwoPSE",},
#                 {"label": "Alpha Separation Energy", "value": "AlphaSE",},
#                 {"label": "Two Proton Shell Gap", "value": "TwoNSGap",},
#                 {"label": "Two Neutron Shell Gap", "value": "TwoPSGap",},
#                 {"label": "Double Mass Difference", "value": "DoubleMDiff",},
#                 {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED",},
#                 {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED",},
#                 {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting",},
#                 {"label": "Single-Proton Energy Splitting", "value": "SPESplitting",},
#                 {"label": "Wigner Energy Coefficient", "value": "WignerEC",},
#             ],
#             # Default Value
#             #"All",
#             # Proton Box Visibility
#             show,
#             # Neutron Box Visibility
#             show,
#             # # Zmin Visibility
#             # hide,
#             # # Zmax Visibility
#             # hide,
#             # # Nmin Visibility
#             # hide,
#             # # Nmax Visibility
#             # hide,
#             # Colorbar Visibility
#             hide,
#             # Wigner Visibility
#             hide,
#             ]
#         elif is_chain == 'isotopic':
#             return [[
#                     {"label": "Binding Energy", "value": "BE"},
#                     {"label": "One Neutron Separation Energy", "value": "OneNSE",},
#                     {"label": "One Proton Separation Energy", "value": "OnePSE",},
#                     {"label": "Two Neutron Separation Energy", "value": "TwoNSE",},
#                     {"label": "Two Proton Separation Energy", "value": "TwoPSE",},
#                     {"label": "Alpha Separation Energy", "value": "AlphaSE",},
#                     {"label": "Two Proton Shell Gap", "value": "TwoNSGap",},
#                     {"label": "Two Neutron Shell Gap", "value": "TwoPSGap",},
#                     {"label": "Double Mass Difference", "value": "DoubleMDiff",},
#                     {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED",},
#                     {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED",},
#                     {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting",},
#                     {"label": "Single-Proton Energy Splitting", "value": "SPESplitting",},
#                     {"label": "Wigner Energy Coefficient", "value": "WignerEC",},
#             ],
#             # Default Value
#             #"BE",
#             # Proton Box Visibility
#             show,
#             # Neutron Box Visibility
#             hide,
#             # # Zmin Visibility
#             # hide,
#             # # Zmax Visibility
#             # hide,
#             # # Nmin Visibility
#             # show,
#             # # Nmax Visibility
#             # show,
#             # Colorbar Visibility
#             hide,
#             # Wigner Visibility
#             hide,
#             ]
#         elif is_chain == 'isotonic':
#             return [[
#                     {"label": "Binding Energy", "value": "BE"},
#                     {"label": "One Neutron Separation Energy", "value": "OneNSE",},
#                     {"label": "One Proton Separation Energy", "value": "OnePSE",},
#                     {"label": "Two Neutron Separation Energy", "value": "TwoNSE",},
#                     {"label": "Two Proton Separation Energy", "value": "TwoPSE",},
#                     {"label": "Alpha Separation Energy", "value": "AlphaSE",},
#                     {"label": "Two Proton Shell Gap", "value": "TwoNSGap",},
#                     {"label": "Two Neutron Shell Gap", "value": "TwoPSGap",},
#                     {"label": "Double Mass Difference", "value": "DoubleMDiff",},
#                     {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED",},
#                     {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED",},
#                     {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting",},
#                     {"label": "Single-Proton Energy Splitting", "value": "SPESplitting",},
#                     {"label": "Wigner Energy Coefficient", "value": "WignerEC",},
#             ],
#             # Default Value
#             #"BE",
#             # Proton Box Visibility
#             hide,
#             # Neutron Box Visibility
#             show,
#             # # Zmin Visibility
#             # show,
#             # # Zmax Visibility
#             # show,
#             # # Nmin Visibility
#             # hide,
#             # # Nmax Visibility
#             # hide,
#             # Colorbar Visibility
#             hide,
#             # Wigner Visibility
#             hide,           
#             ]
#         elif is_chain == 'landscape':
#             return [[
#                     {"label": "Binding Energy", "value": "BE"},
#                     {"label": "One Neutron Separation Energy", "value": "OneNSE",},
#                     {"label": "One Proton Separation Energy", "value": "OnePSE",},
#                     {"label": "Two Neutron Separation Energy", "value": "TwoNSE",},
#                     {"label": "Two Proton Separation Energy", "value": "TwoPSE",},
#                     {"label": "Alpha Separation Energy", "value": "AlphaSE",},
#                     {"label": "Two Proton Shell Gap", "value": "TwoNSGap",},
#                     {"label": "Two Neutron Shell Gap", "value": "TwoPSGap",},
#                     {"label": "Double Mass Difference", "value": "DoubleMDiff",},
#                     {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED",},
#                     {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED",},
#                     {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting",},
#                     {"label": "Single-Proton Energy Splitting", "value": "SPESplitting",},
#                     {"label": "Wigner Energy Coefficient", "value": "WignerEC",},
#                     {"label": "Quad Def Beta2", "value": "QDB2t",},
#             ],
#             # Default Value
#             #"BE",
#             # Proton Box Visibility
#             hide,
#             # Neutron Box Visibility
#             hide,
#             # # Zmin Visibility
#             # hide,
#             # # Zmax Visibility
#             # hide,
#             # # Nmin Visibility
#             # hide,
#             # # Nmax Visibility
#             # hide,
#             # Colorbar Visibility
#             show,
#             # Wigner Visibility
#             show,
#             ]            
#     elif url == "/gpe":
#         if is_chain == 'single':
#             return [[
#                 # Options for Dropdown
#                 #{"label": "All", "value": "All"},
#                 #{"label": "Binding Energy", "value": "BE"},
#                 #{"label": "One Neutron Separation Energy", "value": "OneNSE",},
#                 #{"label": "One Proton Separation Energy", "value": "OnePSE",},
#                 {"label": "Two Neutron Separation Energy", "value": "TwoNSE",},
#                 # {"label": "Two Proton Separation Energy", "value": "TwoPSE",},
#                 # {"label": "Alpha Separation Energy", "value": "AlphaSE",},
#                 # {"label": "Two Proton Shell Gap", "value": "TwoNSGap",},
#                 # {"label": "Two Neutron Shell Gap", "value": "TwoPSGap",},
#                 # {"label": "Double Mass Difference", "value": "DoubleMDiff",},
#                 # {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED",},
#                 # {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED",},
#                 # {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting",},
#                 # {"label": "Single-Proton Energy Splitting", "value": "SPESplitting",},
#                 # {"label": "Wigner Energy Coefficient", "value": "WignerEC",},
#             ],
#             # Default Value
#             #"TwoNSE",
#             # Proton Box Visibility
#             show,
#             # Neutron Box Visibility
#             show,
#             # Zmin Visibility
#             hide,
#             # Zmax Visibility
#             hide,
#             # Nmin Visibility
#             hide,
#             # Nmax Visibility
#             hide,
#             ]
#         elif is_chain == 'isotopic':
#             return [[
#                     # {"label": "Binding Energy", "value": "BE"},
#                     # {"label": "One Neutron Separation Energy", "value": "OneNSE",},
#                     # {"label": "One Proton Separation Energy", "value": "OnePSE",},
#                     {"label": "Two Neutron Separation Energy", "value": "TwoNSE",},
#                     # {"label": "Two Proton Separation Energy", "value": "TwoPSE",},
#                     # {"label": "Alpha Separation Energy", "value": "AlphaSE",},
#                     # {"label": "Two Proton Shell Gap", "value": "TwoNSGap",},
#                     # {"label": "Two Neutron Shell Gap", "value": "TwoPSGap",},
#                     # {"label": "Double Mass Difference", "value": "DoubleMDiff",},
#                     # {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED",},
#                     # {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED",},
#                     # {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting",},
#                     # {"label": "Single-Proton Energy Splitting", "value": "SPESplitting",},
#                     # {"label": "Wigner Energy Coefficient", "value": "WignerEC",},
#             ],
#             # Default Value
#             #"TwoNSE",
#             # Proton Box Visibility
#             show,
#             # Neutron Box Visibility
#             hide,
#             # Zmin Visibility
#             hide,
#             # Zmax Visibility
#             hide,
#             # Nmin Visibility
#             hide,
#             # Nmax Visibility
#             hide,
#             ]
#         elif is_chain == 'isotonic':
#             return [[
#                     # {"label": "Binding Energy", "value": "BE"},
#                     # {"label": "One Neutron Separation Energy", "value": "OneNSE",},
#                     # {"label": "One Proton Separation Energy", "value": "OnePSE",},
#                     {"label": "Two Neutron Separation Energy", "value": "TwoNSE",},
#                     # {"label": "Two Proton Separation Energy", "value": "TwoPSE",},
#                     # {"label": "Alpha Separation Energy", "value": "AlphaSE",},
#                     # {"label": "Two Proton Shell Gap", "value": "TwoNSGap",},
#                     # {"label": "Two Neutron Shell Gap", "value": "TwoPSGap",},
#                     # {"label": "Double Mass Difference", "value": "DoubleMDiff",},
#                     # {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED",},
#                     # {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED",},
#                     # {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting",},
#                     # {"label": "Single-Proton Energy Splitting", "value": "SPESplitting",},
#                     # {"label": "Wigner Energy Coefficient", "value": "WignerEC",},
#             ],
#             # Default Value
#             #"TwoNSE",
#             # Proton Box Visibility
#             hide,
#             # Neutron Box Visibility
#             show,
#             # Zmin Visibility
#             show,
#             # Zmax Visibility
#             show,
#             # Nmin Visibility
#             hide,
#             # Nmax Visibility
#             hide,
#             ]

@app.callback(
    Output("div-emu", "children"),
    [
        Input("dropdown-select-dataset", "value"),
        Input("dropdown-nuc","value"),
        [Input("Msigma","value"),Input("Rho","value"),Input("BE","value"),\
         Input("Mstar","value"),Input("K","value"),Input("zeta","value"),\
         Input("J","value"),Input("L","value"),],
    ],
)
def main_output_emu(
    dataset,
    nuc,
    NMP,
):
    np.set_printoptions(precision=5)
    nuc_dict={'16O':0,'40Ca':1,'48Ca':2,'68Ni':3,'90Zr':4,'100Sn':5,'116Sn':6,'132Sn':7,'144Sm':8,'208Pb':9}
    if(None in NMP):
        return [
            html.Div(
                #id="svm-graph-container",
                children=[
                    html.P("Welcome to BMEX! Please input your requested nuclear matter properties on the left!"),
                ],
                style={'font-size':'3rem'},
            ),
        ]
    elif(dataset == "rmf"):
        all_eval = []
        energy, protrad, timing = rbm.rbm_emulator(nuc_dict[nuc],NMP)

        all_eval.append(html.P(nuc+" Emulator Results:"))
        all_eval.append(html.P("Binding Energy: {:.2f} MeV".format(energy)))
        all_eval.append(html.P("Charge Radius:  {:.2f} fm".format(protrad)))
        all_eval.append(html.P("Emulation time: {:.3f} s".format(timing)))

        return [
            html.Div(
                #id="svm-graph-container",
                children=all_eval,
                style={'font-size':'3rem'},
            ),
        ]


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
