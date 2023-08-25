"""
CNMV crawler class with all the methods we need to crawl the CNMV listing page
"""

from typing import Optional

from config import INITIAL_URL
from mongo import DataClient

from .pipelines import MongoDataPipeLine


class CNMVCrawler:
    """CNMV crawler class"""

    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        url: str = INITIAL_URL,
        data_pipeline: Optional[MongoDataPipeLine] = None,
        mongo_client: Optional[DataClient] = None,
    ) -> None:
        """Initialise the class variables"""
        self.url = url
        self.data_pipeline = data_pipeline
        self.mongo_client = mongo_client
