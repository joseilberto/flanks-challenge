"""
CNMV crawler class with all the methods we need to crawl the CNMV listing page
"""

import asyncio
import logging
from typing import List, NamedTuple, Optional, Tuple, Union
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from config import INITIAL_URL
from mongo import DataClient

from .pipelines import DataTypes, MongoDataPipeLine


class ContentTypes(NamedTuple):
    """
    Named tuple for the content of each pagination
    """

    next_page: str = ""
    urls: List[str] = []


class CNMVCrawler:
    """CNMV crawler class"""

    def __init__(
        self,
        mongo_client: DataClient,
        data_pipeline: MongoDataPipeLine,
        url: Optional[str] = INITIAL_URL,
    ) -> None:
        """Initialise the class variables"""
        self.url = url
        self.mongo_client = mongo_client
        self.data_pipeline = data_pipeline

        self.log = logging.getLogger(__name__)

    async def _get_list_content(
        self,
        url: str,
        session: aiohttp.ClientSession,
        attempts: int = 3,
    ) -> ContentTypes:
        """
        Getting the pagination and list of needed urls that are going to be
        crawled all the elements.
        """
        async with session.get(url) as response:
            attempt = 1
            while attempt < attempts:
                # Check the response status first
                if response.status != 200:
                    msg = f"Failed request to {url} with code {response.status}"
                    self.log.warning(msg)
                    attempt += 1
                    await asyncio.sleep(2)
                    continue

                # Get the html content and create a soup parser
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                # Extract the next page and all urls
                next_page = self._get_next_page(soup)
                urls = self._get_all_urls(soup)
                if next_page is None and not urls:
                    return ContentTypes()
                if next_page is not None and not urls:
                    return ContentTypes(next_page=next_page)
                if next_page is not None and urls:
                    break
        return ContentTypes(next_page, urls)

    def _get_next_page(self, soup: BeautifulSoup) -> str:
        """
        Get the next page from the current soup
        """
        # Get the content table
        content_table = soup.find("section", {"id": "maincontent"})
        if not isinstance(content_table, Tag):
            msg = (
                "Couldn't find Tag for content table, found"
                f" {type(content_table)} instead. Ignoring this page."
            )
            self.log.error(msg)
            return ""

        # Get the pagination element
        pagination = content_table.find("ul", {"class": "pagination"})
        if not isinstance(pagination, Tag):
            msg = (
                "Couldn't find Tag for pagination, found"
                f" {type(pagination)} instead. Ignoring this page."
            )
            self.log.error(msg)
            return ""

        # Get the current page
        current_page = pagination.find("span", {"class": "active"})
        if not isinstance(current_page, Tag) or current_page.parent is None:
            msg = (
                "Couldn't find Tag for current page value or current page"
                f" parent is None. found {type(current_page)} instead. Ignoring"
                " this page."
            )
            self.log.error(msg)
            return ""

        # Find the next element and validate the url on it
        next_page = current_page.parent.findNext("a")
        if next_page is not None:
            return self._validate_next_page_url(next_page)

        return ""

    def _get_all_urls(self, soup: BeautifulSoup) -> List[str]:
        """
        Get all the urls to be crawled in the page
        """
        # Get the content table
        content_table = soup.find("section", {"id": "maincontent"})
        if not isinstance(content_table, Tag):
            msg = (
                "Couldn't find Tag for content table, found"
                f" {type(content_table)} instead. Ignoring this page."
            )
            self.log.error(msg)
            return []

        # Get the element list
        element_list = content_table.find(
            "ul", {"id": "listaElementosPrimernivel"}
        )
        if not isinstance(element_list, Tag):
            msg = (
                "Couldn't find Tag for element list, found"
                f" {type(element_list)} instead. Ignoring this page."
            )
            self.log.error(msg)
            return []
        # Get the element urls
        url_elements = element_list.select(
            "a[id*=ctl00_ContentPrincipal_wucRelacionRegistros]"
        )
        if not url_elements:
            msg = "Couldn't find urls"
            self.log.error(msg)
            return []
        return self._validate_url_elements(url_elements)

    def _validate_next_page_url(
        self, element: Union[Tag, NavigableString]
    ) -> str:
        """
        Validate the url for the next page.
        We ignore if the title indicates that we reached the last page.
        """
        # Checks if we reached the last page
        if isinstance(element, Tag):
            title: Optional[Union[str, List[str]]] = element.get("title")
            if title is not None and "Ir a la última página" in title:
                self.log.info("Reached the last page")
                return ""
            if title is None:
                self.log.error("Next page without title")
                raise ValueError("Next page without title")
        else:
            msg = f"Not able to validate element of type {type(element)}"
            self.log.error(msg)
            raise NotImplementedError(msg)

        # Validate the url element
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
            return ""

    def _validate_url_elements(self, url_elements: List[Tag]) -> List[str]:
        """Validate each url element and return all the valid ones"""
        # Create a list of valid urls to be crawled
        validated: List[str] = []
        for element in url_elements:
            elem_url = element.get("href")
            if not isinstance(elem_url, str):
                msg = f"Expected str, got {type(elem_url)} for the URL element"
                self.log.warning(msg)
                continue
            url = urljoin(self.url, elem_url)  # type: ignore
            if isinstance(url, str):
                validated.append(url)
        return validated

    async def _get_transformed_results(
        self, urls: List[str]
    ) -> List[DataTypes]:
        # pylint: disable=unused-argument
        """
        Get the results of each url and transform them using the data pipeline
        """
        return []

    async def crawl_and_transform(
        self, url: str, session: aiohttp.ClientSession
    ) -> Tuple[List[DataTypes], ContentTypes]:
        """
        Crawl a listing page in the pagination extracting and transforming the
        data
        """
        content = await self._get_list_content(url, session)
        transformed = await self._get_transformed_results(content.urls)
        return transformed, content

    async def crawl_and_save(self) -> None:
        """
        Crawl and save all the results in the database
        """
        async with aiohttp.ClientSession() as session:
            next_page = INITIAL_URL
            while True:
                results, content = await self.crawl_and_transform(
                    next_page, session
                )
                await self.save_results(results)
                next_page = content.next_page
                if not next_page:
                    break

    async def save_results(self, results: List[DataTypes]) -> bool:
        """
        Save the results using the mongo client
        """
        coros = [self.mongo_client.set_data(result) for result in results]
        return all(await asyncio.gather(*coros))
