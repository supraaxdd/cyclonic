from cyclonic_controllers.request_controller import RequestController
from cyclonic_requests.request_enums import OpenMeteoRequestParam

if __name__ == "__main__":
    controller = RequestController()

    response = controller.send_om_request([OpenMeteoRequestParam.TEMP_2M, OpenMeteoRequestParam.WS_10M, OpenMeteoRequestParam.WD_10M])