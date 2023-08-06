import os
import re
import json
import base64
from datetime import datetime
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from flask import send_file, request
from PIL import Image
from io import BytesIO
from . import app, page, cache
from . import helper
from .config import config

#####################################################
# backend callback functions
def list_group():
    # fire on page load
    return [
        {'label': f.name, 'value': f.name}
        for f in os.scandir(helper.dataset_path) if f.is_dir()
    ]

def list_samples(group):
    ''' update samples from selected group '''
    if not group:
        return []
    return sorted([
        {'label': helper.shorten(f.name, n=15, suffix=True), 'value': f.name}
        for f in os.scandir(os.path.join(helper.dataset_path, group)) if f.is_dir()
    ], key=lambda x: x['value'])

def list_tile(group, sample, tile=None, count=None, color=None):
    ''' update items from selected dataset '''
    if not group or not sample:
        return [[]]
    sid = os.path.join(group, sample)
    data = helper.read_metadata(sid)
    if 'grid' not in data:
        # '.' imply current directory in unix
        return [[{'label': 'Single', 'value': '.'}]]
    color = color if color != 'Silver' else ''
    grid = data['grid']
    grid_color = data['color'] if 'color' in data else np.empty_like(grid, dtype=str).tolist()
    options = []
    for j, r in enumerate(grid):
        row = []
        for i, c in enumerate(r):
            tid = '{}_{}'.format(j, i)
            if tid == tile:
                grid[j][i] = c = count
                grid_color[j][i] = color
            cell = {'label': '', 'value': tid}
            if not helper.is_valid_sample(os.path.join(group, sample, tid)):
                cell['disabled'] = True
            else:
                if grid_color[j][i]:
                    cell['style'] = {'color': grid_color[j][i]}
                cell['label'] = c
            row.append(cell)
        options.append(row)
    if tile:
        data['grid'] = grid
        data['color'] = grid_color
        helper.write_metadata(sid, data)
    return options

def fetch_info(uid, update=None):
    mask_csv = helper.csv_path(uid)
    df = pd.read_csv(mask_csv, index_col='ImageId', dtype={'Label': str})
    if 'Label' not in df.columns:
        df['Label'] = np.NaN
    if update:
        label = update['label']
        mask = update['mask']
        df.at[mask, 'Label'] = np.NaN if label == 'other' else label
        if 'contour' in update:
            rle = helper.contour_rle(update['contour'], image_size(uid))
            print(rle)
            df.at[mask, 'EncodedPixels'] = rle
        df.to_csv(mask_csv)
    return df

def gen_table(items):
    return [html.Tr([
        html.Td(d.upper() if i == 0 else d) for i, d in enumerate(r)
    ]) for r in items]

@app.route('/r/<path:uid>')
def serve_image(uid):
    # Refer: http://flask.pocoo.org/docs/1.0/quickstart/#the-request-object
    # ?key=value <=> value = request.args.get('key', '')
    channel = json.loads(config.get('channels', 'UI'))
    c = request.args.get('c', channel[0][0])
    e = request.args.get('e', 'true') == 'true'
    res = rawimg(uid, c, e)
    if not res:
        return ''
    buff, _, _ = res
    buff.seek(0)
    return send_file(buff, mimetype='image/jpeg', last_modified=datetime.now())

@cache.memoize()
def image_size(uid):
    fp = helper.image_picker(uid, 'DAPI', 0)
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
    failback=0 if channel=='DAPI' else None # failback to first file if DAPI channel
    fp = helper.image_picker(uid, channel, failback)
    if not fp:
        return None
    if isinstance(fp, list):
        r, g, b = Image.open(fp[0]), Image.open(fp[1]), Image.open(fp[2])
        if enhance:
            r, g, b = helper.ptche(r), helper.ptche(g), helper.ptche(b)
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
            if enhance:
                im = helper.ptche(im)
            # colorize grayscale image
            r = g = b = np.zeros_like(im)
            rgb = [r, g, b]
            gray = np.asarray(im)
            colorize = json.loads(config.get('channels', 'colorize'))
            rgb[colorize[channel]] = gray
            rgb = np.dstack(rgb)
            im = Image.fromarray(rgb)
    # convert to base64 jpeg
    w, h = im.size
    buff = BytesIO()
    im.save(buff, format='jpeg', quality=quality)
    return buff, w, h