from locust import HttpUser, task
import os
import locust.stats

from settings import Settings, RastLessSettings
from utils.tools import RandomDate, RandomTileByBBox, geojson_file_to_dict, RandomGeometryGeojson

locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 5
locust.stats.PERCENTILES_TO_REPORT = [0.25, 0.50, 0.75, 0.99]

geojson = geojson_file_to_dict(os.path.join(Settings.base_dir, Settings.aoi_geojson_file))
random_geometry_gen = RandomGeometryGeojson(geojson)
random_geometry_gen.generate_points()


class RastLess(HttpUser):
    host = RastLessSettings.host
    layer_id = RastLessSettings.layer_id
    access_token = RastLessSettings.access_token


class RastLessVisualization(RastLess):
    random_tile = RandomTileByBBox(bbox=Settings.bounding_box, min_zoom=Settings.min_zoom, max_zoom=Settings.max_zoom)
    random_dates = RandomDate(Settings.dates)

    @task
    def get_tile(self):
        tile = self.random_tile.get_tile()
        datetime = self.random_dates.get_date()
        datetime = datetime.replace("T", " ")  # This dataset is not stored as isodate
        url = f"/layers/{self.layer_id}/{datetime}/tile/{tile.z}/{tile.x}/{tile.y}.png?token={self.access_token}"
        with self.client.get(url, name="visualization", catch_response=True) as response:
            if response.headers.get("content-type") == "image/png" and len(response.content) > 10:
                response.success()


class RastLessAnalysis(RastLess):
    random_geometry = random_geometry_gen
    statistic = "mean"
    geometry_handler = None
    start_date = Settings.start_date.replace("T", " ")
    end_date = Settings().end_date.replace("T", " ")
    name = ""

    @task
    def get_timeseries(self):
        geometry = getattr(self.random_geometry, self.geometry_handler)()

        body = {
            "statistic": self.statistic,
            "geometry": geometry
        }

        url = f"/layers/{self.layer_id}/statistic?token={self.access_token}&temporal_resolution=daily" \
              f"&start_date={self.start_date}&end_date={self.end_date}"
        with self.client.post(url, json=body, name=self.name, catch_response=True) as response:
            if response.headers.get("content-type") == "application/json" and len(response.content) > 10:
                response.success()


class RastLessPointAnalysis(RastLessAnalysis):
    geometry_handler = "get_point_geojson"
    name = "timeseries-point"


class RastLessPolygonAnalysis(RastLessAnalysis):
    geometry_handler = "get_polygon_geojson"
    name = "timeseries-polygon"
