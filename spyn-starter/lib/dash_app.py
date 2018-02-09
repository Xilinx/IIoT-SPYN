#   Copyright (c) 2018, Xilinx, Inc.
#   All rights reserved.
# 
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


__author__ = "KV Thanjavur Bhaaskar & Naveen Purushotham"
__copyright__ = "Copyright 2018, Xilinx"
__email__ = "kvt@xilinx.com & npurusho@xilinx.com"

import dash
from IPython import display


def show_app(app,  # type: dash.Dash
             port=9999,
             width=900,
             height=600,
             offline=True,
             style=True,
             **dash_flask_kwargs):
    """
    Run the application inside a Jupyter notebook and show an iframe with it
    :param app:
    :param port:
    :param width:
    :param height:
    :param offline:
    :return:
    """
    #     url = 'http://npurusho_pynq:%d' % port
    #     url = 'http://172.19.73.205:%d' % port
    url = 'http://192.168.2.99:%d' % port
    iframe = '<iframe src="{url}" width={width} height={height}></iframe>' \
             ''.format(
        url=url,
        width=width,
        height=height)
    display.display_html(iframe, raw=True)
    if offline:
        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
    if style:
        external_css = [
            "https://fonts.googleapis.com/css?family=Raleway:400,300,600",
            "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-"
            "awesome.min.css",
            "http://getbootstrap.com/dist/css/bootstrap.min.css", ]

        for css in external_css:
            app.css.append_css({"external_url": css})

        external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
                       "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a34"
                       "01de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-"
                       "sachs-report-js.js",
                       "http://getbootstrap.com/dist/js/bootstrap.min.js"]

        for js in external_js:
            app.scripts.append_script({"external_url": js})

    return app.run_server(debug=False,  # needs to be false in Jupyter
                          port=port,
                          host="0.0.0.0",
                          **dash_flask_kwargs)


import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import numpy as np
random_x = range(0, 999, 1)
random_x = list(random_x)

app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Markdown(children='# SPYN-Starter '),
    dcc.Markdown(children='## `EDDP Web Application Demo using PYNQ`'),

    dcc.Markdown(children='### `Set Mode`'),

    dcc.Dropdown(
        options=[
            {'label': 'Current', 'value': 'Current'},
            {'label': 'Speed', 'value': 'Speed'}
        ],
        value='Speed'
    ),

    dcc.Markdown(children='### `Set Direction`'),

    dcc.RadioItems(
        options=[
            {'label': 'Reverse', 'value': 'Reverse'},
            {'label': 'Forward', 'value': 'Forward'}
        ],
        value='Forward'
    ),

    dcc.Markdown(children='### `RPM Slider`'),

    html.Label('RPM'),
    dcc.Slider(
        min=-4000,
        max=4000,
        value=0,
    ),

    dcc.Markdown(children='### `Torque Slider`'),

    html.Label('Torque'),
    dcc.Slider(
        min=-400,
        max=400,
        value=0,
    ),

    dcc.Graph(
        id='Ia vs Ib',
        figure={
            'data': [
                go.Scatter(
                    x=df['Ia'][63000:63999],
                    y=df['Ib'][63000:63999],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.items()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Current Ia'},
                yaxis={'title': 'Current Ib'},
                margin={'l': 80, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    dcc.Markdown(children='### `Current Ia`'),

    dcc.Graph(
        id='Ia',
        figure={
            'data': [
                go.Scatter(
                    x=random_x,
                    y=df['Ia'][63000:63999],
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                ) for i in df.items()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Sample'},
                yaxis={'title': 'Current Ia'},
                margin={'l': 80, 'b': 40, 't': 10, 'r': 10},
                hovermode='closest'
            )
        }
    ),

    dcc.Markdown(children='### `Current Ib`'),

    dcc.Graph(
        id='Ib',
        figure={
            'data': [
                go.Scatter(
                    x=random_x,
                    y=df['Ib'][63000:63999],
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                ) for i in df.items()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Samples'},
                yaxis={'title': 'Current Ib'},
                margin={'l': 80, 'b': 40, 't': 10, 'r': 10},
                hovermode='closest'
            )
        }
    ),

    dcc.Markdown(children='### `Angle`'),

    dcc.Graph(
        id='Angle',
        figure={
            'data': [
                go.Scatter(
                    x=random_x,
                    y=df['angle'][63000:63999],
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                ) for i in df.items()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Samples'},
                yaxis={'title': 'angle'},
                margin={'l': 80, 'b': 40, 't': 10, 'r': 10},
                hovermode='closest'
            )
        }
    ),

    dcc.Markdown(children='### `RPM`'),

    dcc.Graph(
        id='RPM',
        figure={
            'data': [
                go.Scatter(
                    x=random_x,
                    y=df['rpm'][63000:63999],
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                ) for i in df.items()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Samples'},
                yaxis={'title': 'Speed'},
                margin={'l': 80, 'b': 40, 't': 10, 'r': 10},
                hovermode='closest'
            )
        }
    )
], style={'columnCount': 1})