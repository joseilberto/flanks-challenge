"""Test the CNMVCrawler methods"""

from datetime import datetime

import pytest

from src.mongo import DataClient
from tests.test_utils import (
    ENTRY_PAGE1,
    ENTRY_PAGE1_UPDATE1,
    ENTRY_PAGE1_UPDATE2,
    ENTRY_PAGE2,
)


@pytest.mark.asyncio
async def test_set_data(data_client: DataClient) -> None:
    """Test the set_data method inside the crawler"""
    # First, we delete all docs
    await data_client.delete_docs()

    # Test invalid result type
    assert await data_client.set_data("") is False

    # Insert first document
    assert await data_client.set_data(ENTRY_PAGE1) is True

    today = datetime.now().strftime("%Y-%m-%d")

    # Check if the first document was correctly inserted
    query = {
        "nombre": ENTRY_PAGE1.nombre,
        "numero_registro": ENTRY_PAGE1.numero_registro,
        "fecha_registro": ENTRY_PAGE1.fecha_registro,
        "isin": ENTRY_PAGE1.isin,
    }
    document = await data_client.find_entry(query)
    document.pop("write_date")
    expected = ENTRY_PAGE1._asdict()
    expected["last_update"] = today
    expected["updates"] = {}
    assert document == expected

    # Insert second document
    assert await data_client.set_data(ENTRY_PAGE2) is True
    query = {
        "nombre": ENTRY_PAGE2.nombre,
        "numero_registro": ENTRY_PAGE2.numero_registro,
        "fecha_registro": ENTRY_PAGE2.fecha_registro,
        "isin": ENTRY_PAGE2.isin,
    }

    # Check if the second document was correctly inserted
    document = await data_client.find_entry(query)
    document.pop("write_date")
    expected = ENTRY_PAGE2._asdict()
    expected["last_update"] = today
    expected["updates"] = {}
    assert document == expected

    # Insert first document update
    assert await data_client.set_data(ENTRY_PAGE1_UPDATE1) is True

    # Check if the inserted update creates the correct entry
    query = {
        "nombre": ENTRY_PAGE1.nombre,
        "numero_registro": ENTRY_PAGE1.numero_registro,
        "fecha_registro": ENTRY_PAGE1.fecha_registro,
        "isin": ENTRY_PAGE1.isin,
    }
    document = await data_client.find_entry(query)
    document.pop("write_date")
    expected = ENTRY_PAGE1_UPDATE1._asdict()
    expected["last_update"] = today
    expected["updates"] = {"domicilio": {today: ENTRY_PAGE1.domicilio}}
    assert document == expected

    # Insert first document second update
    assert await data_client.set_data(ENTRY_PAGE1_UPDATE2) is True

    # Check if the second update creates the correct entry
    query = {
        "nombre": ENTRY_PAGE1.nombre,
        "numero_registro": ENTRY_PAGE1.numero_registro,
        "fecha_registro": ENTRY_PAGE1.fecha_registro,
        "isin": ENTRY_PAGE1.isin,
    }
    document = await data_client.find_entry(query)
    document.pop("write_date")
    expected = ENTRY_PAGE1_UPDATE2._asdict()
    expected["last_update"] = today
    expected["updates"] = {
        "domicilio": {today: ENTRY_PAGE1_UPDATE1.domicilio},
        "capital_inicial": {today: ENTRY_PAGE1.capital_inicial},
        "capital_maximo": {today: ENTRY_PAGE1.capital_maximo},
        "fecha_ultimo_folleto": {
            today: ENTRY_PAGE1_UPDATE1.fecha_ultimo_folleto
        },
    }
    assert document == expected
