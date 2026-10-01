from typing import Optional
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from app.domain.notebook.FilesMetadata import FilesMetadata
from app.domain.notebook.Message import Message


@dataclass
class Notebook:
    notebook_id: uuid.UUID
    title: str | None
    user_id: uuid.UUID
    created_at: datetime
    messages: Optional[list[Message]]
    files_metadata: Optional[list[FilesMetadata]]
    _new_messages:Optional[list[Message]]
    _new_files_metadata: Optional[list[FilesMetadata]]

    @classmethod
    def create(cls, user_id: uuid.UUID, title: str | None = None):
        return cls(
            notebook_id=uuid.uuid4(),
            user_id=user_id,
            title=title,
            created_at=datetime.now(timezone.utc),
        )
