# Red Mantis

Tool to plot your travel photos onto a world map, clustering by GPS location and generating KML files for visualization in Google Earth or Maps.

## Features

- Extract GPS metadata images
- Cluster points by distance
- Create travle paths
- Generate KML files

## Installation

Clone the repository and install with `uv`:

```bash
git clone <repo-url>
cd red-mantis
uv sync
```

Or using `pip`:

```bash
pip install -e .
```

## Usage

### Command Line

Run the tool with:

```bash
uv run red-mantis <photo_directory> [options]
```

**Options:**

- `--cluster-dist`: Distance in meters for clustering photos (default: 50.0), if set to 0 or negative clustering is disabled
- `--skip-travel-lines`: Skip creating daily travel lines
- `--skip-travel-points`: Skip putting points where photos were taken
- `--output`: Output KML file path (default: travel.kml)
- `--silent`: Disable logging output

**Example:**

```bash
uv run red-mantis ~/Pictures/vacation --cluster-dist 100 --output my_trip.kml
```

## Project Structure

```
src/red_mantis/
├── cli/
│   └── main.py                 # Command-line interface
├── core/
│   ├── extractors.py           # Photo metadata extraction
│   ├── transformer.py          # Clustering and date splitting
│   ├── processor.py            # Main execution pipeline
│   └── kml.py                  # KML file generation
├── models/
│   ├── gps.py                  # GPS coordinate models
│   ├── photo.py                # Photo metadata model
│   ├── arguments.py            # Command arguments
│   └── constants.py            # Constants
└── utils/
    └── logging_setup.py        # Logging configuration
```

## Testing

Run the test suite with pytest:

```bash
uv pip install pytest coverage
uv run pytest -q
```

For coverage report:

```bash
uv run coverage run -m pytest -q
uv run coverage report
```

## Supported Formats

- JPG / JPEG images with EXIF metadata

## Requirements

- Python 3.13+
- pillow
- pydantic
- scikit-learn
- simplekml