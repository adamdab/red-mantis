import pytest
from PIL import ExifTags
from pathlib import Path

from red_mantis.core import extractors


def test_extract_all_photo_paths(tmp_path: Path):
    (tmp_path / "a.jpg").write_text("x")
    (tmp_path / "b.jpeg").write_text("x")
    (tmp_path / "c.png").write_text("x")

    paths = extractors.extract_all_photo_paths(tmp_path)
    found = {p.name for p in paths}
    assert "a.jpg" in found
    assert "b.jpeg" in found
    assert "c.png" not in found


def _make_dummy_image(exif_dict):
    class DummyImage:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            return False
        def _getexif(self):
            return exif_dict
    return DummyImage()


def test__extract_jpg_metadata_and_extract_photo_information(monkeypatch, tmp_path: Path):
    # build EXIF numeric keys for tags we need
    date_tag = next(k for k, v in ExifTags.TAGS.items() if v == 'DateTimeOriginal')
    gps_tag = next(k for k, v in ExifTags.TAGS.items() if v == 'GPSInfo')

    # build gps subtags numeric keys
    gps_lat_tag = next(k for k, v in ExifTags.GPSTAGS.items() if v == 'GPSLatitude')
    gps_lat_ref_tag = next(k for k, v in ExifTags.GPSTAGS.items() if v == 'GPSLatitudeRef')
    gps_lon_tag = next(k for k, v in ExifTags.GPSTAGS.items() if v == 'GPSLongitude')
    gps_lon_ref_tag = next(k for k, v in ExifTags.GPSTAGS.items() if v == 'GPSLongitudeRef')

    # create EXIF data with GPSInfo sub-dictionary
    gps_info = {
        gps_lat_tag: (51, 0, 0),
        gps_lat_ref_tag: 'N',
        gps_lon_tag: (1, 0, 0),
        gps_lon_ref_tag: 'E'
    }

    exif = {
        date_tag: '2020:01:01 10:00:00',
        gps_tag: gps_info
    }

    monkeypatch.setattr(extractors.Image, 'open', lambda path: _make_dummy_image(exif))

    # create dummy file path
    p = tmp_path / "img.jpg"
    p.write_text("x")

    photo = extractors.extract_photo_information(p)

    assert photo.date_taken == '2020:01:01 10:00:00'
    assert photo.gps_metadata is not None
    assert pytest.approx(photo.gps_metadata.get_latitude()) == 51.0
    assert pytest.approx(photo.gps_metadata.get_longitude()) == 1.0


def test__extract_jpg_gps_info_errors_and_empty():
    # missing GPSInfo should raise KeyError
    with pytest.raises(KeyError):
        extractors._extract_jpg_gps_info({})

    # empty GPSInfo dict should return None
    assert extractors._extract_jpg_gps_info({'GPSInfo': {}}) is None