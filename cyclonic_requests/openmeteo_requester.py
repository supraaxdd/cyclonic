from .base_requester import BaseRequester
from .request_enums import RequestURL, OpenMeteoRequestParam
from retry_requests import retry
from utils.logger import logger_setup

import requests_cache
import openmeteo_requests

from datetime import datetime, timedelta

logger = logger_setup("OMREQ")


class OpenMeteoRequester(BaseRequester):
    """
    Wrapper class for the OpenMeteo API
    """

    def __init__(self):
        super().__init__()
        self.url = RequestURL.OPEN_METEO.value

        # Setting up cached session as per OpenMeteo API
        logger.debug("Setting up cached session...")
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)

        logger.debug("Instantiating Request Client...")
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
    
    def send_request(self, params):
        """
        Sends API Request with prepared params
        """
        return self.om_client.weather_api(self.url, params=params)[0]