import os
from core.converter import kml_to_df, df_to_kml, gpx_to_df, df_to_gpx


def batch_convert(input_dir, output_dir, from_format, to_format):
    for file in os.listdir(input_dir):
        if file.endswith(f'.{from_format}'):
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir,
                                       file.replace(f'.{from_format}', f'.{to_format}'))

            if from_format == 'kml':
                df = kml_to_df(input_path)
                if to_format == 'gpx':
                    df_to_gpx(df, output_path)
            # Analogicznie dla innych kombinacji