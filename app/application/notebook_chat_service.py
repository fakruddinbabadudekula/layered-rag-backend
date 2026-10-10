from __future__ import annotations
from typing import Any
from uuid import UUID
from app.domain.entities.RetrieverFilter import RetrieverFilter
from app.domain.unit_of_work import AbstractUnitOfWork
from app.rag_dd.interface.vector_store import AbstractVectorStore
from app.core.exceptions import InvalidCredentialsException, LLMServieException
from app.domain.Notebook import MessageRole, TopKDocs
from app.rag_dd.interface.workflow import Workflow

class NotebookChatService:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        vector_store: AbstractVectorStore,
        workflow: Workflow,
        retryable_exceptions: tuple[type[BaseException], ...],
    ):
        self._uow = uow
        self._vector_store = vector_store
        self._workflow = workflow
        self._RETRYABLE_LLM_EXCEPTIONS = retryable_exceptions

    async def chat(
        self,
        user_id: UUID,
        notebook_id: UUID,
        query: str,
        retriever_filter: RetrieverFilter,
    ) -> dict[str, Any]:
        print(retriever_filter)
        async with self._uow:
            notebook = await self._uow.notebooks.get_notebook(notebook_id)
            if notebook is None:
                raise InvalidCredentialsException(
                    "Invalid Notebook Id",
                    details={
                        "user_id": str(user_id),
                        "notebook_id": str(notebook_id),
                    },
                )
            user_message = notebook.add_message(role=MessageRole.USER, content=query)
            try:
                response = await self._workflow.execute(
                    notebook.messages, self._vector_store, retriever_filter
                )

            except self._RETRYABLE_LLM_EXCEPTIONS as e:
                raise LLMServieException(
                    "llm_service failed to generate response after retries",
                    details={
                        "user_id": str(user_id),
                        "notebook_id": str(notebook_id),
                    },
                ) from e
            top_k_docs_ids = [
                TopKDocs.create(doc["index"], doc["id"])
                for doc in response["top_k_docs"]
            ]
            content = response["response"]
            assistant_message = notebook.add_message(
                role=MessageRole.ASSISTANT,
                content=content,
                top_k_docs_ids_with_index=top_k_docs_ids,
            )

            await self._uow.notebooks.save(notebook)
            await self._uow.flush()
            await self._uow.commit()
            notebook.clear_changes()
            return {
                "assistant_message": assistant_message,
                "top_k_context": response["top_k_docs"],
            }
