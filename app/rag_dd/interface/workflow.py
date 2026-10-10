from abc import ABC, abstractmethod
from typing import Any
from app.domain.entities.RetrieverFilter import RetrieverFilter
from app.rag_dd.interface.vector_store import AbstractVectorStore
from app.domain.Notebook import Message


class Workflow(ABC):
    @abstractmethod
    async def execute(
        self,
        messages: list[Message],
        vector_store: AbstractVectorStore,
        retriever_filter: RetrieverFilter,
    ) -> dict[str,Any]: ...
