from sklearn.cluster import DBSCAN
from datetime import datetime
from red_mantis.models.gps import Metadata, Decimal
from red_mantis.models.photo import DistanceCluster, Cluster

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

def _extract_date(photo: Metadata) -> str:
    """Extract date from photo metadata.
    Args:
        photo (Metadata): Photo metadata containing date information.
    Returns:
        str: Extracted date in 'YYYY-MM-DD' format or 'Unknown' if not available.
    """
    if photo.date_taken:
        try:
            date_obj = datetime.strptime(photo.date_taken, "%Y:%m:%d %H:%M:%S")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return "Unknown"
    return "Unknown"

def split_by_date(clusters: list[Cluster]) -> dict[str, Metadata]:
    """ Split clusters to date photos pairs.
    Args:
        clusters (list[Cluster]): List of photo clusters.
    Returns:
        dict[str, Metadata]: Dictionary mapping date strings to cluster centers.
    """
    date_clusters = {}
    for cluster in clusters:
        for photo in cluster.get_photos():
            date = _extract_date(photo)
            if date not in date_clusters:
                date_clusters[date] = []
            date_clusters[date].append({
                "center": cluster.get_center(),
                "time": photo.date_taken})
            
    sorted_date_clusters = {}
    for date, clusters in date_clusters.items():
        sorted_clusters = sorted(clusters, key=lambda x: x["time"] or "")
        sorted_date_clusters[date] = sorted_clusters

    return {date: [cluster["center"] for cluster in clusters]
            for date, clusters in sorted_date_clusters.items()}        
