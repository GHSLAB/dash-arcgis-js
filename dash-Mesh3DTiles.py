import dash
from dash import html
from dash.dependencies import Input, Output
from feffery_dash_utils.style_utils import style

external_css = ["https://js.arcgis.com/4.33/esri/themes/light/main.css"]
external_scripts = [{"src": "https://js.arcgis.com/4.33/"}]

app = dash.Dash(
    __name__,
    title="IntegratedMesh3DTilesLayer",
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
    async function(id) {
    const [WebScene, SceneView, IntegratedMesh3DTilesLayer, Expand, LayerList, Legend] =
        await $arcgis.import([
          "@arcgis/core/WebScene.js",
          "@arcgis/core/views/SceneView.js",
          "@arcgis/core/layers/IntegratedMesh3DTilesLayer.js",
          "@arcgis/core/widgets/Expand.js",
          "@arcgis/core/widgets/LayerList.js",
          "@arcgis/core/widgets/Legend.js",
        ]);

      /*************************************
       * Load webscene with layer showing
       * building energy ratings
       *************************************/
      const webscene = new WebScene({
        portalItem: {
          id: "5b177c2579bf45159bb91e2a13b4218b",
        },
      });

      /*************************************
       * Create IntegratedMesh3DTilesLayer layer
       * and add it to the webscene
       ***********************************/
      const layer = new IntegratedMesh3DTilesLayer({
        url: "https://tiles.arcgis.com/tiles/V6ZHFr6zdgNZuVG0/arcgis/rest/services/Utrecht_3D_Tiles_Integrated_Mesh/3DTilesServer/tileset.json",
        title: "Utrecht Integrated Mesh 3D Tiles",
      });

      webscene.add(layer);

      /*************************************
       * Create the View and add expandable
       * LayerList and Legend widgets to the UI
       ***********************************/
      const view = new SceneView({
        container: "viewDiv",
        map: webscene,
      });

      const expandLegend = new Expand({
        content: new Legend({
          view: view,
        }),
        expanded: true,
        expandTooltip: "Expand Legend",
        group: "top-right",
        view: view,
      });

      const expandLayerList = new Expand({
        content: new LayerList({
          view: view,
        }),
        expandTooltip: "Expand Layer List",
        group: "top-right",
        view: view,
      });

      view.ui.add([expandLegend, expandLayerList], "top-right");
    }
    """,
    Output("viewDiv", "data-done"),
    Input("viewDiv", "id"),
)

if __name__ == "__main__":
    app.run(debug=True, port=8002)
