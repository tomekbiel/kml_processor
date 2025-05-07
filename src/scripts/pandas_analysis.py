# src/scripts/pandas_analysis.py
import os
import pandas as pd
from geopy.distance import geodesic
from src.core.processor import RouteProcessor


def advanced_analysis():
    # Pobieranie absolutnej ścieżki do folderu projektu
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    input_dir = os.path.join(project_dir, 'data', 'input')
    output_dir = os.path.join(project_dir, 'data', 'output')

    # Inicjalizacja procesora z pełnymi ścieżkami
    processor = RouteProcessor(input_dir=input_dir, output_dir=output_dir)

    # Sprawdzenie czy istnieją pliki do przetworzenia
    if not os.listdir(input_dir):
        raise FileNotFoundError(f"Brak plików w folderze {input_dir}")

    df = processor.merge_files()

    # Obliczanie odległości między punktami
    df['prev_lat'] = df['latitude'].shift()
    df['prev_lon'] = df['longitude'].shift()

    df['distance'] = df.apply(lambda row: geodesic(
        (row['prev_lat'], row['prev_lon']),
        (row['latitude'], row['longitude'])
    ).meters if pd.notnull(row['prev_lat']) else 0, axis=1)

    # Analiza wysokości
    df['elevation_gain'] = df['altitude'].diff().apply(lambda x: x if x > 0 else 0)

    # Tworzenie folderu output jeśli nie istnieje
    os.makedirs(output_dir, exist_ok=True)

    # Zapis wyników
    output_path = os.path.join(output_dir, 'advanced_stats.csv')
    summary = pd.DataFrame({
        'Total Distance (km)': [df['distance'].sum() / 1000],
        'Total Elevation Gain (m)': [df['elevation_gain'].sum()],
        'Max Speed (km/h)': [0]
    })

    summary.to_csv(output_path, index=False)
    print(f"Zapisano plik: {output_path}")
    return df


if __name__ == "__main__":
    try:
        advanced_analysis()
        print("Analiza zakończona pomyślnie!")
    except Exception as e:
        print(f"Błąd podczas analizy: {str(e)}")