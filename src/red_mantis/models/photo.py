from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from red_mantis.models.gps import Metadata


@dataclass(frozen=True)
class Metadata:
    img_path: Path
    gps_metadata: Optional[Metadata] = None
    date_taken: Optional[str] = None


@dataclass(frozen=True)
class Cluster:
    center: Metadata
    photos: List[Metadata]
