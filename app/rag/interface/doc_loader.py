from typing import Any
from app.rag.interface.doc_process import (
    AbstractTextSplitter,
    AbstractDocumentLoader,
)
from app.domain.entities.DocumentChunk import DocumentChunk
from abc import ABC, abstractmethod
from pathlib import Path


class DocumentLoader(ABC):
    loaders: dict[str, AbstractDocumentLoader]
    splitter: AbstractTextSplitter

    @property
    @abstractmethod
    def supported_extensions(self) -> set[str]: ...

    @abstractmethod
    async def load_and_split(self, file_path: Path) -> list[DocumentChunk]: ...
