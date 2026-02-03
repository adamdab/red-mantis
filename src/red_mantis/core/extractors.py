from pathlib import Path
from PIL import Image, ExifTags
from red_mantis.models.metadata import DMSGPSMetadata, GPSMetadata, PhotoMetadata
from red_mantis.models.constants import ImageFormats

def extract_all_photo_paths(directory: Path) -> list[Path]:
    """Extract all photo paths from the given directory."""
    photo_paths = []
    for suffix_list in ImageFormats:
        for suffix in suffix_list.value:
            photo_paths.extend(directory.glob(f'*{suffix}'))
    return photo_paths

def _extract_jpg_metadata(image_path: Path) -> dict:
    """Extract metadata from JPG/JPEG image files."""
    with Image.open(image_path) as image:
        exif_data = image._getexif()
        if not exif_data:
            return {}
        return { ExifTags.TAGS.get(tag): value
                for tag, value in exif_data.items() if tag in ExifTags.TAGS }
    raise FileNotFoundError(f"Image file could not be opened: {image_path}")


def extract_photo_information(photo_path: Path) -> PhotoMetadata:
    """For each supported extension extract all metadata"""
    suffix = photo_path.suffix.lower()
    if suffix in ImageFormats.JPG.value:
        full_metadata = _extract_jpg_metadata(photo_path)
        gps_metadata = _extract_jpg_gps_info(full_metadata)
        return PhotoMetadata(
            img_path=str(photo_path),
            gps_metadata=gps_metadata,
            date_taken=full_metadata.get('DateTimeOriginal')
        )
    raise ValueError(f"Unsupported image format: {photo_path.suffix}")

def _extract_jpg_gps_info(metadata: dict) -> GPSMetadata:
    """Extract GPS information from JPG/JPEG metadata."""
    if 'GPSInfo' not in metadata:
        raise KeyError("No GPSInfo found in metadata.")
    gps_info = metadata.get('GPSInfo', {})
    if not gps_info:
        return None
    gps_data = { ExifTags.GPSTAGS.get(tag): value
                 for tag, value in gps_info.items() if tag in ExifTags.GPSTAGS }
    return DMSGPSMetadata(
        dms_latitude=gps_data['GPSLatitude'],
        lat_ref=gps_data['GPSLatitudeRef'],
        dms_longitude=gps_data['GPSLongitude'],
        lon_ref=gps_data['GPSLongitudeRef']
    )