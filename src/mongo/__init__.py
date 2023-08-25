"""Initialise mongo clients"""

from .mongo_data import MongoDataClient as DataClient

__all__ = ["DataClient"]
