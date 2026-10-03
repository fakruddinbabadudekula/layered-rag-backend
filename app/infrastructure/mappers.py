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
    user_dict = asdict(user)
    return OrmUser(user_dict)


def refresh_token_to_orm(token: DomainRefreshToken) -> OrmRefreshToken:
    token_dict = asdict(token)
    return OrmRefreshToken(token_dict)


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