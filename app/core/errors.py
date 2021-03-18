from collections import Iterable

from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http_error_handler(_, exc: HTTPException) -> JSONResponse:
    return JSONResponse({'errors': [exc.detail]})


async def http_422_error_handler(_, exc: HTTPException) -> JSONResponse:
    errors = {'body': []}

    if isinstance(exc.detail, Iterable) and not isinstance(exc.detail, str):
        for error in exc.detail:
            error_name = '.'.join(
                error['loc'][1:]
            )
            errors['body'].append({error_name: error['msg']})
    else:
        errors['body'].append(exc.detail)

    return JSONResponse({'errors': errors}, status_code=HTTP_422_UNPROCESSABLE_ENTITY)
