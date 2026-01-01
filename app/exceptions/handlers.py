from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def success(data, status_code: int = 200):
    return JSONResponse(status_code=status_code, content={"status": "success", "data": data})


def failure(code: int, message: str):
    return JSONResponse(
        status_code=code,
        content={"status": "failure", "error": {"code": code, "message": message}},
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    # خطاهای Pydantic / FastAPI (مثل ورودی اشتباه)
    return failure(422, "Invalid request")


async def http_exception_handler(request: Request, exc):
    # خطاهای HTTPException که detail ما dict است
    if isinstance(getattr(exc, "detail", None), dict) and "code" in exc.detail and "message" in exc.detail:
        return failure(exc.detail["code"], exc.detail["message"])
    return failure(getattr(exc, "status_code", 500), "Internal server error")
