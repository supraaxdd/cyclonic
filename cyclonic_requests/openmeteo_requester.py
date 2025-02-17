from .base_requester import BaseRequester
from .request_enums import RequestURL, OpenMeteoRequestParam
from retry_requests import retry

import requests_cache
import openmeteo_requests


class OpenMeteoRequester(BaseRequester):
    """
    Wrapper class for the OpenMeteo API
    """

    def __init__(self):
        super().__init__()
        self.url = RequestURL.OPEN_METEO.value

        # Setting up cached session as per OpenMeteo API
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)

        self.om_client = openmeteo_requests.Client(session = retry_session)
        

    def prepare_request(self, options: list[OpenMeteoRequestParam], lat: float = 51.8413, long: float = -8.4911):
        """
        Prepares the parameters for the API Request 
        """
        params = { 
            "latitude": lat,
            "longitude": long,
            "hourly": [option.value for option in options]
        }

        return params
    
    def send_request(self, params):
        """
        Sends API Request with prepared params
        """
        return self.om_client.weather_api(self.url, params=params)[0]