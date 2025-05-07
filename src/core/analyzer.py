import pandas as pd
from geopy.distance import geodesic


class RouteAnalyzer:
    @staticmethod
    def calculate_basic_stats(df):
        """Podstawowe statystyki"""
        return df.groupby('placemark').agg({
            'latitude': ['min', 'max', 'mean'],
            'longitude': ['min', 'max', 'mean'],
            'altitude': ['min', 'max', 'mean', 'std']
        })

    @staticmethod
    def calculate_distance(df):
        """Obliczanie długości trasy"""

        def _calculate(group):
            points = list(zip(group['latitude'], group['longitude']))
            return sum(geodesic(p1, p2).meters
                       for p1, p2 in zip(points[:-1], points[1:]))

        return df.groupby('placemark').apply(_calculate)