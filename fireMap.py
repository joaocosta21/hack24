import ee
import geemap
import solara
import os
import pandas as pd
import geopandas as gpd

class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_ee_data()

    def add_ee_data(self):
        countries = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
        brazil = countries.filter(ee.Filter.eq('country_na', 'Brazil'))
        protected_areas = ee.FeatureCollection('WCMC/WDPA/current/polygons')
        brazil_protected_areas = protected_areas.filterBounds(brazil)

        # Load Brazil's regions
        countries = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
        brazil = countries.filter(ee.Filter.eq('country_na', 'Brazil'))

        # Load Protected areas
        protected_areas = ee.FeatureCollection('WCMC/WDPA/current/polygons')
        brazil_protected_areas = brazil_protected_areas.map(lambda
            feature: feature.intersection(brazil))

        # Filter protected areas in Brazil
        brazil_protected_areas = protected_areas.filterBounds(brazil)

        # Get the Global Forest Change dataset
        gfc2020 = ee.Image('UMD/hansen/global_forest_change_2020_v1_8')
        # Load the MODIS/061/MCD64A1 collection
        fire_dataset = ee.ImageCollection('MODIS/061/MCD64A1').filter(ee.Filter.date('2017-01-01', '2018-05-01'))

        # Select the 'lossyear' band and clip to Brazil's protected areas
        mask = ee.Image().byte().paint(brazil_protected_areas, 1)
        forest_loss = gfc2020.select('lossyear').updateMask(mask)
        burnedArea = fire_dataset.select('BurnDate').mean().updateMask(mask)

        # Define the visualization parameters for forest loss.
        forest_loss_vis = {
          'bands': ['lossyear'],
          'min': 20.0,
          'max': 20.0,
          'palette': ['green', 'green']
        }


        # Select the 'BurnDate' band and clip to Brazil's protected areas

        fire_palette = ['FF0000']  # red

        burnedArea_vis = {
            'min': 30.0,
            'max': 500.0,
            'palette': fire_palette
        }

        # Add the deforestation layer to the map
        self.addLayer(forest_loss, forest_loss_vis, 'Deforestation in Protected Areas')
        self.addLayer(brazil_protected_areas, {}, 'Protected Areas in Brazil')

        # Add fire data to the self
        self.addLayer(burnedArea, burnedArea_vis, 'Fire Data')

@solara.component
def FireMap():
    map = Map.element(zoom=4, height="800px")

    with solara.Column(style={"min-width": "500px"}):
        # Display the current map
        map