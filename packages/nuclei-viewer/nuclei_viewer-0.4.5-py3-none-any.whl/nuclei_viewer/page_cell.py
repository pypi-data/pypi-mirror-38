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
        html.Div(id='pc_uid', style={'display': 'none'}),
        html.Div(id='pc_info', style={'display': 'none'}),
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
        # Nuclei info
        html.Table(id='pc_table')
    ]),
    html.Div(className='ten columns', style={'min-height': '80vh'}, children=[
        dashx.ImageBox(
            id='pc_box',
            className='card',
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
                for k, v in {'Others': 'other', 'Tumor': 'ctc', 'Immune': 'immune'}.items()
            ]],
        ),
    ]),
])

#####################################################
# backend callback functions
@page.callback(
    Output('pc_group', 'options'),
    [Input('pt_uid', 'n_clicks')]
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
    [Input('pc_sample', 'value'), Input('pc_info', 'children')],
    [State('pc_group', 'value'), State('pc_tile', 'value')]
)
def list_tile(sample, info, group, tile):
    ''' update tiles from selected sample '''
    if info and tile:
        info = json.loads(info)
        count = info['ctc']['total'] if 'ctc' in info else 0
        count += info['immune']['total'] if 'immune' in info else 0
        return common.list_tile(group, sample, tile, count)
    return common.list_tile(group, sample)

@page.callback(
    Output('pc_uid', 'children'),
    [Input('pc_tile', 'value')],
    [State('pc_group', 'value'), State('pc_sample', 'value')]
)
def update_uid(tile, group, sample):
    if not group or not sample or not tile:
        return
    return os.path.join(group, sample, tile)

@page.callback(
    Output('pc_box', 'prob'),
    [Input('pc_prob', 'value')]
)
def update_prob(prob):
    return prob

@page.callback(
    Output('pc_info', 'children'),
    [Input('pc_uid', 'children'), Input('pc_prob', 'value'), Input('pc_box', 'clickData')],
)
def update_info(uid, prob, update):
    if not uid:
        return
    df = common.fetch_info(uid, update)
    if 'TumorProb' not in df.columns:
        df['TumorProb'] = 0.
     # fill nan for group-by
    def mask(df, f):
        return df[f(df)]
    pd.DataFrame.mask = mask
    df.Label.fillna('others', inplace=True)
    df.TumorProb.fillna(0, inplace=True)
    # calculate statitics
    df1 = df.groupby(['Label']).count()
    df2 = df.mask(lambda x: x.TumorProb >= prob).groupby(['Label']).count()
    df3 = df1.join(df2, rsuffix='_', sort=True).fillna(0)
    # return json object
    info = {}
    for r in df3.itertuples():
        info[r[0]] = {'total': r[1], 'sub': int(r[3])}
    return json.dumps(info)

@page.callback(
    Output('pc_table', 'children'),
    [Input('pc_info', 'children')],
    [State('pc_prob', 'value')],
)
def update_table(info, prob):
    if not info:
        return
    rows = [['probability', '{:.0%}'.format(prob)]]
    for k, v in json.loads(info).items():
        rows.append([k, '{} / {}'.format(v['sub'], v['total'])])
    return common.gen_table(rows)

@page.callback(
    Output('pc_box', 'data'),
    [Input('pc_uid', 'children')],
)
def update_mask(uid):
    if not uid:
        return {}
    res = common.image_size(uid)
    if not res:
        return {}
    w, h = res
    return {
        'src': '/r/{}'.format(uid),
        'masks': masks(uid, (h, w)),
    }

#####################################################
# utility functions
def masks(uid, size):
    items = []
    for m, c, v, p in helper.iter_contour(uid, size):
        g = v if v in ['ctc', 'immune'] else 'other'
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
