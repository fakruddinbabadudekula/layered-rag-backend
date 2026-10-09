"""Module for register new user.
contains only register router"""

from fastapi import APIRouter, Depends
from app.schemas.user import RegisterUser
from app.interface.api.schemas.auth import BaseUser
from fastapi import status
from app.domain.unit_of_work import AbstractUnitOfWork
from app.interface.api.dependencies import get_uow
from app.core.composition import get_auth_service

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
async def register(payload: RegisterUser, uow: AbstractUnitOfWork = Depends(get_uow)):
    """
    Create a new user account.

    Passwords are hashed with Argon2 before storage; the raw password is
    never persisted or returned.
    """
    auth_service = get_auth_service(uow)
    return await auth_service.register(payload)
