from dataclasses import dataclass
from typing import Protocol

class GPSMetadata(Protocol):
    def get_latitude(self) -> float:
        ...
    def get_longitude(self) -> float:
        ...

@dataclass(frozen=True)
class DMSGPSMetadata:
    dms_latitude: tuple
    lat_ref: str
    dms_longitude: tuple
    lon_ref: str

    def _convert_dms_to_decimal(self, dms: tuple, ref: str) -> float:
        degrees = dms[0]
        minutes = dms[1] / 60.0
        seconds = dms[2] / 3600.0
        decimal = degrees + minutes + seconds
        if ref in ['S', 'W']:
            decimal = -decimal
        return decimal
    
    def get_latitude(self) -> float:
        return self._convert_dms_to_decimal(self.dms_latitude, self.lat_ref)
    
    def get_longitude(self) -> float:
        return self._convert_dms_to_decimal(self.dms_longitude, self.lon_ref)
    
@dataclass(frozen=True)
class DecimalGPSMetadata:
    latitude: float
    longitude: float

    def get_latitude(self) -> float:
        return self.latitude
    
    def get_longitude(self) -> float:
        return self.longitude
    
@dataclass(frozen=True)
class PhotoMetadata:
    img_path: str
    gps_metadata: GPSMetadata | None
    date_taken: str | None = None

@dataclass(frozen=True)
class PhotoCluster:
    center: GPSMetadata
    photos: list[PhotoMetadata]