from app.rag_dd.interface.vector_store import AbstractVectorStore
from app.domain.entities.DocumentChunk import DocumentChunk
import time
import logging

logger = logging.getLogger(__name__)


class VectorStoreService:
    def __init__(self, vector_store: AbstractVectorStore):
        self._vector_store = vector_store

    async def aadd_documents(self, docs: list[DocumentChunk]) -> list[str]:
        start = time.perf_counter()
        if len(docs) == 0 or not docs:
            raise ValueError(f"Docs must be atleast one. Passed empty")
        docs_ids = await self._vector_store.add_documents(docs)
        logger.info(
            "Successfully_added_docs_to_vector_store",
            extra={
                "count": len(docs),
                "duration": time.perf_counter() - start,
            },
        )
        return docs_ids

    async def adelete_documents(self, doc_ids: list[str]) -> None | bool:
        start = time.perf_counter()
        result = await self._vector_store.delete(doc_ids)
        if result or result is None:
            logger.info(
                "Succesfully_deleted_docs_from_vector_store",
                extra={"count": len(doc_ids), "duration": time.perf_counter() - start},
            )
        else:
            logger.info("Unable_to_delete_docs", extra={"docs_ids": doc_ids})
        return result
