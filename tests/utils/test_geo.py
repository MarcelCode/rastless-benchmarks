from benchmarks.utils import geo


def test_bounding_box():
    bbox = geo.BoundingBox(x_west=20.050735473632812, y_north=40.98223072018906, x_east=20.175704956054688,
                           y_south=40.878477727669704)

    bbox_proj = bbox.transform(3857)

    expected_bbox = geo.BoundingBox(x_west=2232037.6629554317, y_north=5009721.052324595, x_east=2245949.202103334,
                                    y_south=4994433.646667561, epsg=3857)

    assert bbox_proj == expected_bbox
