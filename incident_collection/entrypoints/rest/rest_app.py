from functools import partial

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from incident_collection.connectors.mongo import MongoDBConnector
from incident_collection.core.constants import DESCRIPTION, TITLE, VERSION, ApiTag
from incident_collection.core.logger import logger
from incident_collection.core.settings import settings
from incident_collection.entrypoints.rest.routes import problem_router


async def setup_connectors(app: FastAPI):
    mongo_db = MongoDBConnector(uri=settings.MONGO_CONFIG.URL)
    mongo_db.connect()
    mongo_db.create_index(collection='problems', field='hash')
    mongo_db.create_index(collection='problems', field='body')
    mongo_db.create_index(collection='problems', field='headers')
    app.state.mongo_db = mongo_db


def create_app() -> FastAPI:
    logger.info(f"API settings: {settings.dict()}")

    app = FastAPI(
        title=TITLE,
        version=VERSION,
        description=DESCRIPTION,
    )

    app.state.config = settings
    app.add_event_handler(event_type='startup', func=partial(setup_connectors, app=app))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    app.include_router(
        problem_router,
        tags=[ApiTag.PROBLEM],
    )

    return app


app = create_app()
