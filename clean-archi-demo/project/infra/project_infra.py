import os
from enum import Enum

from project.domain.utils.singleton import Singleton
from project.domain.service import Service


class InfraType(str, Enum):
    MEMORY = "memory"
    AWS = "aws"


class _LazyFactory(metaclass=Singleton):

    def __init__(self) -> None:
        self._infra = os.environ.get("PROJECT_INFRA")
        self._setup()

    def _setup(self):
        self.__service: Service | None = None

    def get_service(self) -> Service:
        if self.__service:
            return self.__service
        
        if self._infra == InfraType.MEMORY:
            from project.infra.memory.repository import RepositoryMemory
            repository = RepositoryMemory()
        elif self._infra == InfraType.AWS:
            raise NotImplementedError("AWS Infrastructure not implemented for Service class")
        else:
            raise NotImplementedError()
        
        self.__service = Service(repository=repository)

        return self.__service
    
    service: Service = property(get_service)


ProjectInfra = _LazyFactory()