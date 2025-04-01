from cyclonic_requests.openmeteo_requester import OpenMeteoRequester
from cyclonic_requests.request_enums import OpenMeteoRequestParam

from utils.logger import logger_setup
logger = logger_setup(name="REQCTRL")

class RequestController:
    def __init__(self):
        self.om_requester = OpenMeteoRequester()

    def send_om_request(self, options: list[OpenMeteoRequestParam], previous: bool = False):
        params = self.om_requester.prepare_request(options)

        logger.debug("Sending OpenMeteo request...")
        response = self.om_requester.send_request(params, previous=previous)

        return response
    
    