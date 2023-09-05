"""A listing handler able to list data using different keys"""

import logging
from typing import Dict, List, Optional, Tuple, Union

from mongo import DataClient
from mongo.mongo_data import DocumentType


class SearchHandler:
    # pylint: disable=too-few-public-methods
    """A handler to list elements according to the search key provided"""

    def __init__(self, mongo_client: DataClient) -> None:
        """
        Initialise the class
        """
        self.log = logging.getLogger(__name__)
        self.log.info("Initialising the SearchHandler")
        self.mongo_client = mongo_client

    async def get(
        self,
        isin: Optional[Union[str, List[str]]] = None,
        numero_registro: Optional[Union[str, List[str]]] = None,
        nombre: Optional[str] = None,
        fecha_registro: Optional[Union[str, List[str]]] = None,
    ) -> List[DocumentType]:
        """Get method for searching an entry with given search parameters"""
        query: Dict[str, Union[str, List[str]]] = {}
        query_elements: List[Tuple[str, Optional[Union[str, List[str]]]]] = [
            ("isin", isin),
            ("numero_registro", numero_registro),
            ("nombre", nombre),
            ("fecha_registro", fecha_registro),
        ]
        for key, value in query_elements:
            if value is not None:
                query[key] = value
        if not query:
            self.log.error("The request received has no search parameters.")
            return []
        msg = f"Searching in the database using the parameters: {query}"
        self.log.debug(msg)
        return await self.mongo_client.find_entries(query)
