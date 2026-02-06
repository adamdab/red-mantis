import logging
from pathlib import Path
from contextlib import suppress

from red_mantis.models.run import Plan
from red_mantis.core import extractors
from red_mantis.core import kml, transformer
from red_mantis.utils.logging_setup import configure_logging, print_startup

def execute(plan: Plan):

    configure_logging(plan.silent_mode)
    
    print_startup(plan)
    
    image_paths = extractors.extract_all_photo_paths(Path(plan.input_directory))

    logging.info(f"Found {len(image_paths)} JPG files in the directory")

    tracable_photos = []
    for photo_path in image_paths:
        with suppress((ValueError, KeyError, FileNotFoundError)):
            photo_metadata = extractors.extract_photo_information(photo_path)
            if photo_metadata.gps_metadata:
                tracable_photos.append(photo_metadata)

    logging.info(f"{len(tracable_photos)}/{len(image_paths)} contain GPS information")

    clustered_photos = transformer.cluster_by_distance(tracable_photos,
                                                       max_distance_meters=plan.clustering_threshold)
    
    logging.info(f"Clustered into {len(clustered_photos)} groups")
    
    kml.generate(Path(plan.output_directory), clustered_photos)

    logging.info("Red Mantis run completed successfully")
