from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.Chunk import Chunk


class AbstractChunkRepository(ABC):
    @abstractmethod
    async def create_bulk_chunks(self, chunks: list[Chunk]) -> None: ...

    @abstractmethod
    async def get_chunks(self, file_id: UUID) -> list[Chunk]: ...

    @abstractmethod
    async def delete_bulk_chunks_by_file_id(self, file_id: UUID): ...

    @abstractmethod
    async def delete_by_chunk(self, chunk_id: UUID): ...

    @abstractmethod
    async def delete_bulk_chunks_by_chunk_id(self, chunk_ids: list[UUID]) -> None: ...
