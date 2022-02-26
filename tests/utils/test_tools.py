from mercantile import Tile

from benchmarks.utils import tools
from benchmarks.utils.geo import BoundingBox


def test_get_random_tile():
    bbox = BoundingBox(20.050735473632812, 40.98223072018906,
                       20.175704956054688, 40.878477727669704,
                       epsg=4326)
    min_zoom: int = 10
    max_zoom: int = 15

    random_tile = tools.RandomTile(bbox, min_zoom, max_zoom)

    tiles = [random_tile.get_tile() for _ in range(3)]
    expected_tiles = [Tile(x=18219, y=12296, z=15),
                      Tile(x=1138, y=768, z=11),
                      Tile(x=18212, y=12294, z=15)]

    assert tiles == expected_tiles


def test_get_random_tile_same_init():
    """Tests that 2 initialized RandomTile Classes have the same random seed output"""
    bbox = BoundingBox(20.050735473632812, 40.98223072018906,
                       20.175704956054688, 40.878477727669704,
                       epsg=4326)
    min_zoom: int = 10
    max_zoom: int = 15

    random_tile = tools.RandomTile(bbox, min_zoom, max_zoom)
    random_tile2 = tools.RandomTile(bbox, min_zoom, max_zoom)

    for _ in range(3):
        assert random_tile.get_tile() == random_tile2.get_tile()


def test_get_random_date():
    dates = ["2020-01-01T11:00:00", "2021-01-01T11:00:00", "2022-01-01T11:00:00", "2019-01-01T11:00:00"]

    random_date = tools.RandomDate(dates)
    new_dates = [random_date.get_date() for _ in range(3)]
    expected_new_dates = ['2020-01-01T11:00:00', '2020-01-01T11:00:00', '2022-01-01T11:00:00']

    assert new_dates == expected_new_dates
