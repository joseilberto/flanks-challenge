"""
Service to list SICAVs according to a specified query
"""

import logging
import sys
from typing import no_type_check

from sanic import Sanic

from config import SERVICE_HOST, SERVICE_PORT

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s.%(msecs)03dZ %(levelname)-8s "
        "(%(name)s %(funcName)s): %(message)s"
    ),
    datefmt="%Y-%m-%dT%H:%M:%S",
    handlers=[
        logging.FileHandler("service.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


@no_type_check
def main() -> None:
    """Main method to configure and run service"""
    service = Sanic("SICAV_SERVICE")
    service.config.update({"RESPONSE_TIMEOUT": 180, "REQUEST_TIMEOUT": 60})
    service.run(SERVICE_HOST, SERVICE_PORT, workers=1)


if __name__ == "__main__":
    main()
