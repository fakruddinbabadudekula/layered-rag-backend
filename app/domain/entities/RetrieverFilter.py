from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class RetrieverFilter:
    search_type: Any
    search_kwargs: dict[str, Any]

    @classmethod
    def create(
        cls,
        search_type: Any,
        search_kwargs: dict[str, Any],
    ) -> "RetrieverFilter":
        return cls(
            search_type=search_type,
            search_kwargs=search_kwargs,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)