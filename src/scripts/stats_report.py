# src/scripts/stats_report.py
import pandas as pd
from src.core.analyzer import RouteAnalyzer
from src.core.processor import RouteProcessor


def generate_report():
    processor = RouteProcessor()
    analyzer = RouteAnalyzer()

    df = processor.merge_files()
    stats = analyzer.calculate_basic_stats(df)

    # Formatowanie raportu
    report = f"""
    Raport statystyk tras
    --------------------
    Liczba tras: {len(stats)}
    Średnia długość trasy: {stats['distance_meters'].mean():.2f} m
    Maksymalna wysokość: {stats['altitude']['max'].max()} m n.p.m.
    """

    with open('../../data/output/stats_report.txt', 'w') as f:
        f.write(report)

    return stats


if __name__ == "__main__":
    generate_report()