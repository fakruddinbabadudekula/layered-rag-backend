from abc import ABC, abstractmethod
from typing import Any
from langchain_core.vectorstores.base import VectorStoreRetriever
from app.domain.entities.DocumentChunk import DocumentChunk

class AbstractVectorStore(ABC):
    @abstractmethod
    async def add_documents(
        self,
        chunks: list[DocumentChunk],
    ) -> list[str]: ...

    @abstractmethod
    async def delete(self, chunk_ids: list[str]) -> None | bool: ...

    @abstractmethod
    def get_retriever(self, **kwargs: Any) -> VectorStoreRetriever: ...
