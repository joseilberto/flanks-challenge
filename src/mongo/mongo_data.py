"""Mongo Client used to read and write data into the database"""

import logging
from typing import Any, List, Union, Unpack

from pymongo import ASCENDING
from pymongo.operations import IndexModel

from .mongo_client_base import ClientParams, MongoClientBase


class MongoDataClient(MongoClientBase):
    """Read and write data into the database"""

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

    async def set_index(self) -> Union[Any, List[str]]:
        """Set indexes in mongo collection"""
        index = IndexModel(
            [("nombre", ASCENDING), ("numero_registro", ASCENDING)],
            background=True,
        )
        result = await self.get_collection().create_indexes([index])
        self.log.debug("Set indexes")
        return result
