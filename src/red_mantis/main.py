import argparse
import logging
from pathlib import Path
from contextlib import suppress

from red_mantis.core import extractors
from red_mantis.core import kml, transformer
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
    configure_logging(args.silent)
    
    print_startup(args)
    
    image_paths = extractors.extract_all_photo_paths(Path(args.photo_dir))

    logging.info(f"Found {len(image_paths)} JPG files in the directory")


    tracable_photos = []
    for photo_path in image_paths:
        with suppress((ValueError, KeyError, FileNotFoundError)):
            photo_metadata = extractors.extract_photo_information(photo_path)
            if photo_metadata.gps_metadata:
                tracable_photos.append(photo_metadata)

    logging.info(f"{len(tracable_photos)}/{len(image_paths)} contain GPS information")    

    clustered_photos = transformer.cluster_by_distance(tracable_photos, max_distance_meters=args.cluster_dist)
    
    logging.info(f"Clustered into {len(clustered_photos)} groups")
    
    kml.generate(Path(args.output), clustered_photos)

    logging.info("Red Mantis run completed successfully")

if __name__ == "__main__":
    main()
