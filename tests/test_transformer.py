from pathlib import Path

from red_mantis.core.transformer import cluster_by_identity, cluster_by_distance, split_by_date
from red_mantis.models.gps import Decimal
from red_mantis.models.photo import Metadata as PhotoMetadata


def _make_photo(lat: float | None, lon: float | None, name: str = "img.jpg", date: str | None = None):
    gps = Decimal(latitude=lat, longitude=lon) if lat is not None and lon is not None else None
    return PhotoMetadata(img_path=Path(name), gps_metadata=gps, date_taken=date)


def test_cluster_by_identity_basic():
    p1 = _make_photo(51.0, -0.1, "a.jpg")
    p2 = _make_photo(52.0, -0.2, "b.jpg")

    clusters = cluster_by_identity([p1, p2])

    assert len(clusters) == 2

    # centers should match each photo's gps_metadata
    c1 = clusters[0].get_center()
    c2 = clusters[1].get_center()
    assert c1.get_latitude() == 51.0
    assert c2.get_longitude() == -0.2

    # photos preserved in cluster
    assert clusters[0].get_photos()[0] is p1
    assert clusters[1].get_photos()[0] is p2


def test_cluster_by_identity_none_gps():
    p = _make_photo(None, None, "no_gps.jpg")
    clusters = cluster_by_identity([p])

    assert len(clusters) == 1
    # center should be None when photo has no gps_metadata
    assert clusters[0].get_center() is None
    assert clusters[0].get_photos()[0] is p


def test_cluster_by_distance_basic():
    # two photos with identical coords should be clustered together,
    # the third photo with different coords should form its own cluster (noise allowed)
    p1 = _make_photo(51.0, -0.1, "a.jpg")
    p2 = _make_photo(51.0, -0.1, "b.jpg")
    p3 = _make_photo(52.0, -0.2, "c.jpg")

    clusters = cluster_by_distance([p1, p2, p3], max_distance_meters=1000)

    # Expect two clusters: one with the two identical points, one with the single distant point
    assert len(clusters) == 2

    sizes = sorted([len(c.get_photos()) for c in clusters])
    assert sizes == [1, 2]

    # verify cluster center for the pair is the average of the two identical coordinates
    pair_cluster = next(c for c in clusters if len(c.get_photos()) == 2)
    center = pair_cluster.get_center()
    assert center.get_latitude() == 51.0
    assert center.get_longitude() == -0.1


def test_split_by_date_and_extract_date():
    from red_mantis.models.photo import DistanceCluster
    from red_mantis.models.gps import Decimal

    # photos with the same date but different times should be ordered
    p1 = _make_photo(51.0, -0.1, "a.jpg", date="2020:01:01 10:00:00")
    p2 = _make_photo(51.0, -0.1, "b.jpg", date="2020:01:01 09:00:00")

    center = Decimal(latitude=51.0, longitude=-0.1)
    cluster = DistanceCluster(center=center, photos=[p1, p2])

    # photo with invalid date should fall into 'Unknown'
    p3 = _make_photo(52.0, -0.2, "c.jpg", date="not a date")
    cluster2 = DistanceCluster(center=Decimal(latitude=52.0, longitude=-0.2), photos=[p3])

    result = split_by_date([cluster, cluster2])

    assert "2020-01-01" in result
    # for that date the order should follow time ascending (p2 then p1)
    centers_for_date = result["2020-01-01"]
    assert centers_for_date == [center, center]

    assert "Unknown" in result
    assert result["Unknown"] == [cluster2.get_center()]
