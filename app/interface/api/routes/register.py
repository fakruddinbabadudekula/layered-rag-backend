"""Module for register new user.
contains only register router"""

from fastapi import APIRouter
from app.schemas.user import RegisterUser
from app.interface.api.schemas.auth import BaseUser
from app.application.auth_service import AuthService
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from app.core.db import async_session_factory
from fastapi import status

auth_service = AuthService(SqlAlchemyUnitOfWork(async_session_factory))
router = APIRouter()


@router.post(
    "/register",
    response_model=BaseUser,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        409: {"description": "A user with this email already exists"},
    },
)
async def register(payload: RegisterUser):
    """
    Create a new user account.

    Passwords are hashed with Argon2 before storage; the raw password is
    never persisted or returned.
    """
    return await auth_service.register(payload)
