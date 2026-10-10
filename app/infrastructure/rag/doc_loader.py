from typing import Any

from app.rag_dd.interface.doc_process import (
    AbstractTextSplitter,
    AbstractDocumentLoader,
)
from app.domain.entities.DocumentChunk import DocumentChunk
from pathlib import Path
import logging
import time
from app.rag_dd.interface.doc_loader import DocumentLoader

logger = logging.getLogger(__name__)


class LangchainDocumentLoader(DocumentLoader):

    def __init__(
        self, loaders: dict[str, AbstractDocumentLoader], splitter: AbstractTextSplitter
    ):
        self._loaders = loaders
        self._splitter = splitter

    @property
    def supported_extensions(self) -> set[str]:
        return set(self._loaders.keys())

    def _validate_and_return_ext(self, file_path: Path) -> str:
        if not file_path.exists():
            raise FileNotFoundError(f"file_not_found. path={file_path}")
        ext = file_path.suffix.lower()
        if ext not in self._loaders:
            raise ValueError(f"unsupported_file_type. ext={ext}")
        return ext

    async def load_and_split(
        self,
        file_path: Path,
    ) -> list[DocumentChunk]:
        ext = self._validate_and_return_ext(file_path)
        loader = self._loaders[ext]
        t0 = time.perf_counter()
        docs = await loader.load(file_path)
        logger.info(
            "doc_loaded",
            extra={
                "file": file_path.name,
                "pages": len(docs),
                "duration": time.perf_counter() - t0,
            },
        )

        t1 = time.perf_counter()
        chunks = self._splitter.split(docs)
        logger.info(
            "doc_chunked",
            extra={
                "file": file_path.name,
                "chunks": len(chunks),
                "duration": time.perf_counter() - t1,
            },
        )

        return [
            DocumentChunk.create(content.page_content, content.metadata)
            for content in chunks
        ]
