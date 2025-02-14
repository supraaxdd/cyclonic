from .base_requester import BaseRequester
from .request_enums import RequestURL
from retry_requests import retry

import pandas as pd

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
        

    @classmethod
    def prepare_request(self, options: list):
        """
        Prepares the parameters for the API Request 
        """
        params = { 
            "latitude": 51.8413,
            "longitude": -8.4911,
            "hourly": options
        }

        return params
    
    @classmethod
    def send_request(self, params):
        """
        Sends API Request with prepared params
        """
        return self.om_client.weather_api(self.url, params=params)
    
    @classmethod
    def format_data(self, response):
        return {
            "lat": response.Latitude(),
            "long": response.Longitude(),
            "elevation": response.Elevation(), # m asl
            "timezone": response.Timezone()
        }