from abc import ABC, abstractmethod
from app.domain.repositories import (
    notebook_repository,
    refresh_token_repository,
    user_repository,
    file_repository,
    chunk_repository,
)


class AbstractUnitOfWork(ABC):
    refresh_tokens: refresh_token_repository.AbstractRefreshTokenRepository
    users: user_repository.AbstractUserRepository
    files: file_repository.AbstractFileStorageRepository
    notebooks: notebook_repository.AbstractNotebookRepository
    chunks: chunk_repository.AbstractChunkRepository

    @abstractmethod
    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    @abstractmethod
    async def __aexit__(self, *args) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
