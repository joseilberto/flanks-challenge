"""
Service to list SICAVs according to a specified query
"""

from sanic import Sanic
from sanic.log import LOGGING_CONFIG_DEFAULTS

from config import SERVICE_HOST, SERVICE_PORT
from handlers import InfoHandler, SearchHandler

# Configuring output handlers and filename

for log_key, _ in LOGGING_CONFIG_DEFAULTS["loggers"].items():
    LOGGING_CONFIG_DEFAULTS["loggers"][log_key]["handlers"].append(
        "internalFile"
    )

LOGGING_CONFIG_DEFAULTS["handlers"].update(
    {
        "internalFile": {
            "class": "logging.FileHandler",
            "formatter": "generic",
            "filename": "cnmv_service.log",
        }
    }
)

# Specifying the log formatters
LOGGING_CONFIG_DEFAULTS["formatters"] = {
    "generic": {
        "format": (
            "%(asctime)s.%(msecs)03dZ %(levelname)-8s "
            "(%(name)s %(funcName)s): %(message)s"
        ),
        "datefmt": "%Y-%m-%dT%H:%M:%S",
        "class": "logging.Formatter",
    },
    "access": {
        "format": (
            "%(asctime)s.%(msecs)03dZ %(levelname)-8s %(host)s %(request)s "
            "(%(name)s %(funcName)s): %(message)s"
        ),
        "datefmt": "%Y-%m-%dT%H:%M:%S",
        "class": "logging.Formatter",
    },
}


# Create the service and update its basic configuration
service = Sanic("SICAV_SERVICE", log_config=LOGGING_CONFIG_DEFAULTS)
service.config.update({"RESPONSE_TIMEOUT": 180, "REQUEST_TIMEOUT": 60})
# Assign endpoints to handlers
service.add_route(SearchHandler.as_view(), "/search", methods=["GET"])
service.add_route(InfoHandler.as_view(), "/isin_info", methods=["GET"])


if __name__ == "__main__":
    # Run the service
    service.run(SERVICE_HOST, SERVICE_PORT, workers=1, access_log=True)
