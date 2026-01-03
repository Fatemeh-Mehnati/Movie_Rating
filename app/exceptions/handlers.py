import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

logger = logging.getLogger(__name__)


def success(data, status_code: int = 200):
    return JSONResponse(status_code=status_code, content={"status": "success", "data": data})


def failure(code: int, message: str):
    return JSONResponse(
        status_code=code,
        content={"status": "failure", "error": {"code": code, "message": message}},
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    # ✅ Log all validation errors (422) to file
    # Keep details minimal to avoid leaking sensitive data
    logger.error(
        "Request validation error",
        extra={"path": str(request.url.path), "method": request.method},
        exc_info=True,
    )
    return failure(422, "Invalid request")


async def http_exception_handler(request: Request, exc: HTTPException):
    # ✅ Log all HTTP exceptions (includes your custom APIException and also unexpected HTTPException)
    status_code = getattr(exc, "status_code", 500)

    # If detail follows your APIException structure:
    if isinstance(getattr(exc, "detail", None), dict) and "code" in exc.detail and "message" in exc.detail:
        code = int(exc.detail.get("code", status_code))
        message = str(exc.detail.get("message", "Error"))

        logger.error(
            "HTTP exception",
            extra={"path": str(request.url.path), "method": request.method, "code": code, "message": message},
            exc_info=True,
        )
        return failure(code, message)

    # Generic HTTPException (or unexpected shape)
    logger.error(
        "HTTP exception",
        extra={"path": str(request.url.path), "method": request.method, "code": status_code},
        exc_info=True,
    )
    return failure(status_code, "Internal server error")
