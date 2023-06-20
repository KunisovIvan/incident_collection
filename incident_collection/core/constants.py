TITLE = "Incident Collection System"
VERSION = "1.0"
DESCRIPTION = "REST API for Incident Collection System"

LOG_FMT_UVICORN = "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
LOG_FMT_LOGURU = (
    "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>] [<level>{level}</level>] "
    "[<cyan>{name}</cyan>:<cyan>{function}</cyan>] - <level>{message}</level>"
)


class ApiTag:
    PROBLEM: str = "Problem"
