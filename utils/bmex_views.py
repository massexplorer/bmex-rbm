from dash import dcc
from dash import html
import utils.dash_reusable_components as drc


def emu_view():
    return html.Div(
        id="body",
        className="container scalable",
        children=[
            html.Div(
                id="app-container",
                # className="row",
                children=[
                    html.Div(
                        # className="three columns",
                        id="left-column",
                        children=[
                            drc.Card(
                                id="first-card",
                                children=[
                                    drc.NamedDropdown(
                                        name="Compute For",
                                        id="dropdown-nuc",
                                        options=[
                                            {"label": "16O", "value": "16O"},
                                            {"label": "40Ca", "value": "40Ca"},
                                            {"label": "48Ca", "value": "48Ca"},
                                            {"label": "68Ni", "value": "68Ni"},
                                            {"label": "90Zr", "value": "90Zr"},
                                            {"label": "100Sn", "value": "100Sn"},
                                            {"label": "116Sn", "value": "116Sn"},
                                            {"label": "132Sn", "value": "132Sn"},
                                            {"label": "144Sm", "value": "144Sm"},
                                            {"label": "208Pb", "value": "208Pb"},
                                        ],
                                        clearable=False,
                                        searchable=False,
                                        value="16O",
                                    ),
                                ]
                            ),
                            drc.Card(
                                id="data-card",
                                children=[
                                    drc.NamedDropdown(
                                        name="Select Model",
                                        id="dropdown-select-dataset",
                                        options=[
                                            {"label": "Covariant EDF", "value": "rmf"},
                                            #{"label": "SkMs", "value": "SkMs"},
                                        ],
                                        clearable=False,
                                        searchable=False,
                                        value="rmf",
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="msigma-card",
                                children=[
                                    drc.NamedInput(
                                        name="Mass of Sigma Meson",
                                        id="Msigma",
                                        type="number",
                                        min=480,
                                        max=505,
                                        # step=1,
                                        placeholder=488.0,
                                        value=488.0,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="rho-card",
                                children=[
                                    drc.NamedInput(
                                        name="Saturation Density",
                                        id="Rho",
                                        type="number",
                                        min=0.147,
                                        max=0.159,
                                        # step=1,
                                        placeholder=0.151,
                                        value=0.151,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="e-card",
                                children=[
                                    drc.NamedInput(
                                        name="BE at Saturation",
                                        id="BE",
                                        type="number",
                                        min=-16.50,
                                        max=-16.00,
                                        # step=1,
                                        placeholder=-16.35,
                                        value=-16.35,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="mstar-card",
                                children=[
                                    drc.NamedInput(
                                        name="Effective Nucleon Mass",
                                        id="Mstar",
                                        type="number",
                                        min=0.55,
                                        max=0.62,
                                        # step=1,
                                        placeholder=0.59,
                                        value=0.59,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),                            
                            drc.Card(
                                id="k-card",
                                children=[
                                    drc.NamedInput(
                                        name="Incompressibility Coefficient (K)",
                                        id="K",
                                        type="number",
                                        min=200,
                                        max=255,
                                        # step=1,
                                        placeholder=225.0,
                                        value=225.0,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="j-card",
                                children=[
                                    drc.NamedInput(
                                        name="Symmetry Energy (J)",
                                        id="J",
                                        type="number",
                                        min=30,
                                        max=42,
                                        # step=1,
                                        placeholder=36.0,
                                        value=36.0,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="l-card",
                                children=[
                                    drc.NamedInput(
                                        name="Slope of Symmetry Energy (L)",
                                        id="L",
                                        type="number",
                                        min=50,
                                        max=200,
                                        # step=1,
                                        placeholder=80.0,
                                        value=80.0,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                            drc.Card(
                                id="zeta-card",
                                children=[
                                    drc.NamedInput(
                                        name="Quartic Vector Coupling",
                                        id="zeta",
                                        type="number",
                                        min=0.0,
                                        max=0.06,
                                        # step=1,
                                        placeholder=0.04,
                                        value=0.04,
                                        style={'width':'100%'},
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        id="div-emu",
                        children=[
                            dcc.Graph(
                                id="graph-sklearn-svm",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                    )
                                ),
                            ),
                        ],
                    ),
                ],
            )
        ],
    )

