"""Global tests configuration and fixtures"""

import asyncio

import pytest

from src.mongo import DataClient
from src.mongo.mongo_conn import MongoConnector
from tests.test_utils import (
    ATTEMPT_WAIT,
    ATTEMPTS,
    DB_NAME,
    DELAY,
    INITIAL_URL,
    MONGO_HOST,
    MONGO_PORT,
)


@pytest.fixture(scope="session")
def generate_env_variables(monkeypatch: pytest.MonkeyPatch):
    """Set up env variables for our tests"""
    monkeypatch.setenv("INITIAL_URL", INITIAL_URL)
    monkeypatch.setenv("ATTEMPTS", ATTEMPTS)
    monkeypatch.setenv("ATTEMPT_WAIT", ATTEMPT_WAIT)
    monkeypatch.setenv("DELAY", DELAY)
    monkeypatch.setenv("MONGO_HOST", MONGO_HOST)
    monkeypatch.setenv("MONGO_PORT", MONGO_PORT)


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
