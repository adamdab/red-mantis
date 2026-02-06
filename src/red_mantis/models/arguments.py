from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class MantisPlan:
    """Represents a plan for running the Red Mantis application."""
    input_directory: Path
    output_directory: Path
    clustering_threshold: float
    create_travel_lines: bool
    create_travel_points: bool
    silent_mode: bool

@dataclass(frozen=True)
class KMLGenerationPlan:
    """Represents a plan for generating a KML file."""
    file_path: Path
    photos: list
    create_travel_lines: bool
    create_travel_points: bool