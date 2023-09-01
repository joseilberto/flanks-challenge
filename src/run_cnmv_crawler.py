"""
A local testing script to run the crawler and save the data in MONGO
"""

import asyncio
import logging
import sys
from datetime import datetime
from typing import no_type_check

from crawler import MAPPING, CNMVCrawler, DataPipeline
from mongo import DataClient

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s.%(msecs)03dZ %(levelname)-8s "
        "(%(name)s %(funcName)s): %(message)s"
    ),
    datefmt="%Y-%m-%dT%H:%M:%S",
    handlers=[
        logging.FileHandler(
            f"cnmv_crawler_{datetime.today().strftime('%Y_%m_%d')}.log"
        ),
        logging.StreamHandler(sys.stdout),
    ],
)


@no_type_check
def main() -> None:
    """Main method"""
    data_client = DataClient(db_name="CNMV")
    data_pipeline = DataPipeline(MAPPING)
    crawler = CNMVCrawler(mongo_client=data_client, data_pipeline=data_pipeline)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(data_client.set_index())
    loop.run_until_complete(crawler.crawl_and_save())
    loop.close()


if __name__ == "__main__":
    main()
