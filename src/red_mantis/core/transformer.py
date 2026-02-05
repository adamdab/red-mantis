from red_mantis.models.gps import Metadata, Decimal
from red_mantis.models.photo import DistanceCluster
from sklearn.cluster import DBSCAN

def cluster_by_distance(photos: list[Metadata], max_distance_meters: float) -> list[DistanceCluster]:
    """Cluster photos based on GPS coordinates within a specified distance.
    Args:
        photos (list[PhotoMetadata]): List of photo metadata with GPS information.
        max_distance_meters (float): Maximum distance in meters to consider photos as part of the same cluster.
    Returns:
        dict[ tuple, list[PhotoMetadata]]: A dictionary where keys are cluster GPS coordinates and values are lists of PhotoMetadata objects in that cluster.
    """
    METERS_PER_DEGREE = 111320  # 1 degree is approximately 111.32 km
    db = DBSCAN(eps=max_distance_meters / METERS_PER_DEGREE, min_samples=1, metric='haversine').fit([
        (photo.gps_metadata.get_latitude(), photo.gps_metadata.get_longitude())
        for photo in photos])
    clusters = []
    for label in set(db.labels_):
        cluster_photos = [photos[idx] for idx, cluster_label in enumerate(db.labels_) if cluster_label == label]
        if cluster_photos:
            cluster_center = Decimal(
                latitude=sum(photo.gps_metadata.get_latitude() for photo in cluster_photos) / len(cluster_photos),
                longitude=sum(photo.gps_metadata.get_longitude() for photo in cluster_photos) / len(cluster_photos)
            )
            clusters.append(DistanceCluster(center=cluster_center, photos=cluster_photos))
    return clusters

def cluster_by_identity(photos: list[Metadata]) -> list[DistanceCluster]:
    """
    Cluster photos by identity GPS coordinates (each photo forms its own cluster).
    Args:
        photos (list[PhotoMetadata]): List of photo metadata with GPS information.
    Returns:
        list[PhotoCluster]: A list of PhotoCluster objects, each containing a single photo.
    """
    return [ DistanceCluster(center=photo.gps_metadata, photos=[photo]) for photo in photos ]