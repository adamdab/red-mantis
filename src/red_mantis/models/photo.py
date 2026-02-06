from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Protocol

from red_mantis.models.gps import Metadata


@dataclass(frozen=True)
class Metadata:
    img_path: Path
    gps_metadata: Optional[Metadata] = None
    date_taken: Optional[str] = None

class Cluster(Protocol):
    def get_center(self) -> Metadata:
        ...
    def get_photos(self) -> List[Metadata]:
        ...
    def get_description(self) -> str:
        ...

@dataclass(frozen=True)
class DistanceCluster:
    center: Metadata
    photos: List[Metadata]
    def get_center(self) -> Metadata:
        return self.center
    def get_photos(self) -> List[Metadata]:
        return self.photos
    def get_description(self) -> str:
        description = ""
        for photo in self.photos:
            description += f"Photo: {Path(photo.img_path).name}\n"
            if photo.gps_metadata:
                description += f"Latitude: {photo.gps_metadata.get_latitude()}\n"
                description += f"Longitude: {photo.gps_metadata.get_longitude()}\n"
            if photo.date_taken:
                description += f"Date Taken: {photo.date_taken}\n"
            description += "\n"
        return description.strip()