from random import Random
import mercantile
from typing import List

from benchmarks.utils.geo import BoundingBox


class RandomTile:
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


class RandomDate:
    def __init__(self, dates: List[str]):
        self.random = Random(42)
        self.dates = dates

    def get_date(self, ):
        i = self.random.randint(0, len(self.dates) - 1)
        return self.dates[i]
