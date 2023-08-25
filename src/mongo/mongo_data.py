"""Mongo Client used to read and write data into the database"""

import logging
from typing import Unpack

from .mongo_client_base import ClientParams, MongoClientBase


class MongoDataClient(MongoClientBase):
    """Read and write data into the database"""

    # pylint: disable=too-few-public-methods

    def __init__(self, **kwargs: Unpack[ClientParams]) -> None:
        """Initialise a mongo configs client"""
        super().__init__(**kwargs)
        if self.collection is None:
            self.collection = "cnmv_data"  # Set a default
        self.log = logging.getLogger(__name__)
        self.log.info(
            "Mongo client for db %s configured, using collection %s",
            self.db_name,
            self.collection,
        )
