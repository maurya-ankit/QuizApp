from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_error_handler(_: Request, exec: HTTPException) -> JSONResponse:
    """
    Custom error handler for HTTPException
    """
    return JSONResponse(
        status_code=exec.status_code,
        content={"message": exec.detail},
        media_type="application/json"
    )
