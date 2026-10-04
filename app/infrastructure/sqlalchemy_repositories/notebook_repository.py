from app.domain.repositories.notebook_repository import AbstractNotebookRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.Notebook import Notebook as DomainNotebook
from app.models.notebook import Notebook as OrmNotebook
from app.models.message import Message as OrmMessage
from app.models.file import FileMetadata as OrmFileMetadata
from uuid import UUID
from sqlalchemy import select, delete, update
from app.infrastructure.mappers import (
    orm_to_notebook,
    notebook_to_orm,
    message_to_orm,
    file_to_orm,
)


class NotebookRepository(AbstractNotebookRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create_notebook(self, notebook: DomainNotebook) -> None:
        new_notebook_orm = notebook_to_orm(notebook)
        self._db.add(new_notebook_orm)

    async def get_notebook(self, notebook_id: UUID) -> DomainNotebook | None:
        result = await self._db.execute(
            select(OrmNotebook).where(OrmNotebook.notebook_id == notebook_id)
        )
        notebook_orm = result.scalar_one_or_none()
        if notebook_orm is None:
            return None

        messages_result = await self._db.execute(
            select(OrmMessage).where(OrmMessage.notebook_id == notebook_orm.notebook_id)
        )
        files_result = await self._db.execute(
            select(OrmFileMetadata).where(
                OrmFileMetadata.notebook_id == notebook_orm.notebook_id
            )
        )
        messages_orm = messages_result.scalars().all()
        files_orm = files_result.scalars().all()
        return orm_to_notebook(notebook_orm, messages_orm, files_orm)

    async def get_notebooks(self, user_id: UUID) -> list[DomainNotebook]:
        result = await self._db.execute(
            select(OrmNotebook).where(OrmNotebook.user_id == user_id)
        )
        notebooks_orm = result.scalars().all()
        return [orm_to_notebook(notebook_orm) for notebook_orm in notebooks_orm]

    async def delete_notebook(self, notebook_id: UUID) -> None:
        await self._db.execute(
            delete(OrmNotebook).where(OrmNotebook.notebook_id == notebook_id)
        )

    async def save(self, notebook: DomainNotebook) -> None:
        if notebook.has_changes():
            messages_orm = [
                message_to_orm(message_orm) for message_orm in (notebook.messages or [])
            ]
            files_orm = [
                file_to_orm(file_orm) for file_orm in (notebook.files_metadata or [])
            ]
            if messages_orm:
                self._db.add_all(messages_orm)
            if files_orm:
                self._db.add_all(files_orm)
        return None