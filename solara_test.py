import solara
import ee

from myMap import MyMap 
from fwiMap import FWIMap
from fireMap import FireMap
from home import Home

ee.Authenticate(auth_mode='gcloud')
ee.Initialize(project='digital-yeti-417904')
print('Earth Engine Initialized')

routes = [
    solara.Route(path="/", component=Home, label="Home"),
    solara.Route(path="myMap", component=MyMap, label="MyMapLabel"),
    solara.Route(path="fwiMap", component=FWIMap, label="FWI Map"),
    solara.Route(path="fireMap", component=FireMap, label="Fire Map")
]

@solara.component
def App():
        with solara.Row(style={"min-height": "500px", "backgroundColor": "green"}):
            solara.Router(routes=routes, style={"backgroundColor": "red"})