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

__author__ = "Naveen Purushotham, KV Thanjavur Bhaaskar"
__copyright__ = "Copyright 2018, Xilinx"
__email__ = "npurusho@xilinx.com, kvt@xilinx.com"

import pandas as pd
import time
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os
from pynq import Overlay
from pynq import MMIO
import numpy as np
from spyn.lib import *
from pynq import Xlnk
from flask import send_from_directory
from dash.dependencies import Input, Output, State

overlay = Overlay(
    "/usr/local/lib/python3.6/dist-packages/spyn/overlays/spyn.bit")
overlay.download()

motor = Motor_Controller()

app = dash.Dash()

app.layout = html.Div(
    style={'color': 'Black',
           'background-color': 'rgb(254, 254, 254)',
           'padding': '10px 10px 10px 10px',
           'marginLeft': 'auto',
           'marginRight': 'auto',
           "width": "1000px",
           'boxShadow': '0px 0px 5px 5px rgba(240,89,131,0.4)'},
    children=[
        html.Div([
            html.Img(
                src="http://lh3.googleusercontent.com/GBSzZyiMvimaw7oytvVmgN_R"
                    "2VnGKa5dmCrofqb6HIcGxMqtLbQWSDGOjg7eWUjGuIBo23xRMM8ODMKJz"
                    "tYoyXPMzw=s293",
                style={
                    'float': 'right',
                    'padding': '5px 5px 5px 5px',
                    'position': 'relative',
                })]),
        html.Div(
            style={"width": "500px"},
            children=[
                html.Div([
                    html.H1('SPYN-Starter'),
                    dcc.Markdown(
                        children='## `EDDP Web Application Demo using PYNQ`')],
                    style={'text-align': 'left',
                           'padding': '10px 0px 0px 0px'}),
                html.Div([
                    dcc.Markdown(children='### `Set Mode`'),
                    dcc.Dropdown(
                        id='modes-dropdown',
                        options=[
                            {'label': 'Speed', 'value': 'Speed'},
                            {'label': 'Current', 'value': 'Current'}
                        ],
                        value='Speed'),
                    dcc.Markdown(children='### `Set Decimation`'),
                    dcc.Dropdown(
                        id='decimate-dropdown',
                        options=[
                            {'label': 'no decimation', 'value': '0'},
                            {'label': '1', 'value': '1'},
                            {'label': '2', 'value': '2'},
                            {'label': '3', 'value': '3'},
                            {'label': '4', 'value': '4'},
                            {'label': '6', 'value': '6'},
                            {'label': '8', 'value': '8'},
                            {'label': '10', 'value': '10'},
                            {'label': '12', 'value': '12'},
                        ],
                        value='0')],
                    style={'padding': '0px 0px 0px 0px',
                           'text-align': 'left'}),
                html.Div(
                    style={},
                    children=[
                        dcc.Markdown(children='### `Motor ON/OFF`'),
                        html.Button('ON/OFF', id='button' , disabled = True),
                        html.Div(id='output-text1', children='')]),
                html.Div(children=[
                    dcc.Markdown(children='### `RPM Slider`'),
                    html.Div([
                        dcc.Slider(
                            id='rpm-slider',
                            min=-5000,
                            max=5000,
                            value=0,
                            step=10,
                            marks={0: '0',
                                   5000: '5000',
                                   -5000: '-5000'})],
                        style={'padding': '0px 0px 20px 0px', }),
                    html.Div(id='output-text2', children='')],
                    style={'padding': '0px 0px 0px 10px'}),
                html.Div(children=[
                    dcc.Markdown(children='### `Torque Slider`'),
                    html.Div([
                        dcc.Slider(
                            id='torque-slider',
                            min=-500,
                            max=500,
                            value=0,
                            marks={0: '0',
                                   500: '500',
                                   -500: '-500'})],
                        style={'padding': '0px 0px 20px 0px', }),
                    html.Div(id='output-text3', children='')],
                    style={'padding': '0px 0px 0px 10px', })]),
        html.Div([
            dcc.Markdown(children='### `Set Plot Capture Mode`'),
            html.P('Selection will capture new data'),
            html.Div([
                dcc.RadioItems(
                    id='graphs-radio',
                    options=[
                        {'label': 'Ia Current', 'value': 'Ia Current'},
                        {'label': 'Ib Current', 'value': 'Ib Current'},
                        {'label': 'Angle', 'value': 'Angle'},
                        {'label': 'RPM', 'value': 'RPM'}
                    ],
                    value='Ia Current',
                    labelStyle={'display': 'inline-block'})],
                style={'padding': '0px 0px 20px 0px', }),
            html.Div(id='graphs')],
            style={'padding': '0px 0px 0px 0px',
                   'text-align': 'left',
                   "width": "750px"})])

random_x = range(0, 4096, 1)
random_x = list(random_x)



@app.callback(
    Output('output-text1', 'children'),
    [Input('button', 'n_clicks'),
     Input('modes-dropdown', 'value')],
    [State('rpm-slider', 'value'),
     State('rpm-slider', 'value')])
def motor_button(n_clicks, mode_val, rpm_val, torq_val):
    if int(n_clicks or 0) == 0:
        motor.set_mode('init_mode')
        time.sleep(4)
        motor.set_mode('reset_mode')
        return 'The Motor is Initialized'
    if int(n_clicks or 0) % 2 == 0:
        motor.set_mode('reset_mode')
        return 'The Motor is OFF'
    else:
        if str(mode_val) == 'Speed':
            motor.set_mode('rpm_mode')
            motor.set_rpm(int(rpm_val))
        else:
            motor.set_mode('torque_mode')
            motor.set_torque(int(torq_val))
        return 'The Motor is ON'

@app.callback(Output('button', 'disabled'), [Input('button', 'n_clicks')])     
def set_button_enabled_state(n_clicks):
    time.sleep(4)
    return False

@app.callback(
    Output('output-text2', 'children'),
    [Input('rpm-slider', 'value')])
def update_rpm(sliderValue):
    motor.set_rpm(sliderValue)
    return f'The Motor is set to {sliderValue} RPM'


@app.callback(
    Output('output-text3', 'children'),
    [Input('torque-slider', 'value')])
def update_torque(tsliderValue):
    motor.set_torque(tsliderValue)
    return f'The Motor is set to {tsliderValue} Torque'


@app.callback(
    Output('graphs', 'children'),
    [Input('graphs-radio', 'value'),
     Input('decimate-dropdown','value')])
def update_graphs(tsliderValue, decimation):
    graphs = []
    motor.capture_mode('ia_ib_angle_rpm')

    xlnk = Xlnk()
    input_buffer = xlnk.cma_array(shape=(256,), dtype=np.uint8)

    capture_address = input_buffer.physical_address
    capture_count = 128
    motor._write_controlreg(DECIMATION.offset, int(decimation))
    motor.write_capturereg(0, 2) # make capture unit ready

    def continuous_capture(capture_count):
        mmio_stream = MMIO(capture_address, 256)
        cap_list = [([]) for i in range(4)]
        for _ in range(capture_count):
            motor.stream_capture(capture_address)
            for i in range(4, 260, 4):
                stream = mmio_stream.read(i - 4, 4)
                highbits, lowbits = bytesplit(stream)
                if (i % 8 != 0):
                    cap_list[0].extend([(np.int16(lowbits))])
                    cap_list[1].extend([(np.int16(highbits))])
                else:
                    cap_list[2].extend([(np.int16(lowbits))])
                    cap_list[3].extend([(np.int16(highbits))])
        return cap_list

    cap_list = continuous_capture(capture_count)
    Ia, Ib, angle, rpm = cap_list[0], cap_list[1], cap_list[3], cap_list[2]
    
    current_Ia = (np.array(Ia)) * 0.00039
    current_Ib = (np.array(Ib)) * 0.00039
    
    motor.write_capturereg(0,0) #reset the capture unit
    
    data = {'Ia': current_Ia,
            'Ib': current_Ib,
            'angle': cap_list[3],
            'rpm': cap_list[2]}

    df = pd.DataFrame(data, columns=['Ia', 'Ib', 'angle', 'rpm'])

    if str(tsliderValue) == 'Ia Current':
        data = df.Ia
    elif str(tsliderValue) == 'Ib Current':
        data = df.Ib
    elif str(tsliderValue) == 'Angle':
        data = df.angle
    else:
        data = df.rpm

    graphs.append(dcc.Graph(
        id='Ia',
        figure={
            'data': [
                go.Scatter(
                    x=random_x,
                    y=data,
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                ) #for i in df.items()
            ],
            'layout':{
                'xaxis':{'title': 'Sample'},
                'yaxis':{'title': str(tsliderValue)},
                'margin':{'l': 80, 'b': 40, 't': 10, 'r': 10},
                'hovermode':'closest'}
        }
    ))
    
    #if False:
    graphs.append((html.Div([dcc.Markdown(children='### `Plot-2 Ia vs Ib`')],
                            style={'padding': '3px 3px 3px 3px'})))
    graphs.append(dcc.Graph(
        id='Ia vs Ib',
        figure={
            'data': [
                go.Scattergl(
                    x = df.Ia,
                    y = df.Ib,
                    mode='markers',
                    opacity=0.7,
                    marker=dict(color='#F0598E', line=dict(width=1)),
                    name = 'current'
                )#for i in df.items()
            ],
                'layout': { 
                    'xaxis' : {'title': 'Current Ia'},
                    'yaxis' : {'title': 'Current Ib'},
                    'margin': {'l': 80, 'b': 40, 't': 10, 'r': 10},
                    'hovermode': 'closest'}
        }
    ))
    
    return graphs
