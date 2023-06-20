import time
from typing import Dict, List

from fastapi import APIRouter, status, Request

from incident_collection.core.logger import logger
from incident_collection.entrypoints.rest.schemas import (
    ProblemResponse,
    ProblemData,
    ProblemShortResponse,
    ProblemGetParams, ProblemGetByHashParams,
)
from incident_collection.usecases import ProblemsCreateUseCase, ProblemsGetByHashUseCase, ProblemsGetUseCase

problem_router = APIRouter()


@problem_router.post(
    path="/problems",
    status_code=status.HTTP_201_CREATED,
    response_model=ProblemShortResponse
)
async def add_problem(request: Request, body: Dict) -> ProblemShortResponse:
    case = ProblemsCreateUseCase(mongo_db=request.app.state.mongo_db)
    resp = await case.execute(data=ProblemData(body=body, headers=request.headers))
    return resp


@problem_router.post(
    path="/find",
    status_code=status.HTTP_200_OK,
    response_model=List[ProblemResponse]
)
async def get_problems(request: Request, body: Dict, skip: int = 0, limit: int = 10) -> List[ProblemResponse]:
    case = ProblemsGetUseCase(mongo_db=request.app.state.mongo_db)
    resp = await case.execute(data=ProblemGetParams(body=body, skip=skip, limit=limit))
    return resp


@problem_router.get(
    path="/find2",
    status_code=status.HTTP_200_OK,
    response_model=List[ProblemResponse]
)
async def get_by_hash(request: Request, h: str, skip: int = 0, limit: int = 10) -> List[ProblemResponse]:
    case = ProblemsGetByHashUseCase(mongo_db=request.app.state.mongo_db)
    resp = await case.execute(data=ProblemGetByHashParams(hash=h, skip=skip, limit=limit))
    return resp
