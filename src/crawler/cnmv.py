"""
CNMV crawler class with all the methods we need to crawl the CNMV listing page
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Union
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from config import INITIAL_URL
from mongo import DataClient

from .pipelines import MongoDataPipeLine


class CNMVCrawler:
    """CNMV crawler class"""

    # pylint: disable=too-few-public-methods,unused-argument

    def __init__(
        self,
        url: str = INITIAL_URL,
        mongo_client: Optional[DataClient] = None,
        data_pipeline: Optional[MongoDataPipeLine] = None,
    ) -> None:
        """Initialise the class variables"""
        self.url = url
        self.mongo_client = mongo_client
        self.data_pipeline = data_pipeline

        self.log = logging.getLogger(__name__)

    async def _get_list_content(
        self, url: str, session: aiohttp.ClientSession, to_database: bool
    ) -> Optional[str]:
        """
        Getting the pagination and list of needed urls that are going to be
        crawled all the elements.
        """
        async with session.get(url) as response:
            # Check the response status first
            if response.status != 200:
                msg = f"Failed request to {url} with code {response.status}"
                self.log.error(msg)
                return None

            # Get the html content and create a soup parser
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            # Extract the next page and all urls
            next_page = self._get_next_page(soup)

        return next_page

    def _get_next_page(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Get the next page from the current soup
        """
        content_table = soup.find("section", {"id": "maincontent"})
        if content_table is not None and isinstance(content_table, Tag):
            pagination = content_table.find("ul", {"class": "pagination"})
            if pagination is not None and isinstance(pagination, Tag):
                current_page = pagination.find("span", {"class": "active"})
                if (
                    current_page is not None
                    and current_page.parent is not None
                    and isinstance(current_page, Tag)
                ):
                    next_page = current_page.parent.findNext("a")
                    if next_page is not None:
                        return self._validate_url(next_page)
        return None

    def _validate_url(
        self, element: Union[Tag, NavigableString]
    ) -> Optional[str]:
        """
        Validate the url for the next page.
        We ignore if the title indicates that we reached the last page.
        """
        # Checks if we reached the last page
        if isinstance(element, Tag):
            title: Optional[Union[str, List[str]]] = element.get("title")
            if title is not None and "Ir a la última página" in title:
                self.log.info("Reached the last page")
                return None
            if title is None:
                self.log.error("Next page without title")
                raise ValueError("Next page without title")
        else:
            msg = f"Not able to validate element of type {type(element)}"
            self.log.error(msg)
            raise NotImplementedError(msg)

        try:
            element_url = element.get("href")
            if isinstance(element_url, str):
                url = urlparse(element_url)
                return url.geturl()
            msg = f"Expected str for url, got {type(element_url)}"
            self.log.error(msg)
            raise NotImplementedError(msg)

        # pylint: disable=broad-exception-caught
        except Exception as err:
            msg = (
                f"Could not parse URL: {element.get('href')} with error: {err}"
            )
            self.log.error(msg)
            return None

    async def crawl(
        self, to_database: bool = True
    ) -> List[Dict[str, Union[str, datetime, float, int]]]:
        """
        Crawl all the pages available in the pagination extracting and saving
        the collected data in MONGO
        """
        async with aiohttp.ClientSession() as session:
            await self._get_list_content(INITIAL_URL, session, to_database)
        return []
