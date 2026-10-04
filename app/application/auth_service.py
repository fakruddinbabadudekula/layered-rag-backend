from app.domain.RefreshToken import RefreshToken
from app.schemas.user import RegisterUser
from app.schemas.auth import LoginData, TokenData
from app.domain.User import User
from app.domain.unit_of_work import AbstractUnitOfWork
from app.core.security import hash_password
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    hash_token,
)
import uuid
from app.core.exceptions import (
    InvalidCredentialsException,
    RefreshTokenReUsedDetection,
    RefreshTokenValidationException,
)
from datetime import datetime, timezone

_DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$6j2nlBJCSCkFIMTYG4MQYg$hoq39+Hpcozusp8p1h5DtCxF1MjMiHncVfzkkekPipY"


class AuthService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def _generate_tokens(self, user_id: uuid.UUID, now: datetime) -> TokenData:
        user_id = str(user_id)
        access_token, access_expire_time = create_access_token(user_id, now)
        refresh_token, refresh_expire_time = create_refresh_token(user_id, now)
        return TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            access_expire_time=access_expire_time,
            refresh_expire_time=refresh_expire_time,
        )

    async def register(self, user_data: RegisterUser) -> User:
        new_user = User.create(
            **user_data.model_dump(exclude={"password"}),
            hashed_password=hash_password(user_data.password),
        )
        async with self.uow:
            await self.uow.users.create_user(new_user)
            await self.uow.commit()

        return new_user

    async def login(self, user_data: LoginData) -> TokenData:
        async with self.uow:
            user = await self.uow.users.get_user_by_email(user_data.email)
            if user == None:
                verify_password(user_data.password, _DUMMY_HASH)
                raise InvalidCredentialsException(
                    "Invalid credentials email or password",
                    details={"user_email": user_data.email},
                )
            if not verify_password(user_data.password, user.hashed_password):
                raise InvalidCredentialsException(
                    "Invalid credentials email or password",
                    details={"user_email": user_data.email},
                )
            now = datetime.now(timezone.utc)
            token_data = self._generate_tokens(user.user_id, now)
            await self.uow.refresh_tokens.create_token(
                RefreshToken.create(
                    hashed_token=hash_token(token_data.refresh_token),
                    user_id=user.user_id,
                    family_id=uuid.uuid4(),
                    created_at=now,
                )
            )
            await self.uow.commit()
            return token_data

    async def refresh(self, token: str) -> TokenData:
        async with self.uow:
            stored_token = await self.uow.refresh_tokens.get_token_by_hash(
                hash_token(token)
            )
            if stored_token is None:
                raise RefreshTokenValidationException(
                    "Invalid credentials token",
                    details={"WWW-Authenticate": "Bearer"},
                )
            if stored_token.is_revoked():
                await self.uow.refresh_tokens.revoke_all_tokens_by_family_id(
                    stored_token.family_id
                )
                raise RefreshTokenReUsedDetection(
                    "Refresh token reuse detected; session revoked",
                    details={"user_id": str(stored_token.user_id)},
                )
            if stored_token.is_expired():
                raise RefreshTokenValidationException(
                    "Refresh token expired",
                    details={"WWW-Authenticate": "Bearer"},
                )

            user = await self.uow.users.get_user_by_id(stored_token.user_id)
            if not user:
                raise RefreshTokenValidationException(
                    "Invalid credentials token",
                    details={"WWW-Authenticate": "Bearer"},
                )
            now = datetime.now(timezone.utc)
            token_data = self._generate_tokens(user.user_id, now)
            stored_token.revoke()
            await self.uow.refresh_tokens.save(stored_token)
            await self.uow.refresh_tokens.create_token(
                RefreshToken.create(
                    hashed_token=hash_token(token_data.refresh_token),
                    user_id=user.user_id,
                    family_id=stored_token.family_id,
                    created_at=now,
                )
            )
            await self.uow.commit()
            return token_data

    async def logout(self, token: str):
        async with self.uow:
            stored_token = await self.uow.refresh_tokens.get_token_by_hash(
                hash_token(token)
            )
            if stored_token is None or stored_token.is_expired():
                return  # idempotent, nothing to do
            if stored_token.is_revoked():
                await self.uow.refresh_tokens.revoke_all_tokens_by_family_id(
                    stored_token.family_id
                )
                raise RefreshTokenReUsedDetection(
                    "Refresh token reuse detected; session revoked",
                    details={"user_id": str(stored_token.user_id)},
                )
            stored_token.revoke()
            await self.uow.refresh_tokens.save(stored_token)
            await self.uow.commit()
