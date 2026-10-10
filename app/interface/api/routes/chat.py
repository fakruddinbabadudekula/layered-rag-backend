"""Module for conversation routers
contains chat router which is async without streaming"""

from fastapi import APIRouter, Depends, Request
from app.interface.api.schemas.chat import ChatRequest, ChatRespose
from app.interface.api.dependencies import get_current_user, get_uow
from app.models.user import User
from app.core.composition import get_notebook_chat_service, get_retriever_filter
from app.domain.unit_of_work import AbstractUnitOfWork

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatRespose,
    summary="Ask a question about the documents in a session",
    responses={
        404: {
            "description": "notebook_id does not exist or does not belong to the current user"
        },
        503: {"description": "The LLM provider failed or timed out after retries"},
    },
)
async def chat(
    payload: ChatRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> ChatRespose:
    """
    Runs the RAG pipeline: retrieves the top-k relevant chunks from the
    session's documents, then generates an answer that cites its sources
    as `[1]`, `[2]`, etc. `top_k_docs` in the response lists the chunks used.
    """
    notebook_chat_service = get_notebook_chat_service(
        uow, request.app.state.vector_store
    )
    user_id = current_user.user_id
    notebook_id = payload.notebook_id
    retriever_filter = get_retriever_filter(user_id, notebook_id)
    query = payload.query
    response = await notebook_chat_service.chat(
        user_id, notebook_id, query, retriever_filter
    )
    return ChatRespose(
        query=payload.query,
        response=response["assistant_message"].content,
        top_k_context=response["top_k_context"],
    )
