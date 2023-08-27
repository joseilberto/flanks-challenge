"""Mongo Client used to read and write data into the database"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, TypedDict, Union, Unpack

from pymongo import ASCENDING
from pymongo.operations import IndexModel

from crawler.pipelines import DataTypes

from .mongo_client_base import ClientParams, MongoClientBase


class DocumentType(TypedDict):
    """
    Document entry type for the database
    """

    nombre: str
    numero_registro: str
    fecha_registro: str
    isin: str
    domicilio: str
    capital_inicial: float
    capital_maximo: float
    fecha_ultimo_folleto: str
    last_update: str
    write_date: datetime
    updates: Dict[str, Dict[str, Union[str, float]]]


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

    async def find_entry(self, query: Dict[str, str]) -> Optional[DocumentType]:
        """Find specific entry using the query provided"""
        proj = {"_id": 0}
        document: Optional[DocumentType] = await self.get_collection().find_one(
            query, proj
        )
        if document is None:
            return None
        return document

    async def set_data(self, result: DataTypes) -> bool:
        """
        Set the data for a particular entry
        """
        assert isinstance(result, DataTypes)

        query = {
            "nombre": result.nombre,
            "numero_registro": result.numero_registro,
            "fecha_registro": result.fecha_registro,
            "isin": result.isin,
        }
        # Find existing document first (if any)
        document = await self.find_entry(query)
        if document is None:
            # No record exists in the database for this particular entity.
            # Set up and save the data
            return await self._set_new_entry(result)
        return await self._update_existing_entry(query, document, result)

    async def _set_new_entry(self, result: DataTypes) -> bool:
        """Set a new entry in the database"""
        write_date = datetime.now()
        data = {
            "last_update": write_date.strftime("%Y-%m-%d"),  # ISO 8601
            "write_date": write_date,
            "updates": {},
            **result._asdict(),
        }
        self.log.debug("Setting data for dictionary: %s", data)

        success = await self.get_collection().insert_one(data)

        self.log.info(
            "Data set for %s with numero_registro: %s, isin: %s and"
            " fecha_registro: %s",
            result.nombre,
            result.numero_registro,
            result.isin,
            result.fecha_registro,
        )

        return success.acknowledged

    async def _update_existing_entry(
        self,
        query: Dict[str, str],
        document: DocumentType,
        result: DataTypes,
    ) -> bool:
        """
        Update an existing entry in the database with the differences if we have
        any differences. Otherwise, we don't update any entries.
        """
        # Check the differences between the document in the database and
        # the income document
        differences = {
            field: document[field]  # type: ignore
            for field, value in result._asdict().items()
            if value != document[field]  # type: ignore
        }
        if not differences:
            return True

        # Store the differences in the updates dict in the document
        for field, value in differences.items():
            update = {document["last_update"]: value}
            if field in document["updates"]:
                document["updates"][field].update(update.copy())
                continue
            document["updates"][field] = update.copy()

        # Prepare to write in the database
        write_date = datetime.now()

        data = {
            "last_update": write_date.strftime("%Y-%m-%d"),  # ISO 8601
            "write_date": write_date,
            "updates": document["updates"],
            **result._asdict(),
        }

        self.log.debug("Setting data for dictionary: %s", data)

        success = await self.get_collection().update_one(
            query, data, upsert=True
        )

        self.log.info(
            "Data set for %s with numero_registro: %s, isin: %s and"
            " fecha_registro: %s with updates: %s",
            result.nombre,
            result.numero_registro,
            result.isin,
            result.fecha_registro,
            data["updates"],
        )

        return success.acknowledged
