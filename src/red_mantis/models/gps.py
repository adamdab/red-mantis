from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class Metadata(Protocol):
    """Protocol describing GPS coordinate accessors used across the project."""

    def get_latitude(self) -> float:  # pragma: no cover - simple accessor
        ...

    def get_longitude(self) -> float:  # pragma: no cover - simple accessor
        ...


@dataclass(frozen=True)
class DMS:
    dms_latitude: tuple
    lat_ref: str
    dms_longitude: tuple
    lon_ref: str

    def _convert_dms_to_decimal(self, dms: tuple, ref: str) -> float:
        degrees = dms[0]
        minutes = dms[1] / 60.0
        seconds = dms[2] / 3600.0
        decimal = degrees + minutes + seconds
        if ref in ("S", "W"):
            decimal = -decimal
        return decimal

    def get_latitude(self) -> float:
        return self._convert_dms_to_decimal(self.dms_latitude, self.lat_ref)

    def get_longitude(self) -> float:
        return self._convert_dms_to_decimal(self.dms_longitude, self.lon_ref)


@dataclass(frozen=True)
class Decimal:
    latitude: float
    longitude: float

    def get_latitude(self) -> float:
        return self.latitude

    def get_longitude(self) -> float:
        return self.longitude
