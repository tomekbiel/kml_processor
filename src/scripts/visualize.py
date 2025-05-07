# src/scripts/visualize.py
import os
import matplotlib.pyplot as plt
from src.core.processor import RouteProcessor


def plot_elevation(df, output_dir):
    plt.figure(figsize=(12, 6))
    df['altitude'].plot(title='Profil wysokościowy trasy')
    plt.xlabel('Punkt trasy')
    plt.ylabel('Wysokość (m n.p.m.)')

    output_path = os.path.join(output_dir, 'elevation_profile.png')
    plt.savefig(output_path)
    plt.close()  # Zamiast show() aby uniknąć zawieszania skryptu
    print(f"Zapisano wykres: {output_path}")


if __name__ == "__main__":
    try:
        # Ścieżki absolutne
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        input_dir = os.path.join(project_dir, 'data', 'input')
        output_dir = os.path.join(project_dir, 'data', 'output')

        # Sprawdzenie folderu wejściowego
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Folder {input_dir} nie istnieje")

        if len(os.listdir(input_dir)) == 0:
            raise ValueError("Brak plików w folderze input")

        # Przetwarzanie
        processor = RouteProcessor(input_dir=input_dir, output_dir=output_dir)
        df = processor.merge_files()

        if df.empty:
            raise ValueError("DataFrame jest pusty - sprawdź pliki wejściowe")

        plot_elevation(df, output_dir)
        print("Wizualizacja zakończona pomyślnie!")

    except Exception as e:
        print(f"Błąd: {str(e)}")
        exit(1)