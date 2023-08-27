"""Global tests configuration and fixtures"""

import asyncio

import pytest

from src.mongo import DataClient
from src.mongo.mongo_conn import MongoConnector

from .test_utils import DB_NAME, MONGO_HOST, MONGO_PORT


@pytest.fixture(scope="session")
def mongo_connector() -> MongoConnector:
    """Make a connector fixture"""
    return MongoConnector(MONGO_HOST, MONGO_PORT)


# pylint: disable=redefined-outer-name
@pytest.fixture(scope="session")
def data_client(mongo_connector: MongoConnector) -> DataClient:
    """Make a DataClient fixture"""
    client = DataClient(db_name=DB_NAME, connector=mongo_connector)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.set_index())
    return client
