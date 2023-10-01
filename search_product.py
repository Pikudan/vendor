#  <#Title#>
import os
import pandas as pd
from pathlib import Path
           
def search_product(data):
    if len(data) < 3:
        return None
    path_folder = os.path.dirname(__file__)
    filename = data[0]
    path_output_file = os.path.join(path_folder, f'{filename}.csv')
    base_data = "stas_nan"
    path_input_file = os.path.join(path_folder, f'{base_data}.csv')
    df = pd.read_csv(path_input_file, delimiter=";", low_memory=False)
    df.to_csv(path_output_file)
    return path_output_file
    
