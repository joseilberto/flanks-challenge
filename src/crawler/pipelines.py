"""
Pipelines to transform the raw data found into mongoDB types
"""

import locale
import logging
from datetime import datetime
from typing import Callable, Dict, Optional, Union

from bs4 import BeautifulSoup
from bs4.element import Tag

from data_classes import DataTypes

THS = {
    "numero_registro": "Nº Registro oficial",
    "fecha_registro": "Fecha registro oficial",
    "isin": "ISIN",
    "domicilio": "Domicilio",
    "capital_inicial": "Capital social inicial",
    "capital_maximo": "Capital máximo estatutario",
    "fecha_ultimo_folleto": "Fecha último folleto",
}


def process_capital(capital: str) -> float:
    """
    Try different locales to process the capital field
    """
    try:
        locale.setlocale(locale.LC_NUMERIC, "en_US.utf8")
        return locale.atof(capital)
    except ValueError:
        locale.setlocale(locale.LC_NUMERIC, "es_ES.utf8")
        return locale.atof(capital)


MAPPING: Dict[str, Callable[[str], Union[str, float]]] = {
    "nombre": str,
    "numero_registro": str,
    "fecha_registro": lambda x: datetime.strptime(x, r"%d/%m/%Y").strftime(
        "%Y-%m-%d"
    ),
    "isin": str,
    "domicilio": str,
    "capital_inicial": process_capital,
    "capital_maximo": process_capital,
    "fecha_ultimo_folleto": lambda x: datetime.strptime(
        x, r"%d/%m/%Y"
    ).strftime("%Y-%m-%d"),
}


class MongoDataPipeLine:
    """Data pipeline to transform the raw data into mongo types"""

    def __init__(
        self,
        mapping_functions: Dict[str, Callable[[str], Union[str, float]]],
    ) -> None:
        """Initialising the variables in our pipeline"""
        self.mapping_functions = mapping_functions

        self.log = logging.getLogger(__name__)

    async def extract_and_transform(
        self, url: str, soup: BeautifulSoup
    ) -> Optional[DataTypes]:
        """
        Extract and transform the data from the soup element
        """
        # Get the nombre SICAV
        self.log.debug("Getting nombre in %s", url)
        result = {"nombre": self.get_nombre(url, soup)}
        # Get the data table
        data_table = soup.find("div", {"class": "div_tablaDatos"})
        if not isinstance(data_table, Tag):
            msg = (
                "Couldn't find Tag for data table, found"
                f" {type(data_table)} instead. Ignoring this page."
            )
            self.log.error(msg)
            return None

        # Get the data for all entries in the data table
        self.log.debug(
            "Getting the remaining fields from the data table in %s", url
        )
        result.update(self.get_data_table_elements(url, data_table))  # type: ignore
        return DataTypes(**result)  # type: ignore

    def get_nombre(self, url: str, soup: BeautifulSoup) -> str:
        """
        Get the nombre SICAV which is in a separate element regarding the
        rest of the fields
        """
        # Get the nombre element
        nombre_element = soup.find("p", {"class": "titcont"})
        if not isinstance(nombre_element, Tag):
            msg = (
                f"Couldn't find Tag for nombre element in {url}, found"
                f" {type(nombre_element)} instead. Ignoring this page."
            )
            self.log.error(msg)
            raise ValueError(msg)
        # Get the span with the text containing nombre
        nombre = nombre_element.select_one("span")
        if not isinstance(nombre, Tag):
            msg = (
                f"Couldn't find Tag for nombre in {url}, found"
                f" {type(nombre)} instead. Ignoring this page."
            )
            self.log.error(msg)
            raise ValueError(msg)

        return nombre.text

    def get_data_table_elements(
        self, url: str, data_table: Tag
    ) -> Dict[str, Optional[Union[str, float]]]:
        """Get all elements in the data table"""
        result: Dict[str, Optional[Union[str, float]]] = {}
        for field, th_class in THS.items():
            # Get the current element in the table
            element = data_table.find("td", {"data-th": th_class})
            if not isinstance(element, Tag):
                msg = (
                    f"Couldn't find Tag for {field} for {url}, found"
                    f" {type(element)} instead."
                )
                if field not in [
                    "nombre",
                    "numero_registro",
                    "fecha_registro",
                    "isin",
                ]:
                    msg += "Using None value instead."
                    self.log.warning(msg)
                    result[field] = None
                else:
                    msg += "Key field cannot be None"
                    self.log.error(msg)
                    raise ValueError(msg)

            # ISIN has a different structure, we check it first
            if field == "isin" and isinstance(element, Tag):
                isin = element.select_one("a")
                if not isinstance(isin, Tag):
                    msg = (
                        "Couldn't find Tag for ISIN for {url}, found"
                        f" {type(isin)} instead. Ignoring this page."
                    )
                    self.log.error(msg)
                    raise ValueError(msg)
                result[field] = self.mapping_functions[field](isin.text)
                continue
            # Process elements
            if element is not None:
                result[field] = self.mapping_functions[field](element.text)
        return result
