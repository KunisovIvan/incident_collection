from pydantic import BaseModel, Extra


class BaseScheme(BaseModel):
    class Config:
        extra = Extra.forbid


class IgnoreExtraScheme(BaseModel):
    class Config:
        extra = Extra.ignore
