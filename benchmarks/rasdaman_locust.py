from locust import HttpUser, task
import random

random.seed(42)


class RasdamanVisualization(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/helleeo")
        self.client.get("/world")


class RasdamanAnalysis(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/heleelo")
        self.client.get("/world")
