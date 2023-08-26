"""
Pipelines to transform the raw data found into mongoDB types
"""

import logging
from datetime import datetime
from typing import List, NamedTuple

from bs4 import BeautifulSoup


class DataTypes(NamedTuple):
    """TypeDict for the MongoClientBase params"""

    nombre: str
    numero_registro: str
    fecha_registro: datetime
    domicilio: str
    capital_inicial: float
    capital_maximo: float
    isin: str
    fecha_ultimo_folleto: datetime


class MongoDataPipeLine:
    # pylint: disable=too-few-public-methods,unused-argument
    """Data pipeline to transform the raw data into mongo types"""

    def __init__(self, fields: DataTypes) -> None:
        """Initialising the variables in our pipeline"""
        self.fields = fields._asdict

        self.log = logging.getLogger(__name__)

    async def extract_and_transform(
        self, soup: BeautifulSoup
    ) -> List[DataTypes]:
        """
        Extract and transform the data from the soup element
        """
        return []
