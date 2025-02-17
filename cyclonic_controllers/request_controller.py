from cyclonic_requests.openmeteo_requester import OpenMeteoRequester
from cyclonic_requests.request_enums import OpenMeteoRequestParam

class RequestController:
    def __init__(self):
        self.om_requester = OpenMeteoRequester()

    def send_om_request(self, options: list[OpenMeteoRequestParam]):
        params = self.om_requester.prepare_request(options)
        response = self.om_requester.send_request(params)

        return response