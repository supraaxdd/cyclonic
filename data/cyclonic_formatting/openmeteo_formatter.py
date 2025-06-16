from .base_formatter import BaseFormatter
from utils.logger import logger_setup
from utils.geo import calculate_air_density, calculate_distance, calculate_pgf_components, calculate_pgf_time_series

from pathlib import Path
from datetime import datetime
from pandas import DataFrame

from typing import Any

logger = logger_setup("OMFMTR")

import pandas as pd
import json

class OpenMeteoFormatter(BaseFormatter):
    def __init__(self):
        super().__init__()
        self.OUTPUT_PATH = Path(Path("").cwd(), "./output")

    def format_data(self, response) -> DataFrame:
        logger.debug("Getting hourly variables...")

        # The following is taken from the API
        hourly = response.Hourly()

        logger.debug("Compiling variables...")
        hourly_data = {
            "date": pd.date_range(
                start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = hourly.Interval()),
                inclusive = "left"
            )
        }

        logger.debug("Mapping variables to result...")

        hourly_data["lat"] = response.Latitude()
        hourly_data["long"] = response.Longitude()
        hourly_data["elevation"] = response.Elevation() # m asl
        hourly_data["temperature_2m"] = hourly.Variables(0).ValuesAsNumpy()
        hourly_data["surface_pressure"] = hourly.Variables(1).ValuesAsNumpy()
        hourly_data["wind_speed_10m"] = hourly.Variables(2).ValuesAsNumpy()
        hourly_data["wind_speed_80m"] = hourly.Variables(3).ValuesAsNumpy()
        hourly_data["wind_speed_120m"] = hourly.Variables(4).ValuesAsNumpy()
        hourly_data["wind_speed_180m"] = hourly.Variables(5).ValuesAsNumpy()
        hourly_data["wind_direction_10m"] = hourly.Variables(6).ValuesAsNumpy()
        hourly_data["wind_direction_80m"] = hourly.Variables(7).ValuesAsNumpy()
        hourly_data["wind_direction_120m"] = hourly.Variables(8).ValuesAsNumpy()
        hourly_data["wind_direction_180m"] = hourly.Variables(9).ValuesAsNumpy()
        hourly_data["wind_gusts_10m"] = hourly.Variables(10).ValuesAsNumpy()
        hourly_data["temperature_80m"] = hourly.Variables(11).ValuesAsNumpy()
        hourly_data["temperature_120m"] = hourly.Variables(12).ValuesAsNumpy()
        hourly_data["temperature_180m"] = hourly.Variables(13).ValuesAsNumpy()
        hourly_data["soil_temperature_0cm"] = hourly.Variables(14).ValuesAsNumpy()
        hourly_data["soil_temperature_6cm"] = hourly.Variables(15).ValuesAsNumpy()
        hourly_data["soil_temperature_18cm"] = hourly.Variables(16).ValuesAsNumpy()
        hourly_data["soil_temperature_54cm"] = hourly.Variables(17).ValuesAsNumpy()

        hourly_data["date"] = hourly_data["date"].to_series().dt.strftime('%Y-%m-%dT%H:%M:%SZ') # type: ignore

        result = pd.DataFrame(data=hourly_data)

        return result

    def merge_data(self, df_1: DataFrame, df_2: DataFrame):
        logger.debug("Merging data from two locations...")
        merged_df = df_1.merge(df_2, on="date", how="inner")

        return merged_df
    
    def calculate_pgf_df(self, merged_df: DataFrame) -> DataFrame:
        logger.debug("Calculating PGF values...")
        pgf_df = calculate_pgf_time_series(merged_df)
        new_df = pd.concat([merged_df.reset_index(drop=True), pgf_df], axis=1)

        return new_df
    
    def calculate_deltas(self, df: pd.DataFrame, pressure_col="surface_pressure", temp_col="temperature_2m", hours: int = 3) -> pd.DataFrame:
        logger.debug("Calculating deltas...")
        df[f"{pressure_col}_x_delta_{hours}h"] = df[f"{pressure_col}_x"].diff(periods=hours)
        df[f"{pressure_col}_y_delta_{hours}h"] = df[f"{pressure_col}_y"].diff(periods=hours)
        df[f"{temp_col}_x_delta_{hours}h"] = df[f"{temp_col}_x"].diff(periods=hours)
        df[f"{temp_col}_y_delta_{hours}h"] = df[f"{temp_col}_y"].diff(periods=hours)
        df.dropna(inplace=True)
        return df
    
    def compile_data(self, df_1: DataFrame, df_2: DataFrame) -> DataFrame:
        FEATURES = [
            "date",
            "lat1", "long1", "elev1", "temp1", "pressure1", "wind_speed_10m_x",
            "lat2", "long2", "elev2", "temp2", "pressure2",
            "temperature_2m_x_delta_3h", "temperature_2m_y_delta_3h",
            "surface_pressure_x_delta_3h", "surface_pressure_y_delta_3h",
            "PGF_x", "PGF_y", "PGF_magnitude"
            # "coast_dist"
        ]

        logger.debug("Compiling Data...")
        merged_df = self.merge_data(df_1, df_2)
        pgf_df = self.calculate_pgf_df(merged_df)
        complete_df = self.calculate_deltas(pgf_df)

        complete_df.rename(columns={
            "lat_x": "lat1", "long_x": "long1", "elevation_x": "elev1",
            "lat_y": "lat2", "long_y": "long2", "elevation_y": "elev2",
            "temperature_2m_x": "temp1", "temperature_2m_y": "temp2",
            "surface_pressure_x": "pressure1", "surface_pressure_y": "pressure2"
        }, inplace=True)

        return complete_df[FEATURES]
    
    def write(self, data: DataFrame, previous: bool) -> Path:
        file_path = ""
        past_dir = self.OUTPUT_PATH / "past"
        forecast_dir = self.OUTPUT_PATH / "forecast"
        
        today = datetime.today()
        today_formatted = today.strftime('%Y_%m_%d_%H%M%S')

        # Ensure directories exist
        if not self.OUTPUT_PATH.exists():
            self.OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
        if not past_dir.exists():
            past_dir.mkdir(parents=True, exist_ok=True)
        if not forecast_dir.exists():
            forecast_dir.mkdir(parents=True, exist_ok=True)

        if previous:
            file_path = past_dir / f"result_past_{today_formatted}.json"
        else:
            file_path = forecast_dir / f"result_forecast_{today_formatted}.json"

        logger.debug(f"Writing to {file_path}...")

        # Write using records orientation
        data.to_json(file_path, orient="records", indent=4)

        return file_path
