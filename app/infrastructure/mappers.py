from turtle import title

from app.domain.Notebook import (
    Notebook as DomainNotebook,
    Message as DomainMessage,
    FileMetadata as DomainFileMetadata,
)
from app.domain.User import User as DomainUser
from app.domain.RefreshToken import RefreshToken as DomainRefreshToken
from app.models.user import User as OrmUser
from app.models.refresh_token import RefreshToken as OrmRefreshToken
from app.models.notebook import Notebook as OrmNotebook
from app.models.file import FileMetadata as OrmFileMetadata
from app.models.message import Message as OrmMessage


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


def notebook_to_orm(notebook: DomainNotebook) -> OrmNotebook:
    return OrmNotebook(
        notebook_id=notebook.notebook_id,
        title=notebook.title,
        user_id=notebook.user_id,
        created_at=notebook.created_at,
    )


def orm_to_notebook(
    notebook_orm: OrmNotebook,
    message_orm: list[OrmMessage] | None = None,
    file_orm: list[OrmFileMetadata] | None = None,
) -> DomainNotebook:
    return DomainNotebook(
        notebook_id=notebook_orm.notebook_id,
        title=notebook_orm.title,
        user_id=notebook_orm.user_id,
        created_at=notebook_orm.created_at,
        messages=[orm_to_message(msg) for msg in (message_orm or [])],
        files_metadata=[orm_to_file(file) for file in (file_orm or [])],
    )


def message_to_orm(message: DomainMessage) -> OrmMessage:
    return OrmMessage(
        message_id=message.message_id,
        notebook_id=message.notebook_id,
        content=message.content,
        role=message.role,
        top_k_docs_ids=message.top_k_docs_ids,
        created_at=message.created_at,
    )


def orm_to_message(orm: OrmMessage) -> DomainMessage:
    return DomainMessage(
        message_id=orm.message_id,
        notebook_id=orm.notebook_id,
        content=orm.content,
        role=orm.role,
        top_k_docs_ids=orm.top_k_docs_ids,
        created_at=orm.created_at,
    )


def file_to_orm(file: DomainFileMetadata) -> OrmFileMetadata:
    return OrmFileMetadata(
        file_id=file.file_id,
        notebook_id=file.notebook_id,
        type=file.type,
        name=file.name,
        size=file.size,
        created_at=file.created_at,
    )


def orm_to_file(orm: OrmFileMetadata) -> DomainFileMetadata:
    return DomainFileMetadata(
        file_id=orm.file_id,
        notebook_id=orm.notebook_id,
        type=orm.type,
        name=orm.name,
        size=orm.size,
        created_at=orm.created_at,
    )
