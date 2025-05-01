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

        # Setting up cached session as per OpenMeteo API
        logger.debug("Setting up cached session...")
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)

        logger.debug("Instantiating Request Client...")
        self.om_client = openmeteo_requests.Client(session = retry_session)
        

    def prepare_request(self, options: list[OpenMeteoRequestParam], previous: bool = False, num_days: int = 30, lat: float = 51.8413, long: float = -8.4911):
        """
        Prepares the parameters for the API Request 
        """
        today = datetime.today()
        today_formatted = today.strftime('%Y-%m-%d')

        start_date = None
        end_date = None
        days = None
        days_formatted = None

        if previous:
            days = today - timedelta(days=num_days)
            days_formatted = days.strftime('%Y-%m-%d')
            start_date = days_formatted
            end_date = today_formatted
        else:
            if num_days > 15:
                raise Exception("Max number of days permitted into the future is 16 days")
            days = today + timedelta(days=num_days)
            days_formatted = days.strftime('%Y-%m-%d')
            start_date = today_formatted
            end_date = days_formatted

        params = { 
            "latitude": lat,
            "longitude": long,
            "hourly": [option.value for option in options],
            "start_date": start_date,
	        "end_date": end_date
        }

        return params
    
    def send_request(self, params, previous: bool = False):
        """
        Sends API Request with prepared params
        """
        url = RequestURL.OPEN_METEO_PREVIOUS.value if previous else RequestURL.OPEN_METEO.value
        return self.om_client.weather_api(url=url, params=params)[0]