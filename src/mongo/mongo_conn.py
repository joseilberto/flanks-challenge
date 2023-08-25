"""Mongo Connector Class using motor"""

import asyncio
import logging
from typing import Optional, TypeAlias, no_type_check

import motor.motor_asyncio as motor
from motor import core

from config import MONGO_HOST, MONGO_PORT

ClientAlias: TypeAlias = core.AgnosticClient
DatabaseAlias: TypeAlias = core.AgnosticDatabase


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
        self.client: Optional[ClientAlias] = None

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
        assert loop.is_running()  # Check if we are running in an async loop

        uri = f"mongodb://{self.mongo_host}:{self.mongo_port}"
        self.client = motor.AsyncIOMotorClient(uri, io_loop=loop)

    def conn(self) -> Optional[ClientAlias]:
        """Get the instantiated client"""
        if self.client is None:
            self._initialise_client()

        return self.client

    @no_type_check
    def get_db(self, database_name: str) -> DatabaseAlias:
        """Get a particular database"""
        return self.conn()[database_name]
