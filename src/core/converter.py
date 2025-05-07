from simplekml import Kml
from pykml import parser
import gpxpy
import pandas as pd
import os


def df_to_kml(df, output_path):
    """Zapis DataFrame do pliku KML"""
    kml = Kml()
    for name, group in df.groupby('placemark'):
        linestring = kml.newlinestring(name=name)
        linestring.coords = [(row['longitude'], row['latitude'], row['altitude'])
                             for _, row in group.iterrows()]
    kml.save(output_path)


def kml_to_df(kml_file):
    """Konwersja KML do DataFrame"""
    with open(kml_file) as f:
        doc = parser.parse(f).getroot()

    coordinates = []
    for pm in doc.Document.Placemark:
        if hasattr(pm, 'LineString'):
            coords = str(pm.LineString.coordinates).split()
            for coord in coords:
                lon, lat, alt = map(float, coord.split(','))
                coordinates.append({
                    'placemark': str(pm.name),
                    'longitude': lon,
                    'latitude': lat,
                    'altitude': alt,
                    'source_file': os.path.basename(kml_file)
                })
    return pd.DataFrame(coordinates)


def gpx_to_df(gpx_file):
    """Konwersja GPX do DataFrame"""
    with open(gpx_file) as f:
        gpx = gpxpy.parse(f)

    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation,
                    'time': point.time
                })
    return pd.DataFrame(points)