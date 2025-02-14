from enum import Enum

class RequestURL(Enum):
    OPEN_METEO = "https://api.open-meteo.com/v1/forecast"
    
class OpenMeteoRequestParams(Enum):
    TEMP_2M = "temperature_2m"
    WS_10M = "wind_speed_10m"
    WS_100M = "wind_speed_100m"
    WD_10M = "wind_direction_10m"
    WD_100M = "wind_direction_100m"
    WG_10M = "wind_gusts_10m"