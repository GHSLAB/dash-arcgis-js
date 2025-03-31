import dash
from dash import html
from dash.dependencies import Input, Output
from feffery_dash_utils.style_utils import style

external_css = ["https://js.arcgis.com/4.32/esri/themes/light/main.css"]
external_scripts = [{"src": "https://js.arcgis.com/4.32/init.js"}]

app = dash.Dash(
    __name__,
    title="创建初始地图应用",
    external_scripts=external_scripts,
    external_stylesheets=external_css,
)

app.layout = html.Div(
    [
        html.Div(id="viewDiv", style=style(height="100%", width="100%")),
    ],
    style=style(height="100vh", width="100%", margin=0),
)


app.clientside_callback(
    """
    function(id) {
        require(["esri/Map", "esri/views/MapView"], function (Map, MapView) {
            var map = new Map({
                basemap: "topo-vector"
            });

            var view = new MapView({
                container: "viewDiv",
                map: map,
                center: [-117.18627177661713, 34.05918931592471],
                zoom: 11
            });
        });
    }
    """,
    Output("viewDiv", "data-done"),
    Input("viewDiv", "id"),
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8001)
