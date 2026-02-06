from pathlib import Path

from red_mantis.core import processor
from red_mantis.models.arguments import MantisPlan
from red_mantis.models.photo import Metadata as PhotoMetadata, DistanceCluster
from red_mantis.models.gps import Decimal


def _mk_photo(name: str, lat=None, lon=None):
    gps = Decimal(latitude=lat, longitude=lon) if lat is not None and lon is not None else None
    return PhotoMetadata(img_path=Path(name), gps_metadata=gps, date_taken=None)


def test_execute_filters_non_gps_and_calls_kml(monkeypatch, tmp_path: Path):
    # Prepare fake file list
    fake_paths = [tmp_path / "a.jpg", tmp_path / "b.jpg", tmp_path / "c.jpg"]

    # Patch extract_all_photo_paths to return our fake paths
    monkeypatch.setattr(processor.extractors, 'extract_all_photo_paths', lambda d: fake_paths)

    # patch extract_photo_information: a.jpg has gps, b.jpg has no gps, c.jpg raises ValueError
    def fake_extract(p):
        name = Path(p).name
        if name == 'a.jpg':
            return _mk_photo('a.jpg', lat=51.0, lon=-0.1)
        if name == 'b.jpg':
            return _mk_photo('b.jpg', lat=None, lon=None)
        raise ValueError("bad image")

    monkeypatch.setattr(processor.extractors, 'extract_photo_information', fake_extract)

    # patch transformer.cluster_by_distance to return a predictable cluster
    cluster = DistanceCluster(center=Decimal(latitude=51.0, longitude=-0.1), photos=[_mk_photo('a.jpg', 51.0, -0.1)])
    monkeypatch.setattr(processor.transformer, 'cluster_by_distance', lambda photos, max_distance_meters: [cluster])

    captured = {}

    def fake_generate(kml_plan):
        captured['kml_plan'] = kml_plan

    monkeypatch.setattr(processor.kml, 'generate', fake_generate)

    # silence logging and startup
    monkeypatch.setattr(processor, 'configure_logging', lambda s: None)
    monkeypatch.setattr(processor, 'print_startup', lambda p: None)

    plan = MantisPlan(
        input_directory=tmp_path,
        output_directory=tmp_path / 'out.kml',
        clustering_threshold=100.0,
        create_travel_lines=False,
        create_travel_points=True,
        silent_mode=True
    )

    processor.execute(plan)

    assert 'kml_plan' in captured
    k = captured['kml_plan']
    # ensure the photos passed to kml are exactly the clusters returned by transformer
    assert k.photos == [cluster]
    assert k.file_path == plan.output_directory


def test_execute_empty_directory_calls_kml_with_empty(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(processor.extractors, 'extract_all_photo_paths', lambda d: [])
    monkeypatch.setattr(processor.extractors, 'extract_photo_information', lambda p: (_ for _ in ()).throw(ValueError()))
    monkeypatch.setattr(processor.transformer, 'cluster_by_distance', lambda photos, max_distance_meters: [])

    captured = {}
    monkeypatch.setattr(processor.kml, 'generate', lambda plan: captured.setdefault('called', True))
    monkeypatch.setattr(processor, 'configure_logging', lambda s: None)
    monkeypatch.setattr(processor, 'print_startup', lambda p: None)

    plan = MantisPlan(
        input_directory=tmp_path,
        output_directory=tmp_path / 'out.kml',
        clustering_threshold=100.0,
        create_travel_lines=False,
        create_travel_points=True,
        silent_mode=False
    )

    processor.execute(plan)

    assert captured.get('called', False) is True
