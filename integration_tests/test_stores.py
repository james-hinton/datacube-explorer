from collections import Counter
from datetime import datetime

from dateutil import tz
from shapely import geometry as geo

from cubedash.summary import TimePeriodOverview, SummaryStore
from datacube.model import Range


def _overview():
    orig = TimePeriodOverview(
        1234,
        Counter([
            datetime(2017, 1, 2, tzinfo=tz.tzutc()),
            datetime(2017, 1, 3, tzinfo=tz.tzutc()),
            datetime(2017, 1, 3, tzinfo=tz.tzutc()),
            datetime(2017, 1, 1, tzinfo=tz.tzutc())]),
        {},
        timeline_period='day',
        time_range=Range(
            datetime(2017, 1, 2, tzinfo=tz.tzutc()),
            datetime(2017, 2, 3, tzinfo=tz.tzutc())
        ),
        footprint_geometry=geo.Polygon([
            # ll:
            (-29.882024, 113.105949),
            # lr:
            (-29.930607, 115.464187),
            # ur:
            (-27.849244, 115.494523),
            # ul
            (-27.804641, 113.18267),
        ]),
        footprint_count=0,
        newest_dataset_creation_time=datetime(2018, 1, 1, 1, 1, 1, tzinfo=tz.tzutc()),
        crses={'epsg:1234'}
    )
    return orig


def test_get_null(summary_store: SummaryStore):
    """
    An area with nothing generated should come back as null.

    (It's important for us to distinguish between an area with zero datasets
    and an area where the summary/extent has not been generated.)
    """
    loaded = summary_store.get('some_product', 2019, 4, None)
    assert loaded is None


def test_srid_lookup(summary_store: SummaryStore):
    srid = summary_store._target_srid()
    assert srid is not None
    assert isinstance(srid, int)

    srid2 = summary_store._target_srid()
    assert srid == srid2

    assert summary_store._get_srid_name(srid) == 'EPSG:4326'

    # Cached?
    cache_hits = summary_store._get_srid_name.cache_info().hits
    assert summary_store._get_srid_name(srid) == 'EPSG:4326'
    assert summary_store._get_srid_name.cache_info().hits > cache_hits

