import argparse
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

    args = parser.parse_args()
    print("Running red-mantis with the following parameters:")
    print(f"Photo Directory: {args.photo_dir}")
    print(f"Output Report File: {args.output}")

    image_paths = extractors.extract_all_photo_paths(Path(args.photo_dir))

    print(f"...Found {len(image_paths)} JPG files in the directory.")

    tracable_photos = []
    for photo_path in image_paths:
        with suppress((ValueError, KeyError, FileNotFoundError)):
            photo_metadata = extractors.extract_photo_information(photo_path)
            if photo_metadata.gps_metadata:
                tracable_photos.append(photo_metadata)

    print(f"...Of which {len(tracable_photos)} contain GPS information.")    

    clustered_photos = transformer.cluster_by_distance(tracable_photos, max_distance_meters=args.cluster_dist)
    print(f"...Clustered into {len(clustered_photos)} groups based on distance.")
    
    kml.generate(Path(args.output), clustered_photos)

    print("red-mantis has finished successfully.")
    print("...Done.")

if __name__ == "__main__":
    main()
