import logging
from pathlib import Path
from contextlib import suppress

from red_mantis.models.arguments import MantisPlan, KMLGenerationPlan
from red_mantis.core import extractors
from red_mantis.core import kml, transformer
from red_mantis.utils.logging_setup import configure_logging, print_startup

def execute(plan: MantisPlan):

    configure_logging(plan.silent_mode)
    
    print_startup(plan)
    
    image_paths = extractors.extract_all_photo_paths(plan.input_directory)

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
    
    kml_plan = KMLGenerationPlan(
        file_path=plan.output_directory,
        photos=clustered_photos,
        create_travel_lines=plan.create_travel_lines
    )

    kml.generate(kml_plan)

    logging.info("Red Mantis run completed successfully")
