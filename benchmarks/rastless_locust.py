from locust import HttpUser, task
import requests

from benchmarks.settings import Settings, RastLessSettings
from benchmarks.utils.tools import RandomDate, RandomTile, geojson_file_to_dict, RandomGeometryGeojson


class RastLess(HttpUser):
    host = RastLessSettings.host
    layer_id = RastLessSettings.layer_id
    access_token = RastLessSettings.access_token


class RastLessVisualization(RastLess):
    random_tile = RandomTile(Settings.tiles)
    random_dates = RandomDate(Settings.dates)

    @task
    def get_tile(self):
        tile = self.random_tile.get_tile()
        datetime = self.random_dates.get_date()
        datetime = datetime.replace("T", " ")  # This dataset is not stored as isodate
        url = f"/layers/{self.layer_id}/{datetime}/tile/{tile.z}/{tile.x}/{tile.y}.png?token={self.access_token}"
        self.client.get(url, name="tile")


geojson = geojson_file_to_dict(Settings.aoi_geojson_file)
random_geometry_gen = RandomGeometryGeojson(geojson)
random_geometry_gen.generate_points()


class RastLessPointAnalysis(RastLess):
    random_geometry = random_geometry_gen
    statistic = "mean"

    @task
    def get_timeseries_for_point(self):
        geometry = self.random_geometry.get_point_geojson()

        body = {
            "statistic": self.statistic,
            "geometry": geometry
        }

        url = f"/layers/{self.layer_id}/statistic?token={self.access_token}"
        self.client.post(url, json=body, name="timeseries")

