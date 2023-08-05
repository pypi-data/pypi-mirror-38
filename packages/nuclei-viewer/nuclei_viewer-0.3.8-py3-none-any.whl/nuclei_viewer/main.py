import os
import re
import json
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from flask_caching import Cache
from flask import send_file
from PIL import Image
import base64
import pandas as pd
from io import BytesIO
from urllib.parse import unquote
from . import app
from . import helper
from .config import config
from . import dashx
from . import __version__

#####################################################
# global variables
color = {
    'centroid': 'MistyRose',
    'ctc': 'Gold',
    'nuclei': 'LightSkyBlue', 
    'immune': 'ForestGreen'
}

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
page = dash.Dash(server=app)
page.title = 'Nuclei Viewer'
channels = json.loads(config.get('channels', 'UI'))

#####################################################
# frontend page layout
page.layout = html.Div([
        # Banner
        html.Div(className='banner', children=[
            html.Img(src="/assets/aixmed.png", className='logo'),
            html.H2('Nuclei Analysis App'),
            html.H6('© 2018 AIxMed, Inc. All Rights Reserved.'),
            html.Span(__version__),
            html.Img(src="/assets/logo.png")
        ]),
        # hidden variables
        html.Div(id='dummy', style={'display': 'none'}),
        # represents the URL bar, doesn't render anything
        dcc.Location(id='url', refresh=False),
        # Body
        html.Div(className='container row', children=[
            # menu and info
            html.Div(className='two columns', children=[
                # Dataset info
                html.Div(className='card', children=[
                    dcc.Dropdown(
                        id='group',
                        className='dropdown',
                        searchable=False,
                        placeholder='Group ...',
                    ),
                    dcc.Dropdown(
                        id='sample',
                        className='dropdown',
                        searchable=True,
                        placeholder='Samples ...',
                    ),
                    dashx.RadioItemRows(id='tile', style={'display': 'grid'}),
                ]),
                # Toolbar
                dashx.RadioItemRows(
                    id='channel',
                    className='card',
                    options=[[{'label': i, 'value': i} for i in sub] for sub in channels],
                    value=channels[0][0]
                ),
                dashx.RadioItemRows(
                    id='enhance',
                    className='card',
                    options=[[{'label': i, 'value': i} for i in ['Enhanced', 'Origin']]],
                    value='Enhanced'
                ),
                dashx.RadioItemRows(
                    id='lock-zoom',
                    className='card',
                    options=[[{'label': i, 'value': i} for i in ['Zoom lock', 'Refresh']]],
                    value='Zoom lock'
                ),
                dashx.RadioItemRows(
                    id='filter-nuclei',
                    className='card',
                    options=[[{'label': i, 'value': i} for i in ['Adjacent', 'Generous']]],
                    value='Adjacent'
                ),
                dashx.RadioItemRows(
                    id='cell',
                    className='card',
                    options=[[{'label': i, 'value': i} for i in ['Tumor', 'Immune']]],
                    value='Tumor'
                ),
                dashx.TableInfo(id='info', graph='graph', cell='ctc', color=color),
            ]),
            # major content
            dcc.Graph(
                id='graph',
                className='ten columns',
                style={'height': '90vh'},
                config={
                    'modeBarButtonsToRemove': [
                        'sendDataToCloud', 'zoom2d', 'select2d', 'lasso2d',
                        'autoScale2d', 'hoverClosestCartesian',
                        'hoverCompareCartesian', 'toggleSpikelines', 'resetScale2d'
                    ],
                    'scrollZoom': True,
                    'doubleClick': 'autosize',
                    'displaylogo': False,
                }
            )
        ])
    ])

#####################################################
# backend callback functions
@page.callback(
    Output('group', 'options'), 
    [Input('dummy', 'n_clicks')]
)
@cache.memoize()
def list_group(_):
    # fire on page load
    return [
        {'label': f.name, 'value': f.name} 
        for f in os.scandir(helper.dataset_path) if f.is_dir()
    ]

@page.callback(
    Output('sample', 'options'), 
    [Input('group', 'value')]
)
@cache.memoize()
def list_samples(group):
    ''' update samples from selected group '''
    if not group:
        return []
    return sorted([
        {'label': shorten(f.name, n=15, suffix=True), 'value': f.name}
        for f in os.scandir(os.path.join(helper.dataset_path, group)) if f.is_dir()
    ], key=lambda x: x['value'])

@page.callback(
    Output('tile', 'options'), 
    [Input('sample', 'value')],
    [State('group', 'value')]
)
def list_tile(sample, group):
    ''' update items from selected dataset '''
    if not group or not sample:
        return [[]]
    uid = os.path.join(group, sample)
    data = helper.read_metadata(uid)
    if 'grid' not in data:
        return [[{'label': '', 'value': ''}]]
    grid = np.array(data['grid'])
    options = []
    for j in range(grid.shape[0]):
        option = []
        for i in range(grid.shape[1]):
            tile = '{}_{}'.format(j, i)
            uid = os.path.join(group, sample, tile)
            option.append({
                'label': grid[j, i], 
                'value': tile, 
                'disabled': False if helper.is_valid_sample(uid) else True
            })
        options.append(option)
    return options

@page.callback(
    Output('tile', 'value'),
    [Input('tile', 'options')])
def update_tile(tile):
    if tile and len(tile[0]):
        return tile[0][0]['value']

@page.callback(
    Output('graph', 'figure'),
    [Input('tile', 'value'), Input('channel', 'value'), 
     Input('filter-nuclei', 'value'), Input('enhance', 'value')],
    [State('group', 'value'), State('sample', 'value'),
     State('lock-zoom', 'value'), State('graph', 'relayoutData')]
)
def update_graph(tile, channel, nearby, enhance, group, sample, zoom, relayout):
    if not group or not sample or tile is None:
        return {}
    uid = os.path.join(group, sample, tile)
    res = b64img(uid, channel, (enhance == 'Enhanced'))
    if not res:
        return {'layout': {'title': 'Invalid image data'}}
    b64, w, h = res
    # figure images
    images = [dict(
        xref='x',
        yref='y',
        x=0,
        y=0,
        yanchor='top', # top-left is (0, 0)
        sizing='stretch',
        sizex=w,
        sizey=h,
        layer='below',
        #####
        # Bug at https://github.com/plotly/plotly.js/blob/edc166f62d0d958194c04d830501a741cf6c7175/src/components/images/draw.js#L77
        # Code: ``` if(this.img && this.img.src === d.source) { ```
        # which handle query path incorrectly, then always trigger image download, even it's same url
        # To workaround the issue, need a full url href. 
        # However, the hack won't work inside docker or reverse proxy, alternaitve way is base64 encoded image
        #####
        # source='/image/{}/{}'.format(mode, uid)
        source=b64
    )] if channel else []
    # figure grid lines
    xaxis = dict(
        autorange=False,
        showgrid=False,
        zeroline=False,
        showline=False,
        range=(0, w),
        scaleanchor='y',
        scaleratio=1,
    )
    yaxis = dict(
        autorange=False,
        showgrid=False,
        zeroline=False,
        showline=False,
        range=(h, 0),
    )
    if relayout and zoom == 'Zoom lock':
        if 'xaxis.range[0]' in relayout:
            xaxis['range'] = (
                relayout['xaxis.range[0]'],
                relayout['xaxis.range[1]']
            )
        if 'yaxis.range[0]' in relayout:
            yaxis['range'] = (
                relayout['yaxis.range[0]'],
                relayout['yaxis.range[1]']
            )
    # configure legend
    legend = dict(
        x=0,
        y=1.01,
        orientation='h'
    )
    # custom menu with buttons
    menus = [dict(
        buttons = [
            dict(
                label='+nuclei',
                method='relayout',
                args=['dragmode', 'lasso'],
            ),
        ],
        direction = 'left',
        showactive = False,
        type = 'buttons',
        x = 1,
        y = 0,
        font = dict(size=8),
        borderwidth=0
    )]
    # configure layout
    layout = dict(
        autosize=True,
        dragmode='pan',
        hovermode='closest',
        xaxis=xaxis,
        yaxis=yaxis,
        images=images,
        margin=dict(t=10, b=30, l=40, r=10, pad=4),
        legend=legend,
        updatemenus=menus,
    )
    data = traces(uid, (h, w), (nearby == 'Adjacent'))
    return dict(data=data, layout=layout)

@page.callback(
    Output('info', 'cell'),
    [Input('cell', 'value')],
)
def update_cell(cell):
    if not cell:
        return
    return 'ctc' if cell == 'Tumor' else 'immune'

@page.callback(
    Output('dummy', 'children'),
    [Input('info', 'clickData')],
    [State('group', 'value'), State('sample', 'value'), 
     State('tile', 'value'), State('cell', 'value')],
)
def handle_click(click_data, group, sample, tile, cell):
    if not group or not sample or tile is None:
        return
    uid = os.path.join(group, sample, tile)
    mask_csv = helper.csv_path(uid)
    g = 'ctc' if cell == 'Tumor' else 'immune'
    mask = click_data['uid']
    df = pd.read_csv(mask_csv, index_col='ImageId', dtype={'Label': str})
    if 'Label' not in df.columns:
        df['Label'] = ''
    cur = df.at[mask, 'Label']
    df.at[mask, 'Label'] = g if g != cur else ''
    df.to_csv(mask_csv)

@app.route('/image/<channel>/<path:subpath>')
def serve_image(channel, subpath):
    res = rawimg(subpath, channel)
    if not res:
        return
    buff, _, _ = res
    buff.seek(0)
    return send_file(buff, mimetype='image/jpeg')

#####################################################
# utility functions
def traces(uid, size, nearby):
    ''' parse json in syntax: 
    {
       'centroid': [[y0, x0], [y1, x1], [y2, x2] ... ], 
       'ctc': ['mask01', 'mask02' ...] 
    }
    '''
    items = []
    data = helper.read_metadata(uid)
    # parse centroid markers
    centroid = None
    if 'centroid' in data and len(data['centroid']):
        centroid = np.array(data['centroid'], dtype=object)
        has_label = centroid.shape[1] == 3
        items.append(dict(
            showlegend = True,
            legendgroup = 'centroid',
            name = 'centroid',
            mode = 'markers',
            hoverinfo = 'text' if has_label else 'x+y',
            marker = {'color': color['centroid'], 'symbol': 'x', 'size': 10},
            x = centroid[:, 1],
            y = centroid[:, 0],
            text = centroid[:, 2] if has_label else ''
        ))
        centroid = centroid[:, :2].astype(int)
    # parse contours
    def trace(g, name, is_legend=False, visible=True, x=[0], y=[0]):
        return dict(
            showlegend = is_legend,
            legendgroup = g,
            name = shorten(name),
            customdata = [name],
            mode = 'lines',
            line = {'color': color[g]},
            x = x,
            y = y,
            fill = 'none' if is_legend else 'toself',
            fillcolor = color[g],
            opacity = 1.0 if is_legend else 0.7,
            hoverinfo = 'skip' if is_legend else 'name',
            visible = True if visible else 'legendonly',
        )
    # non-interactive legend placeholders
    hide_nuclei = config.getboolean('channels', 'hide_nuclei', fallback=False)
    for g in ['nuclei', 'ctc', 'immune']:
        visible = g != 'nuclei' if hide_nuclei else True
        items.append(trace(g, g, True, visible))
    # iterate contours
    centroid = centroid if nearby else None
    for m, c, v, p in helper.iter_contour(uid, size, centroid):
        g = v if v in ['ctc', 'immune'] else 'nuclei'
        c = np.vstack((c, c[0])) # closure shape to first pixel
        visible = g != 'nuclei' if hide_nuclei else True
        items.append(trace(g, m, False, visible, c[:, 1], c[:, 0]))
    return items

def shorten(s, n=10, suffix=False):
    # truncate a string to at most n characters
    if suffix:
        return '...' + s[-n:] if len(s) > n else s
        # n = n-5
        # return s[:n] + (s[n:] and '...' + s[-5:])
    else:
        return s[:n] + (s[n:] and '...')

@cache.memoize()
def image_size(uid):
    fp = helper.image_picker(uid, 'DAPI')
    if not fp:
        return None
    im = Image.open(fp)
    return im.size

@cache.memoize()
def b64img(uid, channel, enhance):
    res = rawimg(uid, channel, enhance)
    if not res:
        return
    buff, w, h = res
    encoded = base64.b64encode(buff.getvalue()).decode("utf-8")
    return 'data:image/jpeg;base64, ' + encoded, w, h

def rawimg(uid, channel, enhance=False, quality=75):
    enhance_dapi_only = config.getboolean('channels', 'enhance_DAPI_only', fallback=True)
    failback=0 if channel=='DAPI' else None # failback to first file if DAPI channel
    fp = helper.image_picker(uid, channel, failback)
    if not fp:
        return None
    if isinstance(fp, list):
        r, g, b = Image.open(fp[0]), Image.open(fp[1]), Image.open(fp[2])
        if enhance and enhance_dapi_only:
            b = helper.clahe(b)
        im = Image.merge('RGB', (r, g, b))
    else:
        im = Image.open(fp)
        if im.mode == 'I;16':
            # Convert from 16-bit to 8-bit.
            # Image.point() does not support divide operation.
            # 255/65535 = 0.0038910505836575876, map [0, 65535] to [0, 255] 
            im = im.point(lambda i: i * 0.0038910505836575876)
            im = im.convert('L')
        if im.mode == 'RGBA':
            im = im.convert('RGB')
        if im.mode == 'L':
            if enhance and enhance_dapi_only and channel == 'DAPI':
                im = helper.clahe(im)
            # colorize grayscale image
            r = g = b = np.zeros_like(im)
            rgb = [r, g, b]
            gray = np.asarray(im)
            colorize = json.loads(config.get('channels', 'colorize'))
            rgb[colorize[channel]] = gray
            rgb = np.dstack(rgb)
            im = Image.fromarray(rgb)
    if enhance and not enhance_dapi_only:
        im = helper.clahe(im)
    # convert to base64 jpeg
    w, h = im.size
    buff = BytesIO()
    im.save(buff, format='jpeg', quality=quality)
    return buff, w, h