import uvicorn

from incident_collection.core.constants import LOG_FMT_UVICORN
from incident_collection.entrypoints.rest.rest_app import app


def setup_uvicorn_log_config() -> dict:
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = LOG_FMT_UVICORN
    log_config["formatters"]["default"]["fmt"] = LOG_FMT_UVICORN
    return log_config


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=app.state.config.HOST,
        port=app.state.config.PORT,
        log_config=setup_uvicorn_log_config(),
    )
