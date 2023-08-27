"""Test the CNMVCrawler methods"""

from contextlib import asynccontextmanager

import aiohttp
import pytest
from bs4 import BeautifulSoup

from src.crawler.cnmv import CNMVCrawler, ContentTypes
from tests.test_utils import ATTEMPTS, INITIAL_URL, SAMPLE_LISTING

# pylint: disable=protected-access


class MockResponse:
    # pylint: disable=too-few-public-methods
    """MockResponse class to mock a response from a page"""

    def __init__(self, content: str, status: int = 200) -> None:
        """Initialise the relevant response parameters"""
        self.content = content
        self.status = status

    async def text(self):
        """
        Return the content
        """
        return self.content


@asynccontextmanager
async def mock_listing_request(*args, **kwargs):
    # pylint: disable=unused-argument
    """Mock a successful request to the listing page"""
    yield MockResponse(SAMPLE_LISTING)


@pytest.mark.asyncio
async def test_get_next_page(cnmv_crawler: CNMVCrawler) -> None:
    """Test the _get_next_page method"""
    soup = BeautifulSoup(SAMPLE_LISTING, "html.parser")
    next_page = cnmv_crawler._get_next_page(soup)
    assert next_page == "Next Page"


@pytest.mark.asyncio
async def test_get_list_content(
    monkeypatch: pytest.MonkeyPatch, cnmv_crawler: CNMVCrawler
) -> None:
    """Test the _get_list_content method inside the crawler"""
    async with aiohttp.ClientSession() as session:
        monkeypatch.setattr(session, "get", mock_listing_request)
        content: ContentTypes = await cnmv_crawler._get_list_content(
            INITIAL_URL, session, attempts=int(ATTEMPTS)
        )
        assert content.next_page == "Next Page"
        assert content.urls == [
            "https://localhost/test_url/process_page1",
            "https://localhost/test_url/process_page2",
        ]
