from locust import HttpUser, task

from benchmarks.settings import RasdamanSettings, RasdamanLocalSettings
from benchmarks.utils.auth import get_keycloak_bearer_token

BEARER_TOKEN = get_keycloak_bearer_token(RasdamanSettings)


class RasdamanVisualization(HttpUser):
    host = RasdamanSettings.host
    bearer_token = BEARER_TOKEN

    @task
    def get_tile(self):
        self.client.get(
            "/raster/hypos/wms/?&service=WMS&request=GetMap&layers=TUR_alb_banja_hypos_public_32bit&format=image%2Fpng&transparent=true&version=1.3.0&width=256&height=256&time=%222021-10-28T09:39:15%22&crs=EPSG%3A3857&bbox=2240522.1730950847,4997147.161171682,2242968.158000212,4999593.14607681&styles=log50_C1S3_32bit",
            headers={"Authorization": self.bearer_token},
            name="tile"
        )


class RasdamanLocalVisualization(HttpUser):
    host = RasdamanLocalSettings.host

    @task
    def get_tile(self):
        self.client.get(
            "?&service=WMS&request=GetMap&layers=TUR_alb_banja_hypos_public_32bit&format=image%2Fpng&transparent=true&version=1.3.0&width=256&height=256&time=%222021-10-28T09:39:15%22&crs=EPSG%3A3857&bbox=2240522.1730950847,4997147.161171682,2242968.158000212,4999593.14607681&styles=log50_C1S3_32bit",
            name="tile"
        )
