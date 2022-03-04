from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os

from benchmarks.utils.geo import BoundingBox, Tile

load_dotenv()


@dataclass
class Settings:
    base_dir = Path(__file__).resolve().parent.parent
    bounding_box = BoundingBox(20.050735473632812, 40.98223072018906,
                               20.175704956054688, 40.878477727669704,
                               epsg=4326)
    dates = ['2016-01-08T09:46:11',
             '2016-03-19T09:16:29',
             '2016-03-28T09:34:27',
             '2016-05-13T09:22:24',
             '2016-05-22T09:16:18',
             '2016-06-07T09:16:22',
             '2016-07-25T09:16:41',
             '2016-08-05T09:37:33',
             '2016-08-15T09:32:18',
             '2016-08-17T09:22:57',
             '2016-08-26T09:16:50',
             '2016-09-04T09:32:32',
             '2016-10-13T09:17:01',
             '2016-10-14T09:38:29',
             '2016-10-24T09:33:41',
             '2016-11-03T09:37:03',
             '2016-11-30T09:17:01',
             '2016-12-03T09:34:18',
             '2017-07-19T09:22:44',
             '2017-07-28T09:16:37',
             '2017-07-31T09:36:07',
             '2017-08-13T09:16:44',
             '2017-08-15T09:38:16',
             '2017-08-20T09:22:56',
             '2017-09-14T09:36:54',
             '2017-10-09T09:33:40',
             '2017-10-19T09:32:14',
             '2017-11-01T09:16:59',
             '2017-11-24T09:23:03',
             '2017-11-28T09:33:29',
             '2017-12-19T09:16:53',
             '2018-01-12T09:33:50',
             '2018-02-05T09:16:33',
             '2018-04-02T09:33:45',
             '2018-05-12T09:15:44',
             '2018-07-01T09:35:25',
             '2018-07-16T09:32:20',
             '2018-08-10T09:37:42',
             '2018-08-30T09:35:20',
             '2018-09-24T09:22:33',
             '2018-10-03T09:16:27',
             '2018-10-14T09:30:31',
             '2018-10-26T09:22:46',
             '2018-11-04T09:16:37',
             '2018-11-13T09:39:05',
             '2018-12-29T09:22:45',
             '2019-01-02T09:39:05',
             '2019-01-12T09:39:06',
             '2019-01-27T09:39:11',
             '2019-03-03T09:39:05',
             '2019-03-18T09:39:09',
             '2019-03-19T09:22:27',
             '2019-04-20T09:22:18',
             '2019-05-06T09:22:20',
             '2019-06-16T09:16:31',
             '2019-06-21T09:39:14',
             '2019-07-18T09:16:38',
             '2019-08-25T09:39:15',
             '2019-08-30T09:39:11',
             '2019-09-14T09:39:11',
             '2019-09-27T09:23:12',
             '2019-10-06T09:17:04',
             '2019-11-18T09:39:12',
             '2019-12-13T09:39:05',
             '2020-01-01T09:23:05',
             '2020-01-02T09:39:05',
             '2020-01-17T09:39:04',
             '2020-02-16T09:39:04',
             '2020-02-18T09:22:53',
             '2020-03-12T09:39:08',
             '2020-03-14T09:16:33',
             '2020-03-21T09:22:40',
             '2020-03-30T09:16:24',
             '2020-04-06T09:22:32',
             '2020-04-16T09:39:10',
             '2020-05-26T09:39:16',
             '2020-06-30T09:39:13',
             '2020-07-20T09:16:35',
             '2020-08-24T09:39:16',
             '2020-08-28T09:23:00',
             '2020-12-17T09:39:06',
             '2021-01-03T09:23:08',
             '2021-01-16T09:39:10',
             '2021-01-19T09:23:01',
             '2021-01-28T09:16:50',
             '2021-03-02T09:39:10',
             '2021-03-17T09:39:10',
             '2021-04-21T09:39:06',
             '2021-05-11T09:22:24',
             '2021-05-11T09:39:10',
             '2021-05-21T09:39:11',
             '2021-06-15T09:39:11',
             '2021-07-05T09:39:12',
             '2021-07-30T09:39:14',
             '2021-08-14T09:39:11',
             '2021-09-09T09:16:57',
             '2021-09-23T09:39:08',
             '2021-09-25T09:17:00',
             '2021-10-27T09:17:07',
             '2021-10-28T09:39:15']  # 100 Dates
    tiles = [
        Tile(11, 1138, 768), Tile(11, 1140, 770), Tile(11, 1140, 770), Tile(x=2276, y=1536, z=12),
        Tile(x=2277, y=1536, z=12), Tile(x=2277, y=1537, z=12), Tile(x=2276, y=1537, z=12), Tile(12, 2280, 1540),
        Tile(12, 2281, 1540), Tile(x=4552, y=3072, z=13), Tile(x=4553, y=3072, z=13), Tile(x=4553, y=3073, z=13),
        Tile(x=4552, y=3073, z=13), Tile(x=4554, y=3073, z=13), Tile(x=4553, y=3074, z=13), Tile(x=4554, y=3074, z=13),
        Tile(x=4561, y=3080, z=13), Tile(x=4562, y=3080, z=13), Tile(x=4561, y=3081, z=13), Tile(x=9104, y=6144, z=14),
        Tile(x=9105, y=6144, z=14), Tile(x=9105, y=6145, z=14), Tile(x=9104, y=6145, z=14), Tile(x=9106, y=6144, z=14),
        Tile(x=9107, y=6144, z=14), Tile(x=9107, y=6145, z=14), Tile(x=9106, y=6145, z=14),
        Tile(x=9106, y=6146, z=14), Tile(x=9107, y=6146, z=14), Tile(x=9107, y=6147, z=14), Tile(x=9106, y=6147, z=14),
        Tile(x=9108, y=6147, z=14), Tile(x=9108, y=6148, z=14), Tile(x=9107, y=6148, z=14), Tile(x=9109, y=6148, z=14),
        Tile(x=9109, y=6149, z=14), Tile(x=9122, y=6161, z=14), Tile(x=9123, y=6161, z=14), Tile(x=9124, y=6161, z=14),
        Tile(x=9123, y=6162, z=14)
    ]
    min_zoom: int = 10
    max_zoom: int = 15
    aoi_geojson_file = "data/banja_dam.geojson"
    start_date = '2019-03-18T09:39:09'
    entries = 25

    @property
    def end_date(self):
        start_date_index = self.dates.index(self.start_date)
        return self.dates[start_date_index + self.entries - 1]


@dataclass
class RastLessSettings:
    host = "https://rastless.dev.eomap.com"
    layer_id = "38ee856d-6888-4af1-98a1-dc8906f240e4"
    access_token = os.getenv("RASTLESS_ACCESS_TOKEN")


@dataclass
class RasdamanSettings:
    host = "https://api-layer.eomap.com"
    username = os.getenv("RASDAMAN_USERNAME")
    password = os.getenv("RASDAMAN_PASSWORD")
    keycloak_client_id = os.getenv("RASDAMAN_CLIENT_ID")
    keycloak_client_secret = os.getenv("RASDAMAN_CLIENT_SECRET")
    keycloak_url = "https://auth.eomap.com/auth/"
    keycloak_realm_name = "eomap"
    layer_id = "TUR_alb_banja_hypos_public_32bit"


@dataclass
class RasdamanLocalSettings(RasdamanSettings):
    host = "http://127.0.0.1:5255"
