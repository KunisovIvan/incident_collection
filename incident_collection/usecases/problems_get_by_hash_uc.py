from typing import List

from incident_collection.connectors import MongoDBConnector
from incident_collection.entrypoints.rest.schemas import ProblemResponse, ProblemGetByHashParams
from incident_collection.usecases.base_uc import BaseUseCase


class ProblemsGetByHashUseCase(BaseUseCase):
    def __init__(self, mongo_db: MongoDBConnector):
        self.mongo_db = mongo_db

    async def execute(self, data: ProblemGetByHashParams) -> List[ProblemResponse]:
        problems = self.mongo_db.find_many(
            collection='problems',
            find_clause={'hash': data.hash},
            skip=data.skip,
            limit=data.limit,
        )

        return [ProblemResponse.parse_obj(problem) for problem in problems]
