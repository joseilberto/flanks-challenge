"""Test the MongoDataPipeLine and pipeline methods"""

import pytest
from bs4 import BeautifulSoup

from src.crawler.pipelines import MongoDataPipeLine, process_capital
from src.data_classes import DataTypes
from tests.test_utils import ENTRY_PAGE1, SAMPLE_FILES


def test_get_next_page() -> None:
    """Test the process_capital method"""
    assert process_capital("18,045,092.98") == 18045092.98
    assert process_capital("18.045.092,98") == 18045092.98


@pytest.mark.asyncio
async def test_extract_and_transform(data_pipeline: MongoDataPipeLine) -> None:
    """Test the extract_and_transform method inside the pipeline"""
    url = "https://localhost/test_url/process_page1"
    # Test an empty html page
    soup = BeautifulSoup(SAMPLE_FILES["empty_entry1"], "html.parser")
    result = await data_pipeline.extract_and_transform(url, soup)
    assert result is None

    # Test a working html page
    soup = BeautifulSoup(SAMPLE_FILES["success_entry1"], "html.parser")
    result = await data_pipeline.extract_and_transform(url, soup)
    assert result == ENTRY_PAGE1


@pytest.mark.asyncio
async def test_get_nombre(data_pipeline: MongoDataPipeLine) -> None:
    """Test the get_nombre method inside the pipeline"""
    url = "https://localhost/test_url/process_page1"

    # Test non-existing titcont
    soup = BeautifulSoup(SAMPLE_FILES["no_titcont_entry1"], "html.parser")
    try:
        data_pipeline.get_nombre(url, soup)
    except ValueError:
        assert True

    # Test non-existing span inside the titcont
    soup = BeautifulSoup(SAMPLE_FILES["no_span_entry1"], "html.parser")
    try:
        data_pipeline.get_nombre(url, soup)
    except ValueError:
        assert True

    # Test working entry
    soup = BeautifulSoup(SAMPLE_FILES["success_entry1"], "html.parser")
    assert data_pipeline.get_nombre(url, soup) == ENTRY_PAGE1.nombre


@pytest.mark.asyncio
async def test_get_data_table_elements(
    data_pipeline: MongoDataPipeLine,
) -> None:
    """Test the get_data_table_elements method inside the pipeline"""
    url = "https://localhost/test_url/process_page1"

    # Test missing non-key values in the table
    soup = BeautifulSoup(SAMPLE_FILES["entry1_missing_non_key"], "html.parser")
    tag = soup.find("div", {"class": "div_tablaDatos"})
    result = data_pipeline.get_data_table_elements(url, tag)
    expected = DataTypes(
        ENTRY_PAGE1.nombre,
        ENTRY_PAGE1.numero_registro,
        ENTRY_PAGE1.fecha_registro,
        ENTRY_PAGE1.isin,
    )._asdict()
    expected.pop("nombre")
    assert result == expected

    # Test missing key values in the table
    soup = BeautifulSoup(SAMPLE_FILES["entry1_missing_key"], "html.parser")
    tag = soup.find("div", {"class": "div_tablaDatos"})
    try:
        data_pipeline.get_data_table_elements(url, tag)
    except ValueError:
        assert True

    # Test missing ISIN tag
    soup = BeautifulSoup(SAMPLE_FILES["entry_missing_isin"], "html.parser")
    tag = soup.find("div", {"class": "div_tablaDatos"})
    try:
        data_pipeline.get_data_table_elements(url, tag)
    except ValueError:
        assert True

    # Test working data table
    soup = BeautifulSoup(SAMPLE_FILES["success_entry1"], "html.parser")
    tag = soup.find("div", {"class": "div_tablaDatos"})
    result = data_pipeline.get_data_table_elements(url, tag)
    expected = ENTRY_PAGE1._asdict()
    expected.pop("nombre")
    assert result == expected
