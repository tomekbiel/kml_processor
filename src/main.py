import argparse
import os
from src.core.processor import RouteProcessor
from src.core.analyzer import RouteAnalyzer
from src.core.converter import df_to_kml


def main():
    parser = argparse.ArgumentParser(description='KML/GPX Processor')
    parser.add_argument('--action',
                        choices=['process', 'convert', 'analyze'],
                        default='process',
                        help='Wybierz akcję: process, convert, analyze')
    parser.add_argument('--input',
                        default='data/input',
                        help='Ścieżka do pliku/folderu wejściowego')
    parser.add_argument('--output',
                        default='data/output',
                        help='Ścieżka do pliku/folderu wyjściowego')

    args = parser.parse_args()

    processor = RouteProcessor(args.input, args.output)

    if args.action == 'process':
        df = processor.merge_files()
        clean_df = processor.clean_data(df)
        df_to_kml(clean_df, os.path.join(args.output, 'processed_routes.kml'))
        print("Przetwarzanie zakończone!")


if __name__ == "__main__":
    main()