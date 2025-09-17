import dash
from dash import html
from dash.dependencies import Input, Output
from feffery_dash_utils.style_utils import style

external_css = ["https://js.arcgis.com/4.32/esri/themes/light/main.css"]
external_scripts = [{"src": "https://js.arcgis.com/4.32/init.js"}]

app = dash.Dash(
    __name__,
    title="3D Builderlayer",
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
        require([
            "esri/Map",
            "esri/views/SceneView",
            "esri/layers/BuildingSceneLayer"
        ], function (Map, SceneView, BuildingSceneLayer) {

            var map = new Map({ basemap: "topo-vector", ground: "world-elevation" });

            var view = new SceneView({
                container: "viewDiv",
                map: map,
                camera: {
                    position: {
                        x: -117.18627177661713,
                        y: 34.05918931592471,
                        z: 436.2859044605866 // meters
                    },
                    tilt: 81.4388260694481,
                    heading: 329.7245353350984
                }
            });
            // Create the BuildingSceneLayer and add it to the webscene
            // 加载建筑图层
            const buildingLayer = new BuildingSceneLayer({
                url:
                    "https://tiles.arcgis.com/tiles/V6ZHFr6zdgNZuVG0/arcgis/rest/services/BSL__4326__US_Redlands__EsriAdminBldg_PublicDemo/SceneServer",
                title: "Administration Building, Redlands - Building Scene Layer"
            });
            map.add(buildingLayer);

            // 定义click事件函数, 获取当前view试图的camera参数
            view.on("click", function () { console.log(view.camera); });
        });
    }
    """,
    Output("viewDiv", "data-done"),
    Input("viewDiv", "id"),
)

if __name__ == "__main__":
    app.run(debug=True, port=8002)
