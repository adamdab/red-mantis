import simplekml
import logging
from pathlib import Path
from red_mantis.models.photo import Cluster


def generate(file_path: Path, photos: list[Cluster]) -> None:
    """Generate a KML file from the list of photos with GPS coordinates."""

    kml = simplekml.Kml()
    
    logging.info(f"Generating KML file at: {file_path}")

    for cluster in photos:
        pnt = kml.newpoint(name=f"[{len(cluster.get_photos())} Photos]",
                           coords=[(cluster.get_center().get_longitude(),
                                    cluster.get_center().get_latitude())])
        pnt.description = cluster.get_description()

    kml.save(str(file_path))
