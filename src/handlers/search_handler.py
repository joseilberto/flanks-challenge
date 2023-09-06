"""A listing handler able to list data using different keys"""

import logging
from typing import Dict, List, Optional, Tuple, Union

from data_classes import DocumentType, QueryDict
from mongo import DataClient


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

    def _format_query(self, query: QueryDict, mode: str = "$gte") -> None:
        """Format the query to unest list and create upper and lower limits"""
        for key, value in query.items():
            # Create the upper and lower limits for the keys that allow limits
            if isinstance(value, list) and key in [
                "numero_registro",
                "isin",
                "fecha_registro",
            ]:
                # Check the instances first, if not str, raise Exception
                list_instances = [isinstance(elem, str) for elem in value]
                if not all(list_instances):
                    msg = (
                        f"Expected all elements for {key} to be strings, got"
                        f" {list_instances}"
                    )
                    self.log.error(msg)
                    raise ValueError(msg)
                # Check create the limits for different cases
                if len(value) == 1:
                    query[key] = {mode: value[0]}
                elif len(value) == 2:
                    if value[1] >= value[0]:
                        query[key] = {"$gte": value[0], "$lte": value[1]}
                        continue
                    query[key] = {"$gte": value[1], "lte": value[0]}
                elif len(value) > 2:
                    msg = (
                        "Expected upper and lower limits, got"
                        f" {len(value)} values"
                    )
                    self.log.error(msg)
                    raise ValueError(msg)
            # Raise exception otherwise
            elif not isinstance(value, str):
                msg = f"Expected key {key} to be string, found {type(value)}"
                self.log.error(msg)
                raise ValueError(msg)

    async def get(
        self,
        isin: Optional[Union[str, List[str]]] = None,
        numero_registro: Optional[Union[str, List[str]]] = None,
        nombre: Optional[str] = None,
        fecha_registro: Optional[Union[str, List[str]]] = None,
    ) -> List[DocumentType]:
        """Get method for searching an entry with given search parameters"""
        query_elements: List[
            Tuple[str, Optional[Union[str, List[str], Dict[str, str]]]]
        ] = [
            ("isin", isin),
            ("numero_registro", numero_registro),
            ("nombre", nombre),
            ("fecha_registro", fecha_registro),
        ]
        query: QueryDict = {
            key: value for key, value in query_elements if value is not None
        }
        if not query:
            self.log.error("The request received has no search parameters.")
            return []
        self._format_query(query)
        msg = f"Searching in the database using the parameters: {query}"
        self.log.info(msg)
        return await self.mongo_client.find_entries(query)
