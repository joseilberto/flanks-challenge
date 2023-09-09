"""A listing handler able to list data using different keys"""

from typing import Any, Dict, List, Optional, Union

from sanic.log import logger
from sanic.views import HTTPMethodView

from config import DB_NAME
from data_classes import DocumentType, QueryDict
from mongo import DataClient

from .utils import async_request_params


class InfoHandler(HTTPMethodView):
    # pylint: disable=too-few-public-methods
    """A handler to list elements according to the search key provided"""
    log = logger
    log.info("Initialising the InfoHandler")
    mongo_client = DataClient(db_name=DB_NAME, collection=None, connector=None)

    @async_request_params  # type: ignore
    async def get(
        self,
        isin: Optional[Union[str, List[str]]] = None,
        **kwargs: Dict[str, Any],
    ) -> Optional[DocumentType]:
        # pylint: disable=unused-argument
        """Get method for searching an entry with given search parameters"""
        if isin is None:
            self.log.error("The request didn't received an ISIN value.")
            return None
        try:
            isin = str(isin)
        except ValueError:
            msg = "ISIN value cannot be converted to string"
            self.log.error(msg)
            return None
        query: QueryDict = {"isin": isin}
        msg = f"Listing ISIN {isin} data"
        self.log.info(msg)
        return (await self.mongo_client.find_entries(query))[0]
