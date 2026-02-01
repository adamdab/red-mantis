from pathlib import Path 
from PIL import Image, ExifTags

def get_jpg_files(directory:str) -> list[Path]:
    """Return a list of .jpg files in the given directory."""
    return [f for f in Path(directory).glob('*.jpg')]

def extract_metadata(image_path:Path) -> dict:
    """Extract metadata from the image file."""
    with Image.open(image_path) as image:
        exif_data = image._getexif()
        if not exif_data:
            return {}
        return { ExifTags.TAGS.get(tag): value for tag, value in exif_data.items() if tag in ExifTags.TAGS }
    raise FileNotFoundError(f"Image file could not be opened: {image_path}")

def get_gps_info(metadata:dict) -> dict:
    """Extract GPS information from metadata."""
    if 'GPSInfo' not in metadata:
        raise KeyError("No GPSInfo found in metadata.")
    gps_info = metadata.get('GPSInfo', {})
    if not gps_info:
        return {}
    return { ExifTags.GPSTAGS.get(tag): value for tag, value in gps_info.items() if tag in ExifTags.GPSTAGS }