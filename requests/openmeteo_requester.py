from base_requester import BaseRequester
from request_enums import RequestURL
import openmeteo_requests

class OpenMeteoRequester(BaseRequester):
    def __init__(self):
        super().__init__()
        self.url = RequestURL.OPEN_METEO
        self.om_client = openmeteo_requests.Client()

    def prepare_request(self, **kwargs):
        prepared_request = self.url

        return prepared_request
        # return super().prepare_request(**kwargs)
    
    def send_request(self, params):
        return super().send_request(params)
    
    def format_data(self, response):
        return super().format_data(response)