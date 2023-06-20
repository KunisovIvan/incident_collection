import logging
import sys

from loguru import logger

from incident_collection.core.constants import LOG_FMT_LOGURU
from incident_collection.core.settings import settings


class EndpointFilter(logging.Filter):
    def __init__(
            self,
            path: str,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._path = path

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find(self._path) == -1


class CustomizeLogger:
    logger = None

    @classmethod
    def make_logger(cls, level: str, format: str):
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
        )
        uvi_access = logging.getLogger('uvicorn.access')
        uvi_access.addFilter(EndpointFilter('/healthcheck'))
        uvi_access.addFilter(EndpointFilter('/docs'))
        uvi_access.addFilter(EndpointFilter('/openapi.json'))
        uvi_access.addFilter(EndpointFilter('/metrics'))

        cls.logger = logger

        return cls.logger


logger = CustomizeLogger.make_logger(level=settings.LOGGING_LEVEL, format=LOG_FMT_LOGURU)
