import simplekml

def generate_kml(file_path: str, photos: list[dict]) -> None:
    """Generate a KML file from the list of photos with GPS coordinates."""
    kml = simplekml.Kml()
    
    print(f"Generating KML file at: {file_path}")

    for photo in photos:
        coords = photo["GPSCoordinates"]
        if coords:
            pnt = kml.newpoint(name=photo["ImgPath"].name,
                               coords=[(coords['Longitude'], coords['Latitude'])])
            pnt.description = f"Photo taken at {coords['Latitude']}, {coords['Longitude']}"
    
    kml.save(file_path)