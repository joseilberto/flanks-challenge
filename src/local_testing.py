"""
A local testing script to run the crawler and save the data in MONGO
"""

import asyncio
from typing import no_type_check

from crawler import CNMVCrawler, DataPipeline, MongoDataTypes
from mongo import DataClient


@no_type_check
def main() -> None:
    """Main method"""
    data_client = DataClient(
        db_name="CNMV", collection="cnmv_data", connector=None
    )
    data_pipeline = DataPipeline(MongoDataTypes)
    crawler = CNMVCrawler(mongo_client=data_client, data_pipeline=data_pipeline)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawler.crawl())
    loop.close()


if __name__ == "__main__":
    main()
