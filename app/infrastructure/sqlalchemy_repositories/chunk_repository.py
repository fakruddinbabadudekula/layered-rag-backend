from app.domain.repositories.chunk_repository import AbstractChunkRepository
from app.domain.Chunk import Chunk as DomainChunk
from app.models.chunk import Chunk as OrmChunk
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from app.infrastructure.mappers import orm_to_chunk, chunk_to_orm


class ChunkRepository(AbstractChunkRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create_bulk_chunks(self, chunks):
        chunks_orm = [chunk_to_orm(chunk) for chunk in chunks]
        self._db.add_all(chunks_orm)

    async def get_chunks(self, file_id):
        result = await self._db.execute(
            select(OrmChunk).where(OrmChunk.file_id == file_id)
        )
        chunks_orm = result.scalars().all()
        return [orm_to_chunk(chunk) for chunk in chunks_orm]

    async def delete_bulk_chunks_by_file_id(self, file_id):
        await self._db.execute(delete(OrmChunk).where(OrmChunk.file_id == file_id))

    async def delete_by_chunk(self, chunk_id):
        await self._db.execute(delete(OrmChunk).where(OrmChunk.chunk_id == chunk_id))

    async def delete_bulk_chunks_by_chunk_id(self, chunk_ids):
        await self._db.execute(delete(OrmChunk).where(OrmChunk.chunk_id.in_(chunk_ids)))
