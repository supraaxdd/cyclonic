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

    # Which parameters to request
    parser.add_argument(
        "--params",
        nargs="+",
        choices=[p.name for p in OpenMeteoRequestParam],
        default=[
            "TEMP_2M", "SURFACE_PRESSURE", "WS_10M", "WS_80M",
            "WS_120M", "WS_180M", "WD_10M", "WD_80M", "WD_120M",
            "WD_180M", "WG_10M", "TEMP_80M", "TEMP_120M",
            "TEMP_180M", "ST_0CM", "ST_6CM", "ST_18CM", "ST_54CM"
        ],
        help="List of OpenMeteoRequestParam names to fetch"
    )

    parser.add_argument(
        "--lat",
        type=float,
        default=51.8413,
        help="Latitude co-ordinate as a float"
    )

    parser.add_argument(
        "--long",
        type=float,
        default=-8.4911,
        help="Longitude co-ordinate as a float"
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    logger.debug(f"Arguments: previous={args.previous}, days={args.days}, lat={args.lat}, long={args.long}, params={args.params}")

    logger.debug("Setting up Controller Classes...")
    controller = RequestController()
    formatter = OpenMeteoFormatter()

    requested_params = [OpenMeteoRequestParam[name] for name in args.params]

    locations = controller.find_second_location(args.lat, args.long)
    second_location = locations[0]
    
    logger.info("Sending Request to OpenMeteo...")
    df_1, df_2 = controller.get_weather_data(
        requested_params,
        days=args.days,
        previous=args.previous,
        lat=args.lat,
        long=args.long
    )

    compiled_df = formatter.compile_data(df_1, df_2)
    formatter.write(compiled_df, previous=args.previous)

    logger.info("Finished Data fetching")