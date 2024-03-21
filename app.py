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
import folium
import pandas as pd
from folium.plugins import MarkerCluster
import geopandas as gpd
from shapely.geometry import Point, LineString
from shapely import wkt

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
    crs = 4386
    basin_data = pd.read_csv('basin_data.csv')

    basin_data['geometry'] = basin_data['geometry'].apply(wkt.loads) # turn text into objects
    geodata = gpd.GeoDataFrame(basin_data, crs = crs)

    plot_options = {
      'station':{'color': 'blue', 'size': 5},
      'pourpoint': {'color': 'red', 'size': 5},
      'nmwdi': {'color': 'green', 'size': 5}}

    geomap = folium.Map(location = [37.7749, -106.4194],
                    zoom_start = 9.2,
                    tiles = 'cartodbpositron',
                    control_scale = True)
    
    # tile layers -> map appearance
    folium.TileLayer('openstreetmap', attr="a").add_to(geomap)
    folium.TileLayer('stamenwatercolor', attr="b").add_to(geomap)
    folium.TileLayer('stamenterrain', attr="c").add_to(geomap)

    ### feature groups -> objects on top of the map ###
    basin_layer = folium.FeatureGroup(name = 'Basin Boundary', show=False)
    mainstem_layer = folium.FeatureGroup(name = 'Mainstem River', show=False)
    tributary_layer = folium.FeatureGroup(name='Tributary Rivers', show=False)
    # points on the map
    usgs_layer = folium.FeatureGroup(name = 'USGS Gauges', show=False)
    pourpoint_layer = folium.FeatureGroup(name= 'HUC12 Pour Points', show=False)
    nmwdi_layer = folium.FeatureGroup(name='NM Water Data Initiative Gauge', show=False)

    # add points -> todo: this needs to be taylormade
    plot_types = ['station', 'nmwdi', 'pourpoint'] # only points have these types
    plot_layers = [usgs_layer, nmwdi_layer, pourpoint_layer]
    
    for i, feature_type in enumerate(plot_types):
        map_layer = plot_layers[i]
    
        for _, point in geodata.loc[geodata['type'] == feature_type].iterrows():    
            coords = [point.geometry.y, point.geometry.x]
            
            # Add the popup box with description -> note: we can actually use this to convey useful
            # information such as risk percentage or other data
            textbox = folium.Popup(point.description,
                                  min_width= 300,
                                  max_width= 300)
    
            # Add the marker at the coordinates with color-coordination
            folium.CircleMarker(coords,
                                popup= textbox,
                                # whatever, the rest is style -> can be used for visual information too
                                # e.g. risk level, severity, protected area/not protected area, etc.
                                fill_color = plot_options[feature_type]['color'],
                                fill = True,
                                fill_opacity = 0.85,
                                radius= plot_options[feature_type]['size'],
                                color = plot_options[feature_type]['color']).add_to(map_layer)
    # Plot basin border
    for i,r in geodata.loc[geodata['type'] == 'basin'].iterrows():
        # Convert the Polygon or LineString to geoJSON format
        geo_json = gpd.GeoSeries(r['geometry']).simplify(tolerance = 0.000001).to_json()
        geo_json = folium.GeoJson(data= geo_json,
                                  style_function=lambda x: {'fillcolor': 'none',
                                                            'weight': 2, 
                                                            'color': 'black',
                                                            'opacity': 1,
                                                            'fill_opacity': 0.5,
                                                            'fill': True})
        # Add popup with line description
        folium.Popup(r.description,
                    min_width = 30,
                    max_width= 30).add_to(geo_json)
        
        # Add the feature to the appropriate layer
        geo_json.add_to(basin_layer)

    # Add the layers to the map
    basin_layer.add_to(geomap)
    mainstem_layer.add_to(geomap)
    tributary_layer.add_to(geomap)
    usgs_layer.add_to(geomap)
    pourpoint_layer.add_to(geomap)
    nmwdi_layer.add_to(geomap)

    # Save it as html
    folium.LayerControl().add_to(geomap)
    geomap.save('map.html')

map_create()

page_1_layout = html.Div([
  html.H1('Page 1'),
  html.Div([
      html.Iframe(srcDoc=open('map.html', 'r').read(), width='100%', height='600')
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
