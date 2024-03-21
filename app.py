from flask import Flask, Response
import dash
import dash.dcc as dcc
import dash.html as html
from dash.dependencies import Input, Output

# plots
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import io

# map
import geemap
import ee
import os
import geopandas
from geemap import geojson_to_ee, ee_to_geojson

ee.Authenticate(auth_mode='gcloud')
ee.Initialize(project='digital-yeti-417904')
print('Earth Engine Initialized')

server = Flask(__name__)

app = dash.Dash(__name__, server=server)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

 ### PAGE 1 ###

# map creation
def map_create():
    brazil_shapefile = geemap.shp_to_ee('Brazil.shp')

    Map = geemap.Map()

    landcover = ee.Image('MODIS/006/MCD12Q1/2004_01_01').select('LC_Type1')

    igbpLandCoverVis = {'min': 1.0, 'max': 17.0, 'palette': ['05450a', '086a10', '54a708', '78d203', '009900', 'c6b044', 'dcd159', 'dade48', 'fbff13', 'b6ff05', '27ff87', 'c24f44', 'a5a5a5', 'ff6d4c', '69fff8', 'f9ffa4', '1c0dff']}
    brazil_lc = landcover.clip(brazil_shapefile)
    Map.setCenter(-55, -10, 4)
    Map.addLayer(brazil_lc, igbpLandCoverVis, 'MODIS Land Cover')

    # Save it as html
    Map.save('map.html')

map_create()

page_1_layout = html.Div([
  html.H1('Page 1'),
  html.Div([
      html.Iframe(src='/map.html', width='100%', height='600')
  ]),
  html.Button('Go back to home', id='back'),
])

 ### PAGE 2 ###

page_2_layout = html.Div([
    html.H1('Page 2'),
    html.Div([
        html.Img(src='/plot.png')
    ]),
    dcc.Link('Go back to home', href='/'),
])

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

# plot creation
def plot_png():
   fig = Figure()
   axis = fig.add_subplot(1, 1, 1)
   xs = np.random.rand(100)
   ys = np.random.rand(100)
   axis.plot(xs, ys)
   output = io.BytesIO()
   FigureCanvas(fig).print_png(output)
   return Response(output.getvalue(), mimetype='image/png')

@app.server.route('/plot.png')
def plot():
    return plot_png()

# app generic functions
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)
