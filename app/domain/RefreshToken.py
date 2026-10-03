from __future__ import annotations
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
from enum import Enum


class TokenStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


@dataclass
class RefreshToken:
    token_id: UUID
    hashed_token: str
    status: TokenStatus
    user_id: UUID
    created_at: datetime
    family_id: UUID
    expires_at: datetime
    revoked_at: datetime | None

    @classmethod
    def create(
        cls,
        hashed_token: str,
        user_id: UUID,
        family_id: UUID,
        refresht_token_expire_days: int = 7,
    ) -> RefreshToken:
        now = datetime.now(timezone.utc)
        return cls(
            token_id=uuid4(),
            hashed_token=hashed_token,
            status=TokenStatus.ACTIVE,
            user_id=user_id,
            created_at=now,
            family_id=family_id,
            expires_at=now + timedelta(days=refresht_token_expire_days),
            revoked_at=None,
        )

    def revoke(self) -> None:
        if self.status != TokenStatus.ACTIVE:
            raise ValueError("Cannot revoke an already revoked/expired token")
        self.status = TokenStatus.REVOKED
        self.revoked_at = datetime.now(timezone.utc)

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at

    def is_valid(self) -> bool:
        return self.status == TokenStatus.ACTIVE and self.is_expired
