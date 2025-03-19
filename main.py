from cyclonic_controllers.request_controller import RequestController
from cyclonic_requests.request_enums import OpenMeteoRequestParam
from cyclonic_formatting.openmeteo_formatter import OpenMeteoFormatter

import json

if __name__ == "__main__":
    controller = RequestController()
    formatter = OpenMeteoFormatter()

    response = controller.send_om_request([
        OpenMeteoRequestParam.TEMP_2M,
        OpenMeteoRequestParam.SURFACE_PRESSURE,
        OpenMeteoRequestParam.WS_10M,
        OpenMeteoRequestParam.WS_80M,
        OpenMeteoRequestParam.WS_120M,
        OpenMeteoRequestParam.WS_180M,
        OpenMeteoRequestParam.WD_10M,
        OpenMeteoRequestParam.WD_80M,
        OpenMeteoRequestParam.WD_120M,
        OpenMeteoRequestParam.WD_180M,
        OpenMeteoRequestParam.WG_10M,
        OpenMeteoRequestParam.TEMP_80M,
        OpenMeteoRequestParam.TEMP_120M,
        OpenMeteoRequestParam.TEMP_180M,
        OpenMeteoRequestParam.ST_0CM,
        OpenMeteoRequestParam.ST_6CM,
        OpenMeteoRequestParam.ST_18CM,
        OpenMeteoRequestParam.ST_54CM
    ], True)

    result = formatter.format_data(response, True)
    output = json.dumps(result, indent=4)

    with open("./output/result.json", 'w') as f:
        f.write(output)