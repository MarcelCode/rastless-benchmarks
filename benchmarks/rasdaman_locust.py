from locust import HttpUser, task, constant_throughput
from urllib.parse import quote
import os
import locust.stats

from settings import RasdamanSettings, RasdamanLocalSettings, Settings
from utils.auth import get_keycloak_bearer_token
from utils.tools import RandomDate, RandomTile, geojson_file_to_dict, RandomGeometryGeojson

locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 5
locust.stats.PERCENTILES_TO_REPORT = [0.25, 0.50, 0.75, 0.99]

BEARER_TOKEN = get_keycloak_bearer_token(RasdamanSettings)

geojson = geojson_file_to_dict(os.path.join(Settings.base_dir, Settings.aoi_geojson_file))
random_geometry_gen = RandomGeometryGeojson(geojson)
random_geometry_gen.generate_points()


class Rasdaman(HttpUser):
    random_tile = RandomTile(Settings.tiles)
    random_dates = RandomDate(Settings.dates)
    wait_time = constant_throughput(20)

    host = ""
    layer_id = ""
    url = ""
    headers = {}
    name = ""

    @task
    def get_tile(self):
        tile = self.random_tile.get_tile()
        datetime = self.random_dates.get_date()

        request_url = self.url.format(layer_id=self.layer_id, datetime=datetime, bbox=tile.str_xy_bounds)

        self.client.get(request_url, headers=self.headers, name=self.name)


class RasdamanProxyVisualization(Rasdaman):
    layer_id = RasdamanSettings.layer_id
    host = RasdamanSettings.host
    headers = {"Authorization": BEARER_TOKEN}
    url = "/raster/hypos/wms/?&service=WMS&request=GetMap&layers={layer_id}&format=image%2Fpng&" \
          "transparent=true&version=1.3.0&width=256&height=256&time=%22{datetime}%22&crs=EPSG%3A3857&" \
          "bbox={bbox}&styles=log50_C1S3_32bit"
    name = "visualization"


class RasdamanLocalVisualization(Rasdaman):
    layer_id = RasdamanLocalSettings.layer_id
    host = RasdamanLocalSettings.host
    url = "/rasdaman/ows?service=WMS&request=GetMap&layers={layer_id}&format=image%2Fpng&transparent=true&" \
          "version=1.3.0&width=256&height=256&time=%22{datetime}%22&crs=EPSG%3A3857&bbox={bbox}&" \
          "styles=log50_C1S3_32bit"
    name = "visualization"


class RasdamanProxyPointAnalysis(HttpUser):
    layer_id = RasdamanSettings.layer_id
    host = RasdamanSettings.host
    random_geometry = random_geometry_gen
    bearer_token = BEARER_TOKEN

    @task
    def get_timeseries(self):
        geometry = self.random_geometry.get_point()
        url = f"/raster/hypos/wcps/point/{geometry.x}/{geometry.y}/?layers={self.layer_id}"
        self.client.get(url, headers={"Authorization": self.bearer_token},
                        name="timeseries-point")


class RasdamanProxyPolygonAnalysis(HttpUser):
    layer_id = RasdamanSettings.layer_id
    host = RasdamanSettings.host
    random_geometry = random_geometry_gen
    bearer_token = BEARER_TOKEN

    @task
    def get_timeseries(self):
        geometry = self.random_geometry.get_polygon_geojson()

        body = {
            "feature": geometry
        }

        url = f"/raster/hypos/wcps/polygon/?layers={self.layer_id}"
        self.client.post(url, headers={"Authorization": self.bearer_token}, json=body,
                         name="timeseries-polygon")


class RasdamanLocalPointAnalysis(HttpUser):
    layer_id = RasdamanLocalSettings.layer_id
    host = RasdamanLocalSettings.host
    random_geometry = random_geometry_gen
    start_date = Settings.start_date
    end_date = Settings().end_date

    @task
    def get_timeseries(self):
        point = self.random_geometry.get_point()
        point_web_mercator = point.transform()

        query = f'for $c in ( {self.layer_id} ) return encode($c[ansi("{self.start_date}":"{self.end_date}"),' \
                f' X({point_web_mercator.x}), Y({point_web_mercator.y})],"json")'
        url = f'/rasdaman/ows?VERSION=2.0.1&SERVICE=WCPS&QUERY={quote(query)}'

        self.client.get(url, name="timeseries-point")


class RasdamanLocalPolygonAnalysis(HttpUser):
    layer_id = RasdamanLocalSettings.layer_id
    host = RasdamanLocalSettings.host
    random_geometry = random_geometry_gen
    start_date = Settings.start_date
    end_date = Settings().end_date

    @task
    def get_timeseries(self):
        polygon_formatted, x_bounds, y_bounds = self.random_geometry.get_polygon_rasdaman()

        query = f'for $c in ( {self.layer_id} ) return encode( coverage myTimeSeries over $date' \
                f' ansi(imageCrsDomain($c[ansi("{self.start_date}":"{self.end_date}")], ansi)) values' \
                f' avg( clip( $c[ansi($date), X({x_bounds}), Y({y_bounds})],' \
                f' {polygon_formatted} )), "json")'

        url = f'/rasdaman/ows?VERSION=2.0.1&SERVICE=WCPS&QUERY={quote(query)}'

        self.client.get(url, name="timeseries-polygon")
