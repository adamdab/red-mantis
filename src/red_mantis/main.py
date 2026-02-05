import argparse
import logging
from pathlib import Path
from contextlib import suppress

from red_mantis.core import extractors
from red_mantis.core import kml, transformer

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
    parser.add_argument('--verbose',
                        action='store_true',
                        help='Enable verbose output')

    args = parser.parse_args()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO if args.verbose else logging.WARNING)

    # Colored log formatter (ANSI colors)
    class ColoredFormatter(logging.Formatter):
        COLOR_RESET = '\x1b[0m'
        COLORS = {
            logging.DEBUG: '\x1b[90m',
            logging.INFO: '\x1b[32m',
            logging.WARNING: '\x1b[33m',
            logging.ERROR: '\x1b[31m',
            logging.CRITICAL: '\x1b[31;1m',
        }

        def format(self, record):
            level_color = self.COLORS.get(record.levelno, '')
            # colorize the level name only
            record.levelname = f"{level_color}{record.levelname}{self.COLOR_RESET}"
            return super().format(record)

    fmt = '%(asctime)s | %(levelname)s | %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter(fmt=fmt, datefmt=datefmt))
    logger.handlers = []
    logger.addHandler(handler)
    logger.debug("Logging initialized. verbose=%s", args.verbose)

    logging.info("Running red-mantis with the following parameters:")
    logging.info(f"Photo Directory: {args.photo_dir}")
    logging.info(f"Output Report File: {args.output}")

    image_paths = extractors.extract_all_photo_paths(Path(args.photo_dir))

    logging.info(f"...Found {len(image_paths)} JPG files in the directory.")

    tracable_photos = []
    for photo_path in image_paths:
        with suppress((ValueError, KeyError, FileNotFoundError)):
            photo_metadata = extractors.extract_photo_information(photo_path)
            if photo_metadata.gps_metadata:
                tracable_photos.append(photo_metadata)

    logging.info(f"...Of which {len(tracable_photos)} contain GPS information.")    

    clustered_photos = transformer.cluster_by_distance(tracable_photos, max_distance_meters=args.cluster_dist)
    logging.info(f"...Clustered into {len(clustered_photos)} groups based on distance.")
    
    kml.generate(Path(args.output), clustered_photos)

    logging.info("red-mantis has finished successfully.")
    logging.info("...Done.")

if __name__ == "__main__":
    main()
