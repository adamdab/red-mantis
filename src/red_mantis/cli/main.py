import argparse

from red_mantis.models.run import Plan
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
                        help='Distance in meters for clustering photos')
    parser.add_argument('--output',
                        type=str,
                        default='travel.kml',
                        help='Output report file')
    parser.add_argument('--silent',
                        action='store_true',
                        help='Disable logging output')

    args = parser.parse_args()

    plan = Plan(
        input_directory=args.photo_dir,
        output_directory=args.output,
        clustering_threshold=args.cluster_dist,
        silent_mode=args.silent
    )

    execute(plan)    