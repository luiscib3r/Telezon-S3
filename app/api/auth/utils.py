from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from app.models.user import ADMIN_ROLE, User


def check_role_admin(user: User):
    if user.role != ADMIN_ROLE:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You do not have the necessary permissions to perform this operation",
        )


def is_admin(user: User):
    return user.role == ADMIN_ROLE
