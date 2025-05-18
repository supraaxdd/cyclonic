import sys, argparse

from cyclonic_controllers.request_controller import RequestController
from cyclonic_requests.request_enums import OpenMeteoRequestParam
from cyclonic_formatting.openmeteo_formatter import OpenMeteoFormatter
from utils.logger import logger_setup

from pathlib import Path

import json

logger = logger_setup(name="MAIN")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch and format weather data via the Cyclonic Data Module"
    )

    # Flag for whether to include previous days
    parser.add_argument(
        "-p", "--previous",
        action="store_true",
        help="Include previous days' data"
    )

    # How many days foward or back
    parser.add_argument(
        "-d", "--days",
        type=int,
        default=14,
        metavar="N",
        help="Number of previous days to fetch (default: 14)"
    )

    # # Which parameters to request
    # parser.add_argument(
    #     "--params",
    #     nargs="+",
    #     choices=[p.name for p in OpenMeteoRequestParam],
    #     default=[
    #         "TEMP_2M", "SURFACE_PRESSURE", "WS_10M", "WS_80M",
    #         "WS_120M", "WS_180M", "WD_10M", "WD_80M", "WD_120M",
    #         "WD_180M", "WG_10M", "TEMP_80M", "TEMP_120M",
    #         "TEMP_180M", "ST_0CM", "ST_6CM", "ST_18CM", "ST_54CM"
    #     ],
    #     help="List of OpenMeteoRequestParam names to fetch"
    # )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    params = [
            "TEMP_2M", "SURFACE_PRESSURE", "WS_10M", "WS_80M",
            "WS_120M", "WS_180M", "WD_10M", "WD_80M", "WD_120M",
            "WD_180M", "WG_10M", "TEMP_80M", "TEMP_120M",
            "TEMP_180M", "ST_0CM", "ST_6CM", "ST_18CM", "ST_54CM"
        ]
    logger.debug(f"Arguments: previous={args.previous}, days={args.days}, params={params}")

    logger.debug("Setting up Controller Classes...")
    controller = RequestController()
    formatter = OpenMeteoFormatter()

    requested_params = [OpenMeteoRequestParam[name] for name in args.params]

    logger.debug("Sending Request to OpenMeteo...")
    response = controller.send_om_request(
        requested_params,
        days=args.days,
        previous=args.previous
    )

    logger.debug("Formatting reponse received from OpenMeteo...")
    result = formatter.format_data(response, True)
    output = json.dumps(result, indent=4)

    logger.debug("Writing to /output/result.json...")

    if not Path("./output").exists():
        Path("./output").mkdir(parents=True, exist_ok=True)

    with open("./output/result.json", 'w') as f:
        f.write(output)

    logger.debug("Finished Data fetching")