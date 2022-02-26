from locust import HttpUser, task

from benchmarks.settings import Settings, RasdamanSettings


class RasdamanVisualization(HttpUser):
    host = RasdamanSettings.host

    @task
    def hello_world(self):
        self.client.get('raster/hypos/wms/?&service=WMS&request=GetMap&layers=TUR_alb_banja_hypos_public_32bit&format=image/png&transparent=true&version=1.3.0&width=256&height=256&time="2021-10-27T09:17:07"&crs=EPSG:3857&bbox=2238076.188189961,4999593.14607681,2240522.1730950847,5002039.130981933&styles=log50_C1S3_32bit')

    def on_start(self):
        self.login()

    def login(self):
        login_url = "/admin/login/"
        self.client.get(login_url)

        csrf_token = self.client.cookies["csrftoken"]

        payload = {"username": RasdamanSettings.username, "password": RasdamanSettings.password,
                   "csrfmiddlewaretoken": csrf_token, "next": "/admin/"}

        self.client.post(login_url, data=payload)
