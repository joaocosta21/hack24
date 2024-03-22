import solara
from sol import MyMap 
from home import Home

routes = [
    solara.Route(path="/", component=Home, label="HomeLabel"),
    # the calculator module should have a Page component
    solara.Route(path="calculator", module=calculator, label="CalculatorLabel"),
    solara.Route(path="myMap", component=MyMap, label="MyMapLabel"),
]

@solara.component
def App():
        with solara.Row(style={"min-height": "500px", "backgroundColor": "green"}):
            solara.Router(routes=routes, style={"backgroundColor": "red"})