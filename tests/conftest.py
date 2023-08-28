"""Global tests configuration and fixtures"""

import asyncio
from typing import Generator

import pytest

from src.mongo import DataClient
from src.mongo.mongo_conn import MongoConnector
from tests.test_utils import DB_NAME, MONGO_HOST, MONGO_PORT


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator:
    """Initialize an event loop so that async autouse fixtures work"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


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
    loop.run_until_complete(client.delete_docs())
    loop.run_until_complete(client.set_index())
    return client
