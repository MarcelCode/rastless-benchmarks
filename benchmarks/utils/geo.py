from dataclasses import dataclass
from pyproj import Transformer


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


