from typing import Set

from pydantic import BaseSettings, validator, MongoDsn


class MongoConfig(BaseSettings):
    class Config:
        env_prefix = "MONGO_"
        env_file = ".env"

    DB: str
    HOST: str
    PORT: int
    URL: str = ""

    @validator("URL", pre=True)
    def url(cls, _, values):
        return MongoDsn.build(
            scheme="mongodb",
            user=values.get("USER"),
            password=values.get("PASS"),
            host=values.get("HOST"),
            port=str(values.get("PORT")),
            path=f"/{values.get('DB') or ''}",
        )


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    LOGGING_LEVEL: str = "DEBUG"

    CORS_ALLOW_ORIGINS: Set[str] = {"*"}
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: Set[str] = {"*"}
    CORS_ALLOW_HEADERS: Set[str] = {"*"}

    MONGO_CONFIG: MongoConfig = MongoConfig()

    HOST: str
    PORT: int


settings = Settings()
