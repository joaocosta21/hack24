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
        brazil_shapefile = geemap.shp_to_ee('Brazil.shp')

        dataset = ee.ImageCollection("projects/climate-engine-pro/assets/ce-merra2_fwi-daily")
        image = dataset.filterDate('2022-12-01', '2023-02-01').select('FWI').max()

        vis_params = {
            'min': 0,
            'max': 50,
            'palette': ['green', 'yellow', 'orange', 'red'],
        }

        image = image.clip(brazil_shapefile)
        self.setCenter(-55, -10, 4)
        self.addLayer(image, vis_params, 'FWI')

        # legend
        legend_keys = ['Low', 'Medium', 'High']
        gradient_colors = [(0, 255, 0), (255, 255, 0), (255, 0, 0)]  # RGB for green, yellow, red

        # Define the title for the legend
        legend_title = 'FWI'

        # Add the gradient legend to the map
        self.add_legend(title=legend_title, keys=legend_keys, colors=gradient_colors, position='bottomright')

        self.addLayerControl()

@solara.component
def FWIMap():
    map = Map.element(zoom=4, height="800px")

    with solara.Column(style={"min-width": "500px"}):
        # Display the current map
        map