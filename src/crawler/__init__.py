"""
Initialiser for the crawler folder
"""

from .cnmv import CNMVCrawler
from .pipelines import MAPPING
from .pipelines import MongoDataPipeLine as DataPipeline

__all__ = ["CNMVCrawler", "DataPipeline", "MAPPING"]
