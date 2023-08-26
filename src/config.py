"""
Config file containing the relevant variables we may set in our services 
and crawlers
"""

import os
from urllib.parse import urlparse

# Configuring the initial url the crawler uses and perform requests from this
# url onwards. We validate it with urlparse, we would like to break it as soon
# as possible if the url is not valid.
INITIAL_URL: str = urlparse(
    os.getenv(
        "INITIAL_URL",
        "https://www.cnmv.es/Portal/Consultas/MostrarListados.aspx?id=18",
    )
).geturl()

# Mongo connection information
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
