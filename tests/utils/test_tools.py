import pytest
from mercantile import Tile
import os

from benchmarks.utils import tools
from benchmarks.settings import Settings


def test_get_random_tile():
    tiles = [
        Tile(11, 1138, 768), Tile(11, 1140, 770), Tile(11, 1140, 770), Tile(x=2276, y=1536, z=12),
        Tile(x=2277, y=1536, z=12), Tile(x=2277, y=1537, z=12), Tile(x=2276, y=1537, z=12), Tile(12, 2280, 1540)
    ]

    random_tile = tools.RandomTile(tiles)

    tiles = [random_tile.get_tile() for _ in range(3)]
    expected_tiles = [Tile(x=11, y=1140, z=770),
                      Tile(x=11, y=1138, z=768),
                      Tile(x=2277, y=1536, z=12)]

    assert tiles == expected_tiles


def test_get_random_tile_same_init():
    """Tests that 2 initialized RandomTile Classes have the same random seed output"""
    tiles = [
        Tile(11, 1138, 768), Tile(11, 1140, 770), Tile(11, 1140, 770), Tile(x=2276, y=1536, z=12),
        Tile(x=2277, y=1536, z=12), Tile(x=2277, y=1537, z=12), Tile(x=2276, y=1537, z=12), Tile(12, 2280, 1540)
    ]

    random_tile = tools.RandomTile(tiles)
    random_tile2 = tools.RandomTile(tiles)

    for _ in range(3):
        assert random_tile.get_tile() == random_tile2.get_tile()


def test_get_random_date():
    dates = ["2020-01-01T11:00:00", "2021-01-01T11:00:00", "2022-01-01T11:00:00", "2019-01-01T11:00:00"]

    random_date = tools.RandomDate(dates)
    new_dates = [random_date.get_date() for _ in range(3)]
    expected_new_dates = ['2020-01-01T11:00:00', '2020-01-01T11:00:00', '2022-01-01T11:00:00']

    assert new_dates == expected_new_dates


@pytest.fixture
def random_geometry():
    geojson = tools.geojson_file_to_dict(os.path.join(Settings.base_dir, "data/banja_dam.geojson"))
    rand_geometry = tools.RandomGeometryGeojson(geojson)
    rand_geometry.generate_points(10)

    return rand_geometry


def test_get_random_point_geojson(random_geometry):
    expected_geojson = {
        "type": "Point",
        "coordinates": [20.11335972970832, 40.929896080240404]
    }

    assert random_geometry.get_point_geojson() == expected_geojson


def test_get_random_polygon_geojson(random_geometry):
    expected_geojson = {
        "type": "Polygon",
        "coordinates": [[[20.11035972970832, 40.926896080240404],
                         [20.11035972970832, 40.932896080240404],
                         [20.11635972970832, 40.932896080240404],
                         [20.11635972970832, 40.926896080240404],
                         [20.11035972970832, 40.926896080240404]]]
    }

    assert random_geometry.get_polygon_geojson() == expected_geojson
