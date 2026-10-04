from fastapi import APIRouter, Depends, Response, status, Cookie
from app.interface.api.schemas.auth import AccessTokenResponse
from app.interface.api.cookie import delete_refresh_cookie, set_refresh_cookie
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from app.application.auth_service import AuthService
from app.core.db import async_session_factory
from app.schemas.auth import LoginData

router = APIRouter()
auth_service = AuthService(SqlAlchemyUnitOfWork(async_session_factory))


@router.post(
    "/login",
    response_model=AccessTokenResponse,
    summary="Log in with email and password",
    responses={
        401: {"description": "Invalid email or password"},
    },
)
async def login(
    payload: LoginData,
    response: Response,
) -> AccessTokenResponse:
    """
    Authenticate a user and issue tokens.

    - Returns an **access token** in the response body (short-lived, used as
      `Authorization: Bearer <token>` on protected routes).
    - Sets a **refresh token** as an `HttpOnly` cookie, scoped to
      `/api/v1/auth/refresh`, valid for 7 days.
    """
    token_data = await auth_service.login(payload)
    set_refresh_cookie(response, token_data.refresh_token)
    return AccessTokenResponse(
        token=token_data.access_token, expire_at=token_data.access_expire_time
    )


@router.post(
    "/refresh",
    response_model=AccessTokenResponse,
    summary="Exchange a refresh token for a new access token",
    responses={
        401: {"description": "Missing, invalid, or expired refresh token"},
    },
)
async def refresh(
    response: Response,
    token=Cookie(alias="refresh_token"),
) -> AccessTokenResponse:

    token_data = await auth_service.refresh(token)
    set_refresh_cookie(response, token_data.refresh_token)
    return AccessTokenResponse(
        token=token_data.access_token, expire_at=token_data.access_expire_time
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Log out the current user",
)
async def logout(
    response: Response,
    token=Cookie(alias="refresh_token"),
):

    await auth_service.logout(token)
    delete_refresh_cookie(response)

    return
