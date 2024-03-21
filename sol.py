import ee
import geemap
import solara
import os
import pandas as pd
import geopandas as gpd


ee.Authenticate(auth_mode='gcloud')
ee.Initialize(project='start-hack-agoncalve')
print('Earth Engine Initialized')

# class Map(geemap.Map):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.add_ee_data()

#     def add_ee_data(self):
#         years = ['2001', '2004', '2006', '2008', '2011', '2013', '2016', '2019']
#         def getNLCD(year):
#             dataset = ee.ImageCollection('USGS/NLCD_RELEASES/2019_REL/NLCD')
#             nlcd = dataset.filter(ee.Filter.eq('system:index', year)).first()
#             landcover = nlcd.select('landcover')
#             return landcover

#         collection = ee.ImageCollection(ee.List(years).map(lambda year: getNLCD(year)))
#         labels = [f'NLCD {year}' for year in years]
#         self.ts_inspector(
#             left_ts=collection,
#             right_ts=collection,
#             left_names=labels,
#             right_names=labels,
#         )
#         self.add_legend(
#             title='NLCD Land Cover Type',
#             builtin_legend='NLCD',
#             height="460px",
#             add_header=False
#         )


protected_areas = "/offline_data/data_protected_areas/shp/"
shp_files = [
    os.getcwd() + "/offline_data/data_protected_areas/shp/WDPA_WDOECM_Mar2024_Public_BRA_shp_0/WDPA_WDOECM_Mar2024_Public_BRA_shp-polygons.shp",
    os.getcwd() + "/offline_data/data_protected_areas/shp/WDPA_WDOECM_Mar2024_Public_BRA_shp_1/WDPA_WDOECM_Mar2024_Public_BRA_shp-polygons.shp",
    os.getcwd() + "/offline_data/data_protected_areas/shp/WDPA_WDOECM_Mar2024_Public_BRA_shp_2/WDPA_WDOECM_Mar2024_Public_BRA_shp-polygons.shp",
]

combined_gdf = gpd.GeoDataFrame()
for shp_file in shp_files:
    # Read the shapefile
    gdf = gpd.read_file(shp_file)
    
    # Append the GeoDataFrame to the combined GeoDataFrame
    combined_gdf = pd.concat([combined_gdf, gdf], ignore_index=True)


combined_gdf = combined_gdf[combined_gdf['MARINE'] != '2']
simplified_geometry = combined_gdf.simplify(tolerance=0.01, preserve_topology=True)
combined_gdf['geometry'] = simplified_geometry

protected_areas = geemap.geopandas_to_ee(combined_gdf)


# for shp_file in shp_files:
#     # Read the shapefile
#     gdf = gpd.read_file(shp_file)
#     # Append the GeoDataFrame to the combined GeoDataFrame
#     combined_gdf = pd.concat([combined_gdf, gdf], ignore_index=True)

# # Remove all marine protected areas
# combined_gdf = combined_gdf[combined_gdf['MARINE'] != '2']


class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_ee_data()

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
        # self.addLayer(brazil_lc, igbpLandCoverVis, 'MODIS Land Cover')

@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element(
            zoom=4,
            height="800px",
        )