"""
Service to list SICAVs according to a specified query
"""

import logging
from typing import no_type_check

from sanic import Sanic

from config import DB_NAME, SERVICE_HOST, SERVICE_PORT
from handlers import SearchHandler
from mongo import DataClient

LOGGING_CONFIG = {
    "level": logging.INFO,
    "format": (
        "%(asctime)s.%(msecs)03dZ %(levelname)-8s "
        "(%(name)s %(funcName)s): %(message)s"
    ),
    "datefmt": "%Y-%m-%dT%H:%M:%S",
}


@no_type_check
def main() -> None:
    """Main method to configure and run service"""
    # Create the service and update its basic configuration
    service = Sanic("SICAV_SERVICE", log_config=LOGGING_CONFIG)
    service.config.update({"RESPONSE_TIMEOUT": 180, "REQUEST_TIMEOUT": 60})

    # Create handlers
    data_client = DataClient(db_name=DB_NAME)
    search_handler = SearchHandler(data_client)

    # Assign endpoints to handlers
    service.add_route(search_handler, "/search")

    # Run the service
    service.run(SERVICE_HOST, SERVICE_PORT, workers=1, access_log=True)


if __name__ == "__main__":
    main()
