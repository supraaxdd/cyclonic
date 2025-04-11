from .base_formatter import BaseFormatter
from utils.logger import logger_setup

logger = logger_setup("OMFMTR")

import pandas as pd
import json

class OpenMeteoFormatter(BaseFormatter):
    def __init__(self):
        super().__init__()

    def format_data(self, response, use_json: bool = False):
        result = { 
            "lat": response.Latitude(),
            "long": response.Longitude(),
            "elevation": response.Elevation(), # m asl
            "timezone": response.Timezone()	
        }

        logger.debug("Getting hourly variables...")

        # The following is taken from the API
        hourly = response.Hourly()

        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_surface_pressure = hourly.Variables(1).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
        hourly_wind_speed_80m = hourly.Variables(3).ValuesAsNumpy()
        hourly_wind_speed_120m = hourly.Variables(4).ValuesAsNumpy()
        hourly_wind_speed_180m = hourly.Variables(5).ValuesAsNumpy()
        hourly_wind_direction_10m = hourly.Variables(6).ValuesAsNumpy()
        hourly_wind_direction_80m = hourly.Variables(7).ValuesAsNumpy()
        hourly_wind_direction_120m = hourly.Variables(8).ValuesAsNumpy()
        hourly_wind_direction_180m = hourly.Variables(9).ValuesAsNumpy()
        hourly_wind_gusts_10m = hourly.Variables(10).ValuesAsNumpy()
        hourly_temperature_80m = hourly.Variables(11).ValuesAsNumpy()
        hourly_temperature_120m = hourly.Variables(12).ValuesAsNumpy()
        hourly_temperature_180m = hourly.Variables(13).ValuesAsNumpy()
        hourly_soil_temperature_0cm = hourly.Variables(14).ValuesAsNumpy()
        hourly_soil_temperature_6cm = hourly.Variables(15).ValuesAsNumpy()
        hourly_soil_temperature_18cm = hourly.Variables(16).ValuesAsNumpy()
        hourly_soil_temperature_54cm = hourly.Variables(17).ValuesAsNumpy()

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
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["surface_pressure"] = hourly_surface_pressure
        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
        hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
        hourly_data["wind_speed_120m"] = hourly_wind_speed_120m
        hourly_data["wind_speed_180m"] = hourly_wind_speed_180m
        hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
        hourly_data["wind_direction_80m"] = hourly_wind_direction_80m
        hourly_data["wind_direction_120m"] = hourly_wind_direction_120m
        hourly_data["wind_direction_180m"] = hourly_wind_direction_180m
        hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
        hourly_data["temperature_80m"] = hourly_temperature_80m
        hourly_data["temperature_120m"] = hourly_temperature_120m
        hourly_data["temperature_180m"] = hourly_temperature_180m
        hourly_data["soil_temperature_0cm"] = hourly_soil_temperature_0cm
        hourly_data["soil_temperature_6cm"] = hourly_soil_temperature_6cm
        hourly_data["soil_temperature_18cm"] = hourly_soil_temperature_18cm
        hourly_data["soil_temperature_54cm"] = hourly_soil_temperature_54cm
        hourly_data["date"] = hourly_data["date"].to_series().dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        if (use_json):
            result["hourly"] = pd.DataFrame(data=hourly_data).to_dict(orient="records")
        else:
            result["hourly"] = pd.DataFrame(data=hourly_data)

        return result