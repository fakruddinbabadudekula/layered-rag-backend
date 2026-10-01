from dataclasses import dataclass
from datetime import datetime, timezone
from app.domain.notebook.models import FileType
import uuid


@dataclass
class FilesMetadata:
    file_id: uuid.UUID
    notebook_id: uuid.UUID
    type: FileType
    name: str
    size: int
    created_at: datetime

    @classmethod
    def create(cls, notebook_id: uuid.UUID, type: FileType, name: str, size: int):
        return cls(
            file_id=uuid.uuid4(),
            notebook_id=notebook_id,
            type=type,
            name=name,
            size=size,
            created_at=datetime.now(timezone.utc),
        )
