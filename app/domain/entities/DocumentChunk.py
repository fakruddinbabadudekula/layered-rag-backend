from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class DocumentChunk:
    page_content: str
    metadata: dict[str, Any]

    @classmethod
    def create(cls, page_content: str, metadata: dict[str, Any]) -> DocumentChunk:
        return cls(page_content=page_content, metadata=metadata)
