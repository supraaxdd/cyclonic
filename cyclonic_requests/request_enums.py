from enum import Enum

class RequestURL(Enum):
    OPEN_METEO = "https://api.open-meteo.com/v1/forecast"
    OPEN_METEO_PREVIOUS = "https://previous-runs-api.open-meteo.com/v1/forecast"
    
class OpenMeteoRequestParam(Enum):
    TEMP_2M = "temperature_2m"
    TEMP_80M = "temperature_80m"
    TEMP_120M = "temperature_120m"
    TEMP_180M = "temperature_180m"
    SURFACE_PRESSURE = "surface_pressure"
    WS_10M = "wind_speed_10m"
    WS_80M = "wind_speed_80m"
    WS_120M = "wind_speed_120m"
    WS_180M = "wind_speed_180m"
    WD_10M = "wind_direction_10m"
    WD_80M = "wind_direction_80m"
    WD_120M = "wind_direction_120m"
    WD_180M = "wind_direction_180m"
    WG_10M = "wind_gusts_10m"
    ST_0CM = "soil_temperature_0cm"
    ST_6CM = "soil_temperature_6cm"
    ST_18CM = "soil_temperature_18cm"
    ST_54CM = "soil_temperature_54cm"