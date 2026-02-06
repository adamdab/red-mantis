from red_mantis.models.gps import Metadata, Decimal
from red_mantis.models.photo import DistanceCluster, Cluster
from sklearn.cluster import DBSCAN

def cluster_by_distance(photos: list[Metadata],
                        max_distance_meters: float) -> list[Cluster]:
    """Cluster photos based on GPS coordinates within a specified distance.
    Args:
        photos (list[Metadata])
            List of photo metadata with GPS information.
        max_distance_meters (float)
            Maximum distance in meters to consider photos as part of the same cluster.
    Returns:
        list[Cluster]
            A list of Photo Clusters.
    """
    METERS_PER_DEGREE = 111320  # 1 degree is approximately 111.32 km
    db = DBSCAN(eps=max_distance_meters / METERS_PER_DEGREE,
                min_samples=2,
                metric='haversine')
    db.fit([
        (photo.gps_metadata.get_latitude(), photo.gps_metadata.get_longitude())
        for photo in photos])
    clusters = []
    for label in set(db.labels_):
        cluster_photos = [photos[idx]
                          for idx, cluster_label in enumerate(db.labels_)
                          if cluster_label == label]
        if cluster_photos:
            
            center_lat = sum(photo.gps_metadata.get_latitude()
                             for photo in cluster_photos)
            center_lat = center_lat / len(cluster_photos)

            center_lon = sum(photo.gps_metadata.get_longitude()
                             for photo in cluster_photos)
            center_lon = center_lon / len(cluster_photos)

            cluster_center = Decimal(
                latitude =  center_lat,
                longitude = center_lon,
            )
            clusters.append(
                DistanceCluster(
                    center=cluster_center,
                    photos=cluster_photos))
    return clusters

def cluster_by_identity(photos: list[Metadata]) -> list[Cluster]:
    """
    Cluster photos by identity GPS coordinates (each photo forms its own cluster).
    Args:
        photos (list[Metadata]): List of photo metadata with GPS information.
    Returns:
        list[Cluster]:
            A list of Photo Clusters.
    """
    return [ DistanceCluster(center=photo.gps_metadata,
                             photos=[photo]) for photo in photos ]