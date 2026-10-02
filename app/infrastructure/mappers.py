from app.domain import User, Notebook
from app.models import user as user_orm
from dataclasses import asdict

def orm_to_user(orm: user_orm.User) -> User.User:
    user = User.User(
        name=orm.name,
        email=orm.email,
        hashed_password=orm.hashed_password,
        user_id=orm.user_id,
        created_at=orm.created_at,
    )
    return user


def user_to_orm(user: User.User) -> user_orm.User:
    user_dict=asdict(user)
    return user_orm.User(user_dict)