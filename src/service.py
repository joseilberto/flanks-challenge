"""
Service to list SICAVs according to a specified query
"""

from sanic import Sanic

from config import SERVICE_HOST, SERVICE_PORT
from handlers import InfoHandler, SearchHandler

# Create the service and update its basic configuration
service = Sanic("SICAV_SERVICE")
service.config.update({"RESPONSE_TIMEOUT": 180, "REQUEST_TIMEOUT": 60})
# Assign endpoints to handlers
service.add_route(SearchHandler.as_view(), "/search", methods=["GET"])
service.add_route(InfoHandler.as_view(), "/isin_info", methods=["GET"])


if __name__ == "__main__":
    # Run the service
    service.run(SERVICE_HOST, SERVICE_PORT, workers=1, access_log=True)
