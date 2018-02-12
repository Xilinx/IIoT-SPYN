import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os

from flask import send_from_directory

import numpy as np
random_x = range(0, 999, 1)
random_x = list(random_x)

app = dash.Dash()
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='/static/stylesheet.css'
    ),        
    html.Div([ 
    html.H1('SPYN-Starter'),
    html.Img(src="http://lh3.googleusercontent.com/GBSzZyiMvimaw7oytvVmgN_R2VnGKa5dmCrofqb6HIcGxMqtLbQWSDGOjg7eWUjGuIBo23xRMM8ODMKJztYoyXPMzw=s293")], className='banner'),
    dcc.Markdown(children='## `EDDP Web Application Demo using PYNQ`'),
    
    html.Div([
    dcc.Markdown(children='### `Set Mode`'),

    dcc.Dropdown(
        id='modes-dropdown',
        options=[
            {'label': 'Current', 'value': 'Current'},
            {'label': 'Speed', 'value': 'Speed'}
        ],
        value='Speed'
    ),
    html.Div(id='modes')
    ], className='mode_row', style={'margin-bottom': '10px'}),
    
    
    dcc.Markdown(children='### `Motor ON/OFF`'),    
    html.Button('ON/OFF', id='button'),
    html.Div(id='motor-button'),
    
    html.Div([
    dcc.Markdown(children='### `RPM Slider`'),

    html.Label('RPM'),
    dcc.Slider(
        id='rpm-slider',
        min=-4000,
        max=4000,
        value=0,
        marks={0: 'Reverse          <=== Direction ===>          Forward',
              3900: '4000',
              -3900: '-4000'}
    ),
    dcc.Markdown(children='Motor Speed'),
    html.Div(id='rpm-slide')
    ], className='rpm_row', style={'margin-bottom': '10px'}),
    
    dcc.Markdown(children='### `Torque Slider`'),

    html.Label('Torque'),
    dcc.Slider(
        min=-400,
        max=400,
        value=0,
        marks={0: 'Reverse          <=== Direction ===>          Forward',
              390: '400',
              -390: '-400'},
    )], style={'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "1200px",
          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})

@app.callback(
     dash.dependencies.Output('motor-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks%2==0:
        motor.set_mode('rpm_mode')
        motor.set_rpm(0)
        return 'The Motor is OFF'
    else:
        motor.set_mode('rpm_mode')
        motor.set_rpm(0)
        return 'The Motor is ON'

@app.callback(
    dash.dependencies.Output('modes', 'children'),
    [dash.dependencies.Input('modes-dropdown', 'value')])
def set_mode_dropdown(available_options):
    print(available_options)
    motor.set_mode[available_options]
    return f'The Motor is set to {available_options} mode'
    
@app.callback(
     dash.dependencies.Output(component_id='rpm-slide', component_property='children'),
    [dash.dependencies.Input(component_id='rpm-slider', component_property='value')])
def update_rpm(sliderValue):
        motor.set_mode('rpm_mode')
        motor.set_rpm(sliderValue)
        return f'The Motor is set to {sliderValue} RPM'

@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)