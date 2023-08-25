"""Mongo Connector Class using motor"""

import asyncio
import logging

import motor.motor_asyncio as motor

from config import MONGO_HOST, MONGO_PORT


class MongoConnector:
    """Class to share motor connection to mongo"""

    def __init__(
        self, mongo_host: str = MONGO_HOST, mongo_port: str = MONGO_PORT
    ):
        """Initialise an instance of the MongoConnector"""

        self.log = logging.getLogger(__name__)
        self.mongo_host = mongo_host
        self.mongo_port = int(mongo_port)
        self.log.info(
            "Creating mongo connector for %s:%s",
            self.mongo_host,
            self.mongo_port,
        )
        self.client = None

    def _initialise_client(self) -> None:
        """
        Initialise the connection to mongo. We expect the event loop to be
        running
        """
        self.log.info(
            "Initialising mongo client for %s:%s",
            self.mongo_host,
            self.mongo_port,
        )

        loop = asyncio.get_event_loop()

        uri = f"mongodb://{self.mongo_host}:{self.mongo_port}"
        self.client = motor.AsyncIOMotorClient(uri, io_loop=loop)

    def conn(self) -> motor.AsyncIOMotorClient:
        """Get the instantiated client"""
        if self.client is None:
            self._initialise_client()

        return self.client

    def get_db(self, database_name: str) -> motor.AsyncIOMotorDatabase:
        """Get a particular database"""
        return self.conn()[database_name]
