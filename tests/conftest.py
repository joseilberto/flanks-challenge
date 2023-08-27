"""Global tests configuration and fixtures"""

import os

import pytest

from src.mongo import DataClient
from src.mongo.mongo_conn import MongoConnector

from .test_utils import (
    ATTEMPT_WAIT,
    ATTEMPTS,
    DB_NAME,
    DELAY,
    INITIAL_URL,
    MONGO_HOST,
    MONGO_PORT,
)


@pytest.fixture(scope="session")
def mongo_connector() -> MongoConnector:
    """Make a connector fixture"""
    return MongoConnector(MONGO_HOST, MONGO_PORT)


# pylint: disable=redefined-outer-name
@pytest.fixture(scope="session")
def data_client(mongo_connector: MongoConnector) -> DataClient:
    """Make a DataClient fixture"""
    return DataClient(db_name=DB_NAME, connector=mongo_connector)


def generate_env_variables():
    """Set up env variables for our tests"""
    os.environ["INITIAL_URL"] = INITIAL_URL
    os.environ["ATTEMPTS"] = ATTEMPTS
    os.environ["ATTEMPT_WAIT"] = ATTEMPT_WAIT
    os.environ["DELAY"] = DELAY
    os.environ["MONGO_HOST"] = MONGO_HOST
    os.environ["MONGO_PORT"] = MONGO_PORT
