from abc import ABC, abstractmethod
from typing import Optional, TypeVar

_UseCaseRequest = TypeVar("_UseCaseRequest")
_UseCaseResponse = TypeVar("_UseCaseResponse")


class BaseUseCase(ABC):
    @abstractmethod
    async def execute(self, data: _UseCaseRequest) -> Optional[_UseCaseResponse]:
        raise NotImplementedError
