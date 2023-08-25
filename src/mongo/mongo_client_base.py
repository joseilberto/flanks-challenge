"""Define base mongo client class with basic connection methods"""
import logging
from datetime import datetime
from typing import Any, Dict, Optional, TypeAlias, TypedDict, Union

from motor import core

from .mongo_conn import MongoConnector

CollectionAlias: TypeAlias = core.AgnosticCollection


class ClientParams(TypedDict):
    """TypeDict for the MongoClientBase params"""

    db_name: str
    collection: str
    connector: Optional[MongoConnector]


class MongoClientBase:
    """Base class to manage interactions with mongo"""

    def __init__(
        self,
        db_name: str,
        collection: str,
        connector: Optional[MongoConnector] = None,
    ) -> None:
        """Initialise mongo client"""
        self.db_name = db_name
        self.connector = (
            connector if connector is not None else MongoConnector()
        )
        self.collection = collection

        self.log = logging.getLogger(__name__)
        self.log.info(
            "Mongo client for db %s configured using collection %s",
            db_name,
            self.collection,
        )

    def get_collection(self) -> Union[Any, CollectionAlias]:
        """Helper to access db and collection specified"""
        return self.connector.get_db(self.db_name)[self.collection]

    async def get_n_docs(
        self,
        query: Optional[Dict[str, Union[str, datetime, float, int]]] = None,
    ) -> Union[int, Any]:
        """Count the number of docs in the collection"""
        if query is None:
            query = {}
        return await self.get_collection().count_documents(query)
