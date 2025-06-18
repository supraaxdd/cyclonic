from pathlib import Path

import pandas as pd

def read_input_data(input_set: str):
    file_path = Path(Path.cwd(), input_set)
    return pd.read_json(file_path)

def create_folder_if_not_exists(path: str):
    output_path = Path(Path("").cwd(), path)

    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)