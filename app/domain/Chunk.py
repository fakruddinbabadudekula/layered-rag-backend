from dataclasses import dataclass
from uuid import UUID

@dataclass
class Chunk:
    chunk_id:UUID
    file_id:UUID