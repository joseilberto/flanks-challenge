"""CNMV tests configuration and fixtures"""

import pytest

from src.crawler import MAPPING, CNMVCrawler, DataPipeline
from src.mongo import DataClient
from tests.test_utils import INITIAL_URL


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
