from pathlib import Path 
from PIL import Image, ExifTags

def get_jpg_files(directory:str) -> list[Path]:
    """Return a list of .jpg or .jpeg files in the given directory."""
    jpg = [f for f in Path(directory).glob('*.jpg')]
    jpeg = [f for f in Path(directory).glob('*.jpeg')]
    return jpg + jpeg 

def extract_metadata(image_path:Path) -> dict:
    """Extract metadata from the image file."""
    with Image.open(image_path) as image:
        exif_data = image._getexif()
        if not exif_data:
            return {}
        return { ExifTags.TAGS.get(tag): value
                for tag, value in exif_data.items() if tag in ExifTags.TAGS }
    raise FileNotFoundError(f"Image file could not be opened: {image_path}")

def get_gps_info(metadata:dict) -> dict:
    """Extract GPS information from metadata."""
    if 'GPSInfo' not in metadata:
        raise KeyError("No GPSInfo found in metadata.")
    gps_info = metadata.get('GPSInfo', {})
    if not gps_info:
        return {}
    return { ExifTags.GPSTAGS.get(tag): value
            for tag, value in gps_info.items() if tag in ExifTags.GPSTAGS }

def get_decimal_from_dms(dms, ref):
    """Convert DMS (degrees, minutes, seconds) to decimal degrees"""
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0
    decimal = degrees + minutes + seconds
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def get_coordinates(gps_info:dict) -> tuple[float, float]:
    """Get latitude and longitude from GPS information."""
    lat = get_decimal_from_dms(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
    lon = get_decimal_from_dms(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])
    return (lat, lon)