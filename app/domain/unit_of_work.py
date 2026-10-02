from app.domain.repositories.user_repository import AbstractUserRepository
from app.domain.repositories.notebook_repository import AbstractNotebookRepository
from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):
    
    @abstractmethod
    async def __aexit__(self, *args) -> None:
        self.rollback()

    @abstractmethod
    async def commit(self) -> None:...

    @abstractmethod
    async def rollback(self) -> None:...

    @property
    @abstractmethod
    def notebooks(self) -> AbstractNotebookRepository:...

    @property
    @abstractmethod
    def users(self) -> AbstractUserRepository:...
