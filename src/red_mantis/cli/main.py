import argparse
from pathlib import Path

from red_mantis.models.arguments import MantisPlan
from red_mantis.core.processor import execute
from red_mantis.utils.logging_setup import configure_logging, print_startup

def main():
    parser = argparse.ArgumentParser(
        prog="red-mantis",
        description="Your travel tracker from photos")
    
    parser.add_argument('photo_dir',
                        type=str,
                        help='Directory containing photos to process')
    parser.add_argument('--cluster-dist',
                        type=float,
                        default=50.0,
                        help='Distance in meters for clustering photos, to disable clustering set to 0')
    parser.add_argument('--skip-travel-lines',
                        action='store_true',
                        help='Skip travel lines in the KML output')
    parser.add_argument('--skip-travel-points',
                        action='store_true',
                        help='Skip creating travel points in the KML output')
    parser.add_argument('--output',
                        type=str,
                        default='travel.kml',
                        help='Output report file')
    parser.add_argument('--silent',
                        action='store_true',
                        help='Disable logging output')

    args = parser.parse_args()

    plan = MantisPlan(
        input_directory=Path(args.photo_dir),
        output_directory=Path(args.output),
        clustering_threshold=args.cluster_dist,
        create_travel_lines=not args.skip_travel_lines,
        create_travel_points=not args.skip_travel_points,
        silent_mode=args.silent
    )

    execute(plan)    