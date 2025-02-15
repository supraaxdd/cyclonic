from cyclonic_controllers.request_controller import RequestController
from cyclonic_requests.request_enums import OpenMeteoRequestParams

if __name__ == "__main__":
    controller = RequestController()

    response = controller.send_om_request([OpenMeteoRequestParams.TEMP_2M, OpenMeteoRequestParams.WS_10M, OpenMeteoRequestParams.WD_10M])