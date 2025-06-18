from pathlib import Path

import pandas as pd

def read_input_data(input_set: str):
    file_path = Path(Path.cwd(), input_set)
    return pd.read_json(file_path)