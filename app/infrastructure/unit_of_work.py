from app.domain.unit_of_work import AbstractUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.infrastructure.sqlalchemy_repositories import (
    user_repository,
    refresh_token_repository,
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.session_maker: async_sessionmaker[AsyncSession]
        self.db_session: AsyncSession | None = None

    async def __aenter__(self):
        self.db_session = self.session_maker()
        self.user = user_repository.UserRepository(self.db_session)
        self.refresh_token = refresh_token_repository.RefreshTokenRepository(
            self.db_session
        )
        return await super().__enter__()

    async def commit(self) -> None:
        self.db_session.commit()

    async def rollback(self) -> None:
        self.db_session.rollback()

    async def __aexit__(self, *args) -> None:
        await super().__aexit__(*args)
        self.db_session.close()
