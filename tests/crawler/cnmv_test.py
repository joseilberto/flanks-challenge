"""Test the CNMVCrawler methods"""

from contextlib import asynccontextmanager
from typing import List

import aiohttp
import pytest
from bs4 import BeautifulSoup

from src.crawler.cnmv import CNMVCrawler
from src.data_classes import ContentTypes, DataTypes
from tests.test_utils import (
    ATTEMPTS,
    ENTRY_PAGE1,
    ENTRY_PAGE2,
    INITIAL_URL,
    SAMPLE_FILES,
)


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
async def mock_entry_page_request(*args, **kwargs):
    # pylint: disable=unused-argument
    """Mock a successful request to a page containing an entry"""
    yield MockResponse(SAMPLE_FILES["success_entry1"])


@asynccontextmanager
async def mock_entry_page_request_fail(*args, **kwargs):
    # pylint: disable=unused-argument
    """Mock a failed request to a page containing an entry"""
    yield MockResponse(SAMPLE_FILES["success_entry1"], status=404)


@asynccontextmanager
async def mock_listing_request_fail(*args, **kwargs):
    # pylint: disable=unused-argument
    """Mock a failed request to the listing page with status != 200"""
    yield MockResponse(SAMPLE_FILES["success_list_page"], status=404)


@asynccontextmanager
async def mock_listing_request_empty(*args, **kwargs):
    # pylint: disable=unused-argument
    """Mock a successful request to an empty listing page"""
    yield MockResponse(SAMPLE_FILES["empty_list_page"], status=404)


@asynccontextmanager
async def mock_listing_request(*args, **kwargs):
    # pylint: disable=unused-argument
    """Mock a successful request to the listing page"""
    yield MockResponse(SAMPLE_FILES["success_list_page"])


async def mock_get_list_content(*args, **kwargs):
    # pylint: disable=unused-argument
    """Mock the behaviour of the _get_list_content page"""
    return ContentTypes(
        "Next Page",
        [
            "https://localhost/test_url/process_page1",
            "https://localhost/test_url/process_page2",
        ],
    )


async def mock_transformed_results(*args, **kwargs):
    # pylint: disable=unused-argument
    """Mock the behaviour of the _get_list_content page"""
    return [ENTRY_PAGE1, ENTRY_PAGE1]


async def mock_crawl_and_transform(*args, **kwargs):
    # pylint: disable=unused-argument
    """Mock the behaviour of the crawl_and_transform method"""
    return [ENTRY_PAGE1, ENTRY_PAGE2], ContentTypes()


def test_get_next_page(cnmv_crawler: CNMVCrawler) -> None:
    """Test the _get_next_page method"""
    # Test a listing page without the maincontent section
    soup = BeautifulSoup(SAMPLE_FILES["empty_list_page"], "html.parser")
    next_page = cnmv_crawler._get_next_page(soup)
    assert next_page == ""

    # Test a listing page without the pagination ul
    soup = BeautifulSoup(SAMPLE_FILES["no_pagination_list_page"], "html.parser")
    next_page = cnmv_crawler._get_next_page(soup)
    assert next_page == ""

    # Test a listing page without the current page
    soup = BeautifulSoup(
        SAMPLE_FILES["no_current_page_list_page"], "html.parser"
    )
    next_page = cnmv_crawler._get_next_page(soup)
    assert next_page == ""

    # Test a listing page without the next page a element
    soup = BeautifulSoup(SAMPLE_FILES["no_next_page_list_page"], "html.parser")
    next_page = cnmv_crawler._get_next_page(soup)
    assert next_page == ""

    # Test a successful listing page for the next page
    soup = BeautifulSoup(SAMPLE_FILES["success_list_page"], "html.parser")
    next_page = cnmv_crawler._get_next_page(soup)
    assert next_page == "Next Page"


def test_get_all_urls(cnmv_crawler: CNMVCrawler) -> None:
    """Test the _get_next_page method"""
    # Test a listing page without the maincontent section
    soup = BeautifulSoup(SAMPLE_FILES["empty_list_page"], "html.parser")
    urls = cnmv_crawler._get_all_urls(soup)
    assert urls == []

    # Test a listing page without the url list
    soup = BeautifulSoup(SAMPLE_FILES["no_urls_list_list_page"], "html.parser")
    urls = cnmv_crawler._get_all_urls(soup)
    assert urls == []

    # Test a listing page without urls in the urls list
    soup = BeautifulSoup(
        SAMPLE_FILES["empty_urls_list_list_page"], "html.parser"
    )
    urls = cnmv_crawler._get_all_urls(soup)
    assert urls == []


def test_validate_next_page_url(cnmv_crawler: CNMVCrawler) -> None:
    """Test the _validate_next_page_url method"""
    # Check if it is the last page tag
    soup = BeautifulSoup("<b></b>", "html.parser")
    tag = soup.new_tag("a", title="Ir a la última página")
    next_page = cnmv_crawler._validate_next_page_url(tag)
    assert next_page == ""

    # Check for next page without a link
    soup = BeautifulSoup("<b></b>", "html.parser")
    tag = soup.new_tag("a", title="1")
    next_page = cnmv_crawler._validate_next_page_url(tag)
    assert next_page == ""


def test_validate_url_elements(cnmv_crawler: CNMVCrawler) -> None:
    """Test the _validate_url_elements method"""
    # Check if href is not present in a tag
    soup = BeautifulSoup("<b></b>", "html.parser")
    tag = soup.new_tag("a", title="1")
    urls = cnmv_crawler._validate_url_elements([tag])
    assert urls == []


@pytest.mark.asyncio
async def test_get_list_content(
    monkeypatch: pytest.MonkeyPatch, cnmv_crawler: CNMVCrawler
) -> None:
    """Test the _get_list_content method inside the crawler"""
    monkeypatch.setenv("ATTEMPT_WAIT", "0")
    async with aiohttp.ClientSession() as session:
        # Mock request with response.status != 200
        monkeypatch.setattr(session, "get", mock_listing_request_fail)
        content: ContentTypes = await cnmv_crawler._get_list_content(
            INITIAL_URL, session, attempts=int(ATTEMPTS)
        )
        assert content.next_page == ""
        assert content.urls == []

        # Mock a request with empty html
        monkeypatch.setattr(session, "get", mock_listing_request_empty)
        content: ContentTypes = await cnmv_crawler._get_list_content(
            INITIAL_URL, session, attempts=int(ATTEMPTS)
        )
        assert content.next_page == ""
        assert content.urls == []

        # Mock a successful request with next page and urls
        monkeypatch.setattr(session, "get", mock_listing_request)
        content: ContentTypes = await cnmv_crawler._get_list_content(
            INITIAL_URL, session, attempts=int(ATTEMPTS)
        )
        assert content.next_page == "Next Page"
        assert content.urls == [
            "https://localhost/test_url/process_page1",
            "https://localhost/test_url/process_page2",
        ]


@pytest.mark.asyncio
async def test_get_transformed_results(
    monkeypatch: pytest.MonkeyPatch, cnmv_crawler: CNMVCrawler
) -> None:
    """Test the _get_transformed_results method inside the crawler"""
    monkeypatch.setenv("ATTEMPT_WAIT", "0")
    async with aiohttp.ClientSession() as session:
        urls = [
            "https://localhost/test_url/process_page1",
            "https://localhost/test_url/process_page2",
        ]
        # Getting a failed response from the _get_transformed_results method
        monkeypatch.setattr(session, "get", mock_entry_page_request_fail)
        results: List[DataTypes] = await cnmv_crawler._get_transformed_results(
            urls, session
        )
        assert len(results) == 0

        # Getting a successful response from the _get_transformed_results method
        monkeypatch.setattr(session, "get", mock_entry_page_request)
        results: List[DataTypes] = await cnmv_crawler._get_transformed_results(
            urls, session
        )
        assert len(results) == 2
        assert results[0] == results[1] == ENTRY_PAGE1


@pytest.mark.asyncio
async def test_crawl_and_transform(
    monkeypatch: pytest.MonkeyPatch, cnmv_crawler: CNMVCrawler
) -> None:
    """Test the crawl_and_transform method inside the crawler"""
    async with aiohttp.ClientSession() as session:
        # Mock a successful request with next page and urls
        monkeypatch.setattr(
            cnmv_crawler, "_get_list_content", mock_get_list_content
        )
        monkeypatch.setattr(
            cnmv_crawler, "_get_transformed_results", mock_transformed_results
        )
        transformed, content = await cnmv_crawler.crawl_and_transform(
            INITIAL_URL, session
        )

        assert transformed == await mock_transformed_results()
        assert content == await mock_get_list_content()


@pytest.mark.asyncio
async def test_save_results(cnmv_crawler: CNMVCrawler) -> None:
    """Test the save_results method inside the crawler"""
    saved = await cnmv_crawler.save_results([ENTRY_PAGE1, ENTRY_PAGE2])
    assert saved is True


@pytest.mark.asyncio
async def test_crawl_and_save(
    monkeypatch: pytest.MonkeyPatch, cnmv_crawler: CNMVCrawler
) -> None:
    """Test the crawl_and_save method inside the crawler"""
    monkeypatch.setattr(
        cnmv_crawler, "crawl_and_transform", mock_crawl_and_transform
    )
    await cnmv_crawler.crawl_and_save()
