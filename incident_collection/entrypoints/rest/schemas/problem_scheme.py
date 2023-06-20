from itertools import chain
from typing import Dict, List

from pydantic import validator

from incident_collection.entrypoints.rest.schemas import BaseScheme, IgnoreExtraScheme


class ProblemData(BaseScheme):
    body: Dict
    headers: Dict


class ProblemShortResponse(IgnoreExtraScheme):
    hash: str


class ProblemResponse(IgnoreExtraScheme):
    hash: str
    body: Dict
    headers: Dict

    @validator('body', 'headers', pre=True)
    def list_to_dict(cls, value):
        if isinstance(value, list):
            result = {}
            for v in value:
                result.update(v)
            return result
        return value


class ProblemGetParams(BaseScheme):
    body: Dict
    skip: int
    limit: int


class ProblemGetByHashParams(BaseScheme):
    hash: str
    skip: int
    limit: int
