import requests
from urllib.parse import quote

from benchmarks.settings import Settings, RasdamanLocalSettings, RasdamanSettings
from benchmarks.utils.tools import geojson_file_to_dict, RandomGeometryGeojson
from benchmarks.utils.auth import get_keycloak_bearer_token


geojson = geojson_file_to_dict(Settings.aoi_geojson_file)
random_geometry_gen = RandomGeometryGeojson(geojson)
random_geometry_gen.generate_points()

if __name__ == '__main__':
    layer_id = "TUR_alb_banja_hypos_public_32bit"
    point = random_geometry_gen.get_point()
    bearer_token = get_keycloak_bearer_token(RasdamanSettings)
    start_date = "2016-01-08T09:46:11"
    end_date = "2022-02-25T09:39:13"

    polygon_formatted, x_bounds, y_bounds = random_geometry_gen.get_polygon_rasdaman()

    query = f'for $c in ( {layer_id} ) return encode( coverage myTimeSeries over $date' \
            f' ansi(imageCrsDomain($c[ansi("{start_date}":"{end_date}")], ansi)) values' \
            f' avg( clip( $c[ansi($date), X({x_bounds}), Y({y_bounds})],' \
            f' {polygon_formatted} )), "json")'
    url = f'http://127.0.0.1:5255/rasdaman/ows?VERSION=2.0.1&SERVICE=WCPS&QUERY={quote(query)}'

    response = requests.get(url)
    print("neu")


# 'http://127.0.0.1:5255/rasdaman/ows?VERSION=2.0.1&SERVICE=WCPS&QUERY=for $c in ( TUR_alb_banja_hypos_public_32bit ) return encode( coverage myTimeSeries over $date ansi(imageCrsDomain($c[ansi("2016-01-08T09:46:11":"2022-02-25T09:39:13")], ansi)) values avg( clip( $c[ansi($date), X(2237997.9:2238665.9), Y(5002772.5:5003656.6)], POLYGON ((2237997.9 5002772.5, 2237997.9 5003656.6, 2238665.9 5003656.6, 2238665.9 5002772.5, 2237997.9 5002772.5)))), "json")'