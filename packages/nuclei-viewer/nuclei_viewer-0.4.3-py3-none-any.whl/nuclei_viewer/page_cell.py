import os
import json
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from . import app, page, cache
from . import helper
from .config import config
from . import common
from . import dashx

#####################################################
# global variables

#####################################################
# frontend page layout
layout = html.Div(className='row', children=[
    html.Div(className='two columns', children=[
        # hidden variables
        html.Div(id='pc_dummy', style={'display': 'none'}),
        # Dataset info
        html.Div(className='card', children=[
            dcc.Dropdown(
                id='pc_group',
                className='dropdown',
                searchable=False,
                placeholder='Group ...',
            ),
            dcc.Dropdown(
                id='pc_sample',
                className='dropdown',
                searchable=True,
                placeholder='Samples ...',
            ),
            dashx.RadioItemRows(id='pc_tile', style={'display': 'grid'}),
        ]),
        # Toolbar
        html.Div(className='card', style={'height': '35px'}, children=[
            dcc.Slider(
                id='pc_prob',
                min=0,
                max=1,
                step=0.05,
                value=0.7,
                included=False,
                marks= {p: {'label': '{:.0%}'.format(p)} for p in [0, 0.4, 0.7, 1]}
            ),
        ]),
    ]),
    html.Div(className='ten columns', style={'min-height': '80vh'}, children=[
        dashx.ImageBox(
            id='pc_box', 
            channel=[
                [{'label': i, 'value': i} for i in sub] 
                for sub in json.loads(config.get('channels', 'UI'))
            ],
            enhance=[[
                {'label': k, 'value': v} 
                for k, v in {'Enhanced': True, 'Origin': False}.items()
            ]],
            cell=[[
                {'label': k, 'value': v} 
                for k, v in {'Nah': 'nuclei', 'Tumor': 'ctc', 'Immune': 'immune'}.items()
            ]],
        ),
    ]),
])

#####################################################
# backend callback functions
@page.callback(
    Output('pc_group', 'options'), 
    [Input('pc_dummy', 'n_clicks')]
)
@cache.memoize()
def list_group(_):
    # fire on page load
    return common.list_group()

@page.callback(
    Output('pc_sample', 'options'), 
    [Input('pc_group', 'value')]
)
@cache.memoize()
def list_samples(group):
    ''' update samples from selected group '''
    return common.list_samples(group)

@page.callback(
    Output('pc_tile', 'options'), 
    [Input('pc_sample', 'value')],
    [State('pc_group', 'value')]
)
def list_tile(sample, group):
    ''' update items from selected dataset '''
    return common.list_tile(sample, group)

@page.callback(
    Output('pc_tile', 'value'),
    [Input('pc_tile', 'options')])
def update_tile(tile):
    return common.update_tile(tile)

@page.callback(
    Output('pc_box', 'prob'),
    [Input('pc_prob', 'value')])
def update_prob(prob):
    return prob

@page.callback(
    Output('pc_box', 'data'),
    [Input('pc_tile', 'value')],
    [State('pc_group', 'value'), State('pc_sample', 'value')]
)
def update_nuclei(tile, group, sample):
    if not group or not sample or tile is None:
        return {}
    uid = os.path.join(group, sample, tile)
    res = common.image_size(uid)
    if not res:
        return {}
    w, h = res
    return {
        'src': '/r/{}'.format(uid),
        'nuclei': nuclei(uid, (h, w)),
    }

@page.callback(
    Output('pc_dummy', 'children'),
    [Input('pc_box', 'clickData')],
    [State('pc_group', 'value'), State('pc_sample', 'value'), 
     State('pc_tile', 'value')],
)
def handle_click(click_data, group, sample, tile):
    return common.handle_click(click_data, group, sample, tile)

#####################################################
# utility functions
#@helper.timeit
def nuclei(uid, size):
    items = []
    for m, c, v, p in helper.iter_contour(uid, size):
        g = v if v in ['ctc', 'immune'] else 'nuclei'
        p0 = np.min(c, axis=0)
        p1 = np.max(c, axis=0)
        d = p1 - p0 # w, h of nuclei
        # expand to triple rectangle
        p0 -= d
        p1 += d
        items.append({
            'mask': m,
            'label': g,
            # [y0, x0], [y1, x1] => [x0, y0, x1, y1]
            'rect': p0[::-1].tolist() + p1[::-1].tolist(),
            'prob': p,
        })
    return items
