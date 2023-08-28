"""Test the MongoDataPipeLine and pipeline methods"""

import pytest
from bs4 import BeautifulSoup

from src.crawler.pipelines import MongoDataPipeLine, process_capital
from tests.test_utils import ENTRY_PAGE1, SAMPLE_FILES


def test_get_next_page() -> None:
    """Test the process_capital method"""
    assert process_capital("18,045,092.98") == 18045092.98
    assert process_capital("18.045.092,98") == 18045092.98


@pytest.mark.asyncio
async def test_extract_and_transform(data_pipeline: MongoDataPipeLine) -> None:
    """Test the extract_and_transform method inside the crawler"""
    url = "https://localhost/test_url/process_page1"
    # Test an empty html page
    soup = BeautifulSoup(SAMPLE_FILES["empty_entry1"], "html.parser")
    result = await data_pipeline.extract_and_transform(url, soup)
    assert result is None

    # Test a working html page
    soup = BeautifulSoup(SAMPLE_FILES["success_entry1"], "html.parser")
    result = await data_pipeline.extract_and_transform(url, soup)
    assert result == ENTRY_PAGE1
