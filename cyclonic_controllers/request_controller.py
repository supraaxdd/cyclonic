from cyclonic_requests.openmeteo_requester import OpenMeteoRequester
from cyclonic_requests.request_enums import OpenMeteoRequestParam

from utils.logger import logger_setup
logger = logger_setup(name="REQCTRL")

class RequestController:
    def __init__(self):
        self.om_requester = OpenMeteoRequester()

    def send_om_request(self, options: list[OpenMeteoRequestParam], previous: bool = False, days : int = 30):
        logger.debug("Preparing request parameters...")
        try:
            params = self.om_requester.prepare_request(options, num_days=days, previous=previous)

            logger.debug("Sending OpenMeteo request...")
            response = self.om_requester.send_request(params, previous=previous)

            return response
        except Exception as e:
            logger.error(e)
            exit(1)


    
    