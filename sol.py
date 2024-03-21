import ee
import geemap
import solara
import os
import pandas as pd
import geopandas as gpd


ee.Authenticate(auth_mode='gcloud')
ee.Initialize(project='digital-yeti-417904')
print('Earth Engine Initialized')

class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_ee_data()
        self.add_inspector()

    def add_ee_data(self):
        region_of_interest = ee.FeatureCollection('FAO/GAUL/2015/level0')\
                      .filter(ee.Filter.eq('ADM0_NAME', 'Brazil'))
        
        # brazil_shapefile = geemap.shp_to_ee('Brazil.shp')
        brazil_shape = region_of_interest

        landcover = ee.Image('MODIS/006/MCD12Q1/2004_01_01').select('LC_Type1')
    
        ## Protected Areas ##
        # protected_areas = ee.FeatureCollection("WCMC/WDPA/current/polygons")
        # brazil_protected_areas = protected_areas.filterBounds(brazil_shape)
        # self.addLayer(brazil_protected_areas, {}, 'Protected Area')
        # self.addLayer(brazil_shape)


        # Define the ImageCollection for population data
        pop_collection = ee.ImageCollection('WorldPop/GP/100m/pop')\
                        .filterDate('2020-01-01', '2020-12-31').mean()
        pop_collection_brazil = pop_collection.clip(brazil_shape)

        vis = {'min': 0.0, 'max': 50.0, 'palette': ['24126c', '1fff4f', 'd4ff50']}
        
        self.addLayer(pop_collection_brazil, vis, 'Population')


        igbpLandCoverVis = {'min': 1.0, 'max': 17.0, 'palette': ['05450a', '086a10', '54a708', '78d203', '009900', 'c6b044', 'dcd159', 'dade48', 'fbff13', 'b6ff05', '27ff87', 'c24f44', 'a5a5a5', 'ff6d4c', '69fff8', 'f9ffa4', '1c0dff']}
        brazil_lc = landcover.clip(brazil_shape)
        self.setCenter(-55, -10, 4)
        self.addLayer(brazil_lc, igbpLandCoverVis, 'MODIS Land Cover')

        self.addLayerControl()
    
def Floating(children=None, style=None):
    return solara.Div(style={**style, "position": "absolute", "z-index": "9999"}, children=children)

def remove_layer_population():
    print('Removing Population Layer')

@solara.component
def RemovePopulationLayerButton():
    return solara.Button("Remove Population Layer", onclick=remove_layer_population)

@solara.component
def MyMap():
    # Use a state to keep track of the current map
    map = Map.element(zoom=4, height="800px")

    with solara.Column(style={"min-width": "500px"}):
        # Display the current map
        map