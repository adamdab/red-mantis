import simplekml
import logging
from pathlib import Path
from red_mantis.models.photo import Cluster


def generate(file_path: Path, photos: list[Cluster]) -> None:
    """Generate a KML file from the list of photos with GPS coordinates."""

    kml = simplekml.Kml()
    
    logging.info(f"Generating KML file at: {file_path}")

    for cluster in photos:
        pnt = kml.newpoint(name=f"[{len(cluster.photos)} Photos]",
                           coords=[(cluster.center.get_longitude(),
                                    cluster.center.get_latitude())])
        description = "";
        for photo in cluster.photos:
            description += f"Photo: {Path(photo.img_path).name}\n" \
                           f"Latitude: {photo.gps_metadata.get_latitude()}\n" \
                           f"Longitude: {photo.gps_metadata.get_longitude()}\n\n"
        pnt.description = description.strip()

    kml.save(str(file_path))
