from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Any
from app.domain.notebook.models import MessageRole
import uuid


@dataclass
class Message:
    message_id: uuid.UUID
    role: MessageRole
    content: str
    notebook_id: uuid.UUID
    top_k_docs: dict[str, Any]
    created_at: datetime

    @classmethod
    def create(
        cls,
        role: MessageRole,
        content: str,
        notebook_id: uuid.UUID,
        top_k_docs_ids: dict[str, Any] | None = None,
    ):
        return cls(
            message_id=uuid.uuid4(),
            created_at=datetime.now(timezone.utc),
            role=role,
            top_k_docs=top_k_docs_ids,
            content=content,
            notebook_id=notebook_id,
        )
