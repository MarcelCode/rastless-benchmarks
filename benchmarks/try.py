import requests

from benchmarks.settings import Settings, RastLessSettings
from benchmarks.utils.tools import geojson_file_to_dict, RandomGeometryGeojson


geojson = geojson_file_to_dict(Settings.aoi_geojson_file)
random_geometry_gen = RandomGeometryGeojson(geojson)
random_geometry_gen.generate_points()

if __name__ == '__main__':
    geometry = random_geometry_gen.get_point_geojson()

    body = {
        "statistic": "mean",
        "geometry": geometry
    }

    url = f"/layers/{RastLessSettings.layer_id}/statistic?token={RastLessSettings.access_token}"

    response = requests.post(RastLessSettings.host + url, json=body)
    print("neu")