import simplekml
from pathlib import Path
from red_mantis.models.metadata import PhotoMetadata


def generate(file_path: Path, photos: list[PhotoMetadata]) -> None:
    """Generate a KML file from the list of photos with GPS coordinates."""

    kml = simplekml.Kml()
    
    print(f"Generating KML file at: {file_path}")

    for photo in photos:
        pnt = kml.newpoint(name=Path(photo.img_path).name,
                           coords=[(photo.gps_metadata.get_longitude(),
                                    photo.gps_metadata.get_latitude())])
        pnt.description = f"Photo: {Path(photo.img_path).name}\n" \
                          f"Latitude: {photo.gps_metadata.get_latitude()}\n" \
                          f"Longitude: {photo.gps_metadata.get_longitude()}"
        
    kml.save(str(file_path))
