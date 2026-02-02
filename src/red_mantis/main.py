import argparse
from contextlib import suppress
import red_mantis.image_progessor as img_proc
import red_mantis.file_generator as file_gen

def main():
    parser = argparse.ArgumentParser(
        prog="red-mantis",
        description="Your travel tracker from photos")
    
    parser.add_argument('photo_dir',
                        type=str,
                        help='Directory containing photos to process')
    parser.add_argument('--output',
                        type=str,
                        default='travel.kml',
                        help='Output report file')

    args = parser.parse_args()
    print("Running red-mantis with the following parameters:")
    print(f"Photo Directory: {args.photo_dir}")
    print(f"Output Report File: {args.output}")

    paths_jpg = img_proc.get_jpg_files(args.photo_dir)

    print(f"...Found {len(paths_jpg)} JPG files in the directory.")

    tracable_photos = []
    for photo_path in paths_jpg:
        with suppress(KeyError):
            metadata = img_proc.extract_metadata(photo_path)
            gps_info = img_proc.get_gps_info(metadata)
            tracable_photos.append(
                {"ImgPath": photo_path,
                 "GPSMetadata":gps_info,
                 "GPSCoordinates": img_proc.get_coordinates(gps_info)})

    print(f"...Of which {len(tracable_photos)} contain GPS information.")

    file_gen.generate_kml(args.output, tracable_photos)

    print("red-mantis has finished successfully.")
    print("...Done.")

if __name__ == "__main__":
    main()
