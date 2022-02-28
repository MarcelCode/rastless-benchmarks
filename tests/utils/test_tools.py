from mercantile import Tile

from benchmarks.utils import tools


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
