from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os

from benchmarks.utils.geo import BoundingBox

load_dotenv()


@dataclass
class Settings:
    base_dir = Path(__file__).resolve().parent.parent
    bounding_box: BoundingBox = BoundingBox(20.050735473632812, 40.98223072018906,
                                            20.175704956054688, 40.878477727669704,
                                            epsg=4326)
    dates = ['2017-08-20T09:22:56', '2021-05-21T09:39:11', '2017-09-14T09:36:54', '2021-01-19T09:23:01',
             '2016-08-17T09:22:57', '2016-11-03T09:37:03', '2018-08-30T09:35:20', '2020-03-12T09:39:08',
             '2021-10-27T09:17:07', '2020-01-17T09:39:04', '2016-12-03T09:34:18', '2018-08-10T09:37:42',
             '2016-08-26T09:16:50', '2016-08-05T09:37:33', '2016-06-07T09:16:22', '2018-11-04T09:16:37',
             '2019-08-25T09:39:15', '2019-01-12T09:39:06', '2018-04-02T09:33:45', '2017-11-28T09:33:29',
             '2020-01-02T09:39:05', '2019-12-13T09:39:05', '2019-06-16T09:16:31', '2020-05-26T09:39:16',
             '2020-01-01T09:23:05', '2018-01-12T09:33:50', '2019-05-06T09:22:20', '2020-04-16T09:39:10',
             '2019-03-19T09:22:27', '2019-10-06T09:17:04', '2021-09-23T09:39:08', '2018-10-26T09:22:46',
             '2018-12-29T09:22:45', '2017-11-24T09:23:03', '2017-12-19T09:16:53', '2019-01-02T09:39:05',
             '2020-02-18T09:22:53', '2016-01-08T09:46:11', '2019-07-18T09:16:38', '2016-10-13T09:17:01',
             '2020-08-24T09:39:16', '2017-10-19T09:32:14', '2016-11-30T09:17:01', '2018-10-03T09:16:27',
             '2017-08-15T09:38:16', '2018-07-16T09:32:20', '2016-10-14T09:38:29', '2021-09-09T09:16:57',
             '2017-07-28T09:16:37', '2017-08-13T09:16:44', '2021-05-11T09:22:24', '2021-09-25T09:17:00',
             '2019-03-18T09:39:09', '2017-10-09T09:33:40', '2019-06-21T09:39:14', '2020-07-20T09:16:35',
             '2019-03-03T09:39:05', '2020-03-30T09:16:24', '2016-05-13T09:22:24', '2018-02-05T09:16:33',
             '2018-11-13T09:39:05', '2020-04-06T09:22:32', '2018-09-24T09:22:33', '2020-06-30T09:39:13',
             '2021-01-28T09:16:50', '2021-06-15T09:39:11', '2021-07-05T09:39:12', '2016-03-28T09:34:27',
             '2021-03-02T09:39:10', '2021-07-30T09:39:14', '2021-05-11T09:39:10', '2020-03-21T09:22:40',
             '2016-03-19T09:16:29', '2020-03-14T09:16:33', '2021-10-28T09:39:15', '2016-08-15T09:32:18',
             '2018-10-14T09:30:31', '2020-12-17T09:39:06', '2019-04-20T09:22:18', '2017-11-01T09:16:59',
             '2021-01-03T09:23:08', '2020-08-28T09:23:00', '2020-02-16T09:39:04', '2021-03-17T09:39:10',
             '2019-08-30T09:39:11', '2019-09-27T09:23:12', '2018-05-12T09:15:44', '2017-07-19T09:22:44',
             '2016-07-25T09:16:41', '2017-07-31T09:36:07', '2019-01-27T09:39:11', '2016-10-24T09:33:41',
             '2019-09-14T09:39:11', '2021-04-21T09:39:06', '2016-09-04T09:32:32', '2021-08-14T09:39:11',
             '2021-01-16T09:39:10', '2018-07-01T09:35:25', '2016-05-22T09:16:18', '2019-11-18T09:39:12']  # 100 Dates
    min_zoom: int = 10
    max_zoom: int = 15


@dataclass
class RastLessSettings:
    host = "https://rastless.dev.eomap.com"
    rastless_layer_id = "38ee856d-6888-4af1-98a1-dc8906f240e4"
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


@dataclass
class RasdamanLocalSettings(RasdamanSettings):
    host = os.getenv("RASDAMAN_LOCAL_HOST")
