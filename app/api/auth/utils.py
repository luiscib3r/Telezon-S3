from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from app.models.user import User, ADMIN_ROLE


def check_role_admin(user: User):
    if user.role != ADMIN_ROLE:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="You do not have the necessary permissions to perform this operation"
        )
