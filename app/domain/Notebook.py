from __future__ import annotations
from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class FileType(str, Enum):
    PDF = ".pdf"


@dataclass
class FileMetadata:
    file_id: UUID
    notebook_id: UUID
    type: FileType
    name: str
    size: int
    created_at: datetime

    @classmethod
    def create(cls, notebook_id: UUID, type: FileType, name: str, size: int) -> FileMetadata:
        return cls(
            file_id=uuid4(),
            notebook_id=notebook_id,
            type=type,
            name=name,
            size=size,
            created_at=datetime.now(timezone.utc),
        )


@dataclass
class Message:
    message_id: UUID
    role: MessageRole
    content: str
    notebook_id: UUID
    top_k_docs_ids: list[UUID] | None
    created_at: datetime

    @classmethod
    def create(
        cls,
        role: MessageRole,
        content: str,
        notebook_id: UUID,
        top_k_docs_ids: list[UUID] | None = None,
    ) -> Message:
        return cls(
            message_id=uuid4(),
            created_at=datetime.now(timezone.utc),
            role=role,
            top_k_docs_ids=top_k_docs_ids,
            content=content,
            notebook_id=notebook_id,
        )


@dataclass
class Notebook:
    notebook_id: UUID
    title: str | None
    user_id: UUID
    created_at: datetime
    messages: list[Message] = field(default_factory=list)
    files_metadata: list[FileMetadata] = field(default_factory=list)
    _new_messages: list[Message] = field(default_factory=list)
    _new_files_metadata: list[FileMetadata] = field(default_factory=list)

    @classmethod
    def create(cls, user_id: UUID, title: str | None = None) -> Notebook:
        return cls(
            notebook_id=uuid4(),
            user_id=user_id,
            title=title,
            created_at=datetime.now(timezone.utc),
        )

    def add_message(self, role: MessageRole, content: str, top_k_docs_ids: list[UUID] | None = None) -> Message:
        message = Message.create(role, content, self.notebook_id, top_k_docs_ids)
        self.messages.append(message)
        self._new_messages.append(message)
        return message

    def add_file_metadata(self, type: FileType, name: str, size: int) -> FileMetadata:
        file_metadata = FileMetadata.create(self.notebook_id, type, name, size)
        self.files_metadata.append(file_metadata)
        self._new_files_metadata.append(file_metadata)
        return file_metadata

    @property
    def new_messages(self) -> list[Message]:
        return list(self._new_messages)

    @property
    def new_files_metadata(self) -> list[FileMetadata]:
        return list(self._new_files_metadata)

    @property
    def has_changes(self) -> bool:
        return bool(self._new_messages or self._new_files_metadata)

    def clear_changes(self) -> None:
        self._new_messages.clear()
        self._new_files_metadata.clear()   