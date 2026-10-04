from app.domain.repositories.file_repository import AbstractFileStorageRepository
from pathlib import Path
from typing import AsyncIterator
import aiofiles, aiofiles.os
from logging import getLogger
import time

logger = getLogger(__name__)

CHUNK_SIZE = 1024 * 1024  # 1MB


class FileStorageRepository(AbstractFileStorageRepository):
    def __init__(self):
        pass

    async def save(self, stream: AsyncIterator[bytes], destination: Path) -> int:
        destination.parent.mkdir(parents=True, exist_ok=True)
        file_size = 0
        start = time.perf_counter()
        async with aiofiles.open(destination, "wb") as out:
            async for (
                chunk
            ) in (
                stream
            ):  # generic async iterator which is not depend on any third party tools like UplaoadFile(fastapi)
                if len(chunk) > CHUNK_SIZE:
                    for i in range(0, len(chunk), CHUNK_SIZE):
                        await out.write(chunk[i : i + CHUNK_SIZE])
                        file_size += CHUNK_SIZE
                    file_size += len(chunk) % CHUNK_SIZE
                else:
                    await out.write(chunk)
                    file_size += len(chunk)
        logger.info(
            "file_written",
            extra={
                "file_name": destination.name,
                "file_size": file_size,
                "duration_ms": (time.perf_counter() - start) * 1000,
            },
        )
        return file_size

    async def delete(self, file_path: Path) -> None:
        start = time.perf_counter()
        if await aiofiles.os.path.exists(file_path):
            await aiofiles.os.remove(file_path)
            logger.info(
                "file_deleted",
                extra={
                    "file_path": str(file_path),
                    "duration_ms": (time.perf_counter() - start) * 1000,
                },
            )
