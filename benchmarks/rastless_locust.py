import os
from locust import HttpUser, task, stats
from dotenv import load_dotenv

from benchmarks.settings import Settings, RastLessSettings
from benchmarks.utils.tools import RandomDate, RandomTile

load_dotenv()


class RastLessVisualization(HttpUser):
    host = RastLessSettings.host
    layer_id = RastLessSettings.rastless_layer_id
    access_token = os.getenv("RASTLESS_ACCESS_TOKEN")
    random_tile = RandomTile(Settings.bounding_box, Settings.min_zoom, Settings.max_zoom)
    random_dates = RandomDate(Settings.dates)

    @task
    def get_tile(self):
        tile = self.random_tile.get_tile()
        datetime = self.random_dates.get_date()
        datetime = datetime.replace("T", " ")  # This dataset is not stored as isodate
        self.client.get(
            f"/layers/{self.layer_id}/{datetime}/tile/{tile.z}/{tile.x}/{tile.y}.png?token={self.access_token}",
            name="tile"
        )
