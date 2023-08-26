"""Mongo Client used to read and write data into the database"""

import logging
from datetime import datetime
from typing import List, Unpack

from pymongo import ASCENDING
from pymongo.operations import IndexModel

from crawler.pipelines import DataTypes

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

    async def set_index(self) -> List[str]:
        """Set indexes in mongo collection"""
        index = IndexModel(
            [
                ("nombre", ASCENDING),
                ("numero_registro", ASCENDING),
                ("isin", ASCENDING),
                ("fecha_registro", ASCENDING),
            ],
            background=True,
        )
        result = await self.get_collection().create_indexes([index])
        if isinstance(result, list):
            self.log.debug("Set indexes")
            return result
        msg = f"Couldn't set indexes, got the following result: {result}"
        self.log.error(msg)
        raise ValueError(msg)

    async def set_data(self, result: DataTypes) -> bool:
        """
        Set the data for a particular entry
        """
        assert isinstance(result, DataTypes)

        query = {
            "nombre": result.nombre,
            "numero_registro": result.numero_registro,
        }
        # Set up and save the data
        data = {"write_date": datetime.now(), **result._asdict()}
        self.log.debug("Setting data for dictionary: %s", data)

        success = await self.get_collection().update_one(
            query, {"$set": data}, upsert=True
        )

        self.log.info(
            "Data set for %s with numero_registro: %s",
            query["nombre"],
            query["numero_registro"],
        )

        return success.acknowledged
