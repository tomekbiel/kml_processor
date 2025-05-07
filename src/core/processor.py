# src/core/processor.py
import pandas as pd
import glob
import os
from geopy.distance import geodesic
from .converter import kml_to_df, gpx_to_df
from .analyzer import RouteAnalyzer

class RouteProcessor:
    def __init__(self, input_dir='data/input', output_dir='data/output'):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def merge_files(self, file_type='kml'):
        """Łączenie plików określonego typu"""
        all_files = glob.glob(os.path.join(self.input_dir, f'*.{file_type}'))
        dfs = [kml_to_df(f) if file_type == 'kml' else gpx_to_df(f)
              for f in all_files]
        return pd.concat(dfs, ignore_index=True)

    def clean_data(self, df, tolerance=0.0001):
        """Czyszczenie danych"""
        df = df.sort_values(['latitude', 'longitude'])
        df['lat_rounded'] = (df['latitude'] / tolerance).round() * tolerance
        df['lon_rounded'] = (df['longitude'] / tolerance).round() * tolerance
        return df.drop_duplicates(subset=['lat_rounded', 'lon_rounded']).drop(
            columns=['lat_rounded', 'lon_rounded'])

    def calculate_metrics(self, df):
        """Obliczanie metryk trasy"""
        return RouteAnalyzer.calculate_basic_stats(df)

    def save_output(self, df, filename):
        """Zapis wyników"""
        output_path = os.path.join(self.output_dir, filename)
        df.to_csv(output_path, index=False)
        print(f"Zapisano plik: {output_path}")