from locust import HttpUser, task

from benchmarks.settings import RasdamanSettings, RasdamanLocalSettings, Settings
from benchmarks.utils.auth import get_keycloak_bearer_token
from benchmarks.utils.tools import RandomDate, RandomTile

BEARER_TOKEN = get_keycloak_bearer_token(RasdamanSettings)


class RasdamanProxyVisualization(HttpUser):
    host = RasdamanSettings.host
    layer_id = RasdamanLocalSettings.layer_id
    random_tile = RandomTile(Settings.tiles)
    random_dates = RandomDate(Settings.dates)
    bearer_token = BEARER_TOKEN

    @task
    def get_tile(self):
        tile = self.random_tile.get_tile()
        datetime = self.random_dates.get_date()

        url = f"/raster/hypos/wms/?&service=WMS&request=GetMap&layers={self.layer_id}&format=image%2Fpng&" \
              f"transparent=true&version=1.3.0&width=256&height=256&time=%22{datetime}%22&crs=EPSG%3A3857&" \
              f"bbox={tile.str_xy_bounds}&styles=log50_C1S3_32bit"

        self.client.get(url, headers={"Authorization": self.bearer_token}, name="tile")


class RasdamanLocalVisualization(HttpUser):
    host = RasdamanLocalSettings.host
    layer_id = RasdamanLocalSettings.layer_id
    random_tile = RandomTile(Settings.tiles)
    random_dates = RandomDate(Settings.dates)

    @task
    def get_tile(self):
        tile = self.random_tile.get_tile()
        datetime = self.random_dates.get_date()

        url = f"/rasdaman/ows?service=WMS&request=GetMap&layers={self.layer_id}&format=image%2Fpng&transparent=true&" \
              f"version=1.3.0&width=256&height=256&time=%22{datetime}%22&crs=EPSG%3A3857&bbox={tile.str_xy_bounds}&" \
              f"styles=log50_C1S3_32bit"

        self.client.get(url, name="tile")
