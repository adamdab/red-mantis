from dataclasses import dataclass

@dataclass(frozen=True)
class Plan:
    """Represents a plan for running the Red Mantis application."""
    input_directory: str
    output_directory: str
    clustering_threshold: float
    silent_mode: bool
