import requests

from benchmarks.settings import Settings, RasdamanSettings
from benchmarks.utils.tools import geojson_file_to_dict, RandomGeometryGeojson
from benchmarks.utils.auth import get_keycloak_bearer_token


geojson = geojson_file_to_dict(Settings.aoi_geojson_file)
random_geometry_gen = RandomGeometryGeojson(geojson)
random_geometry_gen.generate_points()

if __name__ == '__main__':
    bearer_token = get_keycloak_bearer_token(RasdamanSettings)
    geometry = random_geometry_gen.get_point()
    layer_id = "TUR_alb_banja_hypos_public_32bit"

    url = f"/raster/hypos/wcps/point/{geometry.x}/{geometry.y}/?layers={layer_id}"

    response = requests.get(RasdamanSettings.host + url, headers={"Authorization": bearer_token})
    print("neu")


# https://api-layer.eomap.com/raster/hypos/wcps/point/20.101486162865427/40.94121249747613/?layers=SDD_alb_banja_hypos_public_32bit