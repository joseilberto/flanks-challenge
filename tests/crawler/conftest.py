"""CNMV tests configuration and fixtures"""

import os

import pytest

from src.crawler import MAPPING, CNMVCrawler, DataPipeline
from src.mongo import DataClient
from tests.test_utils import (
    ATTEMPT_WAIT,
    ATTEMPTS,
    DELAY,
    INITIAL_URL,
    MONGO_HOST,
    MONGO_PORT,
)


@pytest.fixture
def data_pipeline() -> DataPipeline:
    """Creating DataPipeline fixture"""
    return DataPipeline(MAPPING)


# pylint: disable=redefined-outer-name
@pytest.fixture
def cnmv_crawler(
    data_client: DataClient, data_pipeline: DataPipeline
) -> CNMVCrawler:
    """Creating CNMVCrawler fixture"""
    return CNMVCrawler(
        mongo_client=data_client, data_pipeline=data_pipeline, url=INITIAL_URL
    )


def generate_env_variables():
    """Set up env variables for our tests"""
    os.environ["INITIAL_URL"] = INITIAL_URL
    os.environ["ATTEMPTS"] = ATTEMPTS
    os.environ["ATTEMPT_WAIT"] = ATTEMPT_WAIT
    os.environ["DELAY"] = DELAY
    os.environ["MONGO_HOST"] = MONGO_HOST
    os.environ["MONGO_PORT"] = MONGO_PORT
