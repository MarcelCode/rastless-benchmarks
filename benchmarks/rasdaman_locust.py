from locust import HttpUser, task

from benchmarks.settings import RasdamanSettings, RasdamanLocalSettings, Settings
from benchmarks.utils.auth import get_keycloak_bearer_token
from benchmarks.utils.tools import RandomDate, RandomTile, geojson_file_to_dict, RandomGeometryGeojson

BEARER_TOKEN = get_keycloak_bearer_token(RasdamanSettings)

geojson = geojson_file_to_dict(Settings.aoi_geojson_file)
random_geometry_gen = RandomGeometryGeojson(geojson)
random_geometry_gen.generate_points()


class Rasdaman(HttpUser):
    random_tile = RandomTile(Settings.tiles)
    random_dates = RandomDate(Settings.dates)

    host = ""
    layer_id = ""
    url = ""
    headers = {}

    @task
    def get_tile(self):
        tile = self.random_tile.get_tile()
        datetime = self.random_dates.get_date()

        request_url = self.url.format(layer_id=self.layer_id, datetime=datetime, bbox=tile.str_xy_bounds)

        self.client.get(request_url, headers=self.headers, name="tile")


class RasdamanProxyVisualization(Rasdaman):
    layer_id = RasdamanSettings.layer_id
    host = RasdamanSettings.host
    headers = {"Authorization": BEARER_TOKEN}
    url = "/raster/hypos/wms/?&service=WMS&request=GetMap&layers={layer_id}&format=image%2Fpng&" \
          "transparent=true&version=1.3.0&width=256&height=256&time=%22{datetime}%22&crs=EPSG%3A3857&" \
          "bbox={bbox}&styles=log50_C1S3_32bit"


class RasdamanLocalVisualization(Rasdaman):
    layer_id = RasdamanLocalSettings.layer_id
    host = RasdamanLocalSettings.host
    url = "/rasdaman/ows?service=WMS&request=GetMap&layers={layer_id}&format=image%2Fpng&transparent=true&" \
          "version=1.3.0&width=256&height=256&time=%22{datetime}%22&crs=EPSG%3A3857&bbox={bbox}&" \
          "styles=log50_C1S3_32bit"
