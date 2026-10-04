from app.domain.User import User as DomainUser
from app.domain.RefreshToken import RefreshToken as DomainRefreshToken
from app.models.user import User as OrmUser
from app.models.refresh_token import RefreshToken as OrmRefreshToken
from dataclasses import asdict


def orm_to_user(orm: OrmUser) -> DomainUser:
    user = DomainUser(
        name=orm.name,
        email=orm.email,
        hashed_password=orm.hashed_password,
        user_id=orm.user_id,
        created_at=orm.created_at,
    )
    return user


def user_to_orm(user: DomainUser) -> OrmUser:
    return OrmUser(
        name=user.name,
        email=user.email,
        hashed_password=user.hashed_password,
        user_id=user.user_id,
        created_at=user.created_at,
    )


def refresh_token_to_orm(token: DomainRefreshToken) -> OrmRefreshToken:
    return OrmRefreshToken(
        token_id=token.token_id,
        hashed_token=token.hashed_token,
        status=token.status,
        user_id=token.user_id,
        created_at=token.created_at,
        family_id=token.family_id,
        expires_at=token.expires_at,
        revoked_at=token.revoked_at,
    )   




def orm_to_refresh_token(orm: OrmRefreshToken) -> DomainRefreshToken:
    token = DomainRefreshToken(
        token_id=orm.token_id,
        hashed_token=orm.hashed_token,
        status=orm.status,
        user_id=orm.user_id,
        created_at=orm.created_at,
        family_id=orm.family_id,
        expires_at=orm.expires_at,
        revoked_at=orm.revoked_at,
    )
    return token