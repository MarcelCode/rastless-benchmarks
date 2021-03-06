from dataclasses import dataclass
from pyproj import Transformer
import mercantile


@dataclass
class BoundingBox:
    x_west: float
    y_north: float
    x_east: float
    y_south: float
    epsg: int = 4326

    def transform(self, epsg_out: int = 3857):
        t = Transformer.from_crs(f"epsg:{self.epsg}", f"epsg:{epsg_out}", always_xy=True)
        x_west_proj, y_north_proj = t.transform(self.x_west, self.y_north)
        x_east_proj, y_south_proj = t.transform(self.x_east, self.y_south)
        return BoundingBox(x_west_proj, y_north_proj, x_east_proj, y_south_proj, epsg=epsg_out)


@dataclass
class Tile:
    z: int
    x: int
    y: int

    @property
    def xy_bounds(self):
        return mercantile.xy_bounds(self.x, self.y, self.z)

    @property
    def str_xy_bounds(self):
        bounds = self.xy_bounds
        return ",".join([str(bounds.left), str(bounds.bottom), str(bounds.right), str(bounds.top)])


@dataclass
class Point:
    x: float
    y: float
    epsg: int = 4326

    def transform(self, epsg_out: int = 3857):
        t = Transformer.from_crs(f"epsg:{self.epsg}", f"epsg:{epsg_out}", always_xy=True)
        x, y = t.transform(self.x, self.y)
        return Point(x, y, epsg=epsg_out)
