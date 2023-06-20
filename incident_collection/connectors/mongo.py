from typing import Iterable

import pymongo
from fastapi import HTTPException
from yarl import URL

from incident_collection.core.logger import logger


class MongoDBConnector:
    connection = None
    uri: str = None
    database = None
    db = None

    def __init__(self, uri: str):
        self.uri = uri
        self.database = URL(uri).name

    def connect(self):
        if not self.connection:
            try:
                self.connection = pymongo.MongoClient(self.uri)
            except Exception as ex:
                logger.error(f'Connect MongoDB error: {ex}')
                raise HTTPException(detail='Connect MongoDB error', status_code=500)
        self.db = self.connection[self.database]

    def _reconnect(self):
        if not self.connection:
            self.connect()

    def create_index(self, collection: str, field: str):
        self._reconnect()
        try:
            self.db[collection].create_index(field)
        except Exception as ex:
            logger.error(f'Create index error: {ex}')

    def find_one(self, collection: str, find_clause: dict) -> dict:
        self._reconnect()
        return self.db[collection].find_one(find_clause) or {}

    def find_many(self, collection: str, find_clause: dict, skip: int, limit: int) -> Iterable[dict]:
        self._reconnect()
        return self.db[collection].find(find_clause).skip(skip).limit(limit)

    def insert_one(self, collection: str, find_clause: dict) -> dict:
        self._reconnect()
        try:
            return self.db[collection].insert_one(find_clause)
        except Exception as ex:
            logger.error(f'Insert one Error: {ex}')
            raise HTTPException(detail='Insert one Error', status_code=500)

    def update_one(self, collection: str, find_clause: dict, update_clause: dict) -> dict:
        self._reconnect()
        return self.db[collection].update_one(find_clause, update_clause)

    def delete_one(self, collection: str, find_clause: dict) -> dict:
        self._reconnect()
        return self.db[collection].delete_one(find_clause)

    def delete_many(self, collection: str, find_clause: dict) -> dict:
        self._reconnect()
        return self.db[collection].delete_many(find_clause)
