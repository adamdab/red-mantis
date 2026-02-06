import simplekml
import logging
from red_mantis.models.arguments import KMLGenerationPlan
from red_mantis.models.photo import Cluster
from red_mantis.core.transformer import split_by_date

def generate(plan: KMLGenerationPlan) -> None:
    """Generate a KML file from the list of photos with GPS coordinates."""

    kml = simplekml.Kml()
    
    logging.info(f"Generating KML file at: {plan.file_path}")
    
    if plan.create_travel_points:
        _generate_cluster_points(kml, plan.photos)
    if plan.create_travel_lines:
        _generate_travel_lines(kml, plan.photos)

    kml.save(str(plan.file_path))

def _generate_cluster_points(kml:simplekml.Kml, photos: list[Cluster]):
    for cluster in photos:
        pnt = kml.newpoint(name=f"[{len(cluster.get_photos())} Photos]",
                           coords=[(cluster.get_center().get_longitude(),
                                    cluster.get_center().get_latitude())])
        pnt.description = cluster.get_description()
    logging.info(f"Added {len(photos)} cluster points to KML")

def _get_color(inx:int) -> str:
    red = "FF0000FF"  # Red color in KML format (AABBGGRR)
    green = "FF00FF00"  # Green color in KML format (AABBGGRR)
    blue = "FFFF0000"  # Blue color in KML format (AABBGGRR)
    colors = [red, green, blue]
    return colors[inx % len(colors)]

def _generate_travel_lines(kml:simplekml.Kml, photos: list[Cluster]):
    idx = 0
    sorted_clusters = split_by_date(photos)
    for date, clusters in sorted_clusters.items():
        ls = kml.newlinestring(name=f"Travel Path - {date}")
        ls.coords = [(metadata.get_longitude(), metadata.get_latitude())
                     for metadata in clusters]
        ls.style.linestyle.width = 3
        ls.style.linestyle.color = _get_color(idx)
        ls.tesalite = 1
        ls.altitudemode = simplekml.AltitudeMode.clamptoground
        idx += 1
    logging.info(f"Added {len(sorted_clusters)} travel lines to KML")