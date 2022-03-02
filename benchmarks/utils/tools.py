import json
from random import Random
import mercantile
from typing import List
from shapely.geometry import shape, Point

from benchmarks.utils.geo import BoundingBox, Tile, Point as GeomPoint


class RandomTileByBBox:
    def __init__(self, bbox: BoundingBox, min_zoom: int, max_zoom: int):
        self.random = Random(42)
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

        if not bbox.epsg == 4326:
            self.bbox = bbox.transform(4326)
        else:
            self.bbox = bbox

    def get_tile(self) -> mercantile.Tile:
        random_zoom = self.random.randint(self.min_zoom, self.max_zoom)

        random_x_coord = self.random.uniform(self.bbox.x_east, self.bbox.x_west)
        random_y_coord = self.random.uniform(self.bbox.y_north, self.bbox.y_south)

        return mercantile.tile(random_x_coord, random_y_coord, random_zoom)


class RandomTile:
    def __init__(self, tiles: List[Tile]):
        self.random = Random(42)
        self.tiles = tiles

    def get_tile(self) -> Tile:
        i = self.random.randint(0, len(self.tiles) - 1)
        return self.tiles[i]


class RandomDate:
    def __init__(self, dates: List[str]):
        self.random = Random(42)
        self.dates = dates

    def get_date(self):
        i = self.random.randint(0, len(self.dates) - 1)
        return self.dates[i]


class RandomGeometryGeojson:
    def __init__(self, polygon_geojson: dict):
        self.random = Random(42)
        self.polygon = shape(polygon_geojson)
        self.points = []

    def generate_points(self, number: int = 1000):
        random = Random(42)
        minx, miny, maxx, maxy = self.polygon.bounds

        while len(self.points) < number:
            pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if self.polygon.contains(pnt):
                self.points.append(GeomPoint(pnt.x, pnt.y))

    def get_point(self) -> GeomPoint:
        i = self.random.randint(0, len(self.points) - 1)
        return self.points[i]

    def get_point_geojson(self):
        point = self.get_point()
        return {
            "type": "Point",
            "coordinates": [
                point.x,
                point.y
            ]
        }

    def get_polygon_geojson(self, size_degree: float = 0.003):
        point = self.get_point()
        coordinates = []
        for calc in [[-size_degree, -size_degree], [-size_degree, size_degree], [size_degree, size_degree],
                     [size_degree, -size_degree], [-size_degree, -size_degree]]:
            coordinates.append([point.x + calc[0], point.y + calc[1]])
        return {
            "type": "Polygon",
            "coordinates": [coordinates]
        }


def geojson_file_to_dict(geojson_file_path) -> dict:
    with open(geojson_file_path) as fobj:
        data = json.load(fobj)

    return data["features"][0]["geometry"]


if __name__ == '__main__':
    geojson = geojson_file_to_dict("/home/marcel/PycharmProjects/rastless-benchmarks/data/banja_dam.geojson")

    random_points = RandomGeometryGeojson(geojson)
    random_points.generate_points()

    print("test")
