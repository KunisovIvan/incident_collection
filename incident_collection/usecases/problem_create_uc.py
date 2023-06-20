import json

from incident_collection.connectors import MongoDBConnector
from incident_collection.entrypoints.rest.schemas import ProblemShortResponse, ProblemData
from incident_collection.usecases.base_uc import BaseUseCase


class ProblemsCreateUseCase(BaseUseCase):
    def __init__(self, mongo_db: MongoDBConnector):
        self.mongo_db = mongo_db

    async def execute(self, data: ProblemData) -> ProblemShortResponse:
        body = dict(sorted(data.body.items()))
        headers = dict(sorted(data.headers.items()))
        hash_data = str(hash(json.dumps({'headers': headers, 'body': body})))
        self.mongo_db.insert_one(
            collection='problems',
            find_clause={
                'body': [{b[0]: b[1]} for b in data.body.items()],
                'headers': [{h[0]: h[1]} for h in data.headers.items()],
                'hash': hash_data
            }
        )
        return ProblemShortResponse(hash=hash_data)
