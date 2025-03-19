from .base_requester import BaseRequester
from .request_enums import RequestURL, OpenMeteoRequestParam
from retry_requests import retry

import requests_cache
import openmeteo_requests

from datetime import datetime, timedelta


class OpenMeteoRequester(BaseRequester):
    """
    Wrapper class for the OpenMeteo API
    """

    def __init__(self):
        super().__init__()

        # Setting up cached session as per OpenMeteo API
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)

        self.om_client = openmeteo_requests.Client(session = retry_session)
        

    def prepare_request(self, options: list[OpenMeteoRequestParam], lat: float = 51.8413, long: float = -8.4911):
        """
        Prepares the parameters for the API Request 
        """
        today = datetime.today()
        today_formatted = today.strftime('%Y-%m-%d')
        five_days_prior = today - timedelta(7)
        five_days_prior_formatted = five_days_prior.strftime('%Y-%m-%d')
            
        params = { 
            "latitude": lat,
            "longitude": long,
            "hourly": [option.value for option in options],
            "start_date": five_days_prior_formatted,
	        "end_date": today_formatted
        }

        return params
    
    def send_request(self, params, previous: bool = False):
        """
        Sends API Request with prepared params
        """

        url = RequestURL.OPEN_METEO_PREVIOUS.value if previous else RequestURL.OPEN_METEO.value
        return self.om_client.weather_api(url=url, params=params)[0]