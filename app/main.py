from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

from app.core.logging import setup_logging
from app.exceptions.handlers import request_validation_exception_handler, http_exception_handler
from app.controller.movies import router as movies_router

# ✅ Enable logging as early as possible
setup_logging()

app = FastAPI(title="Movie Rating System", version="1.0.0")

app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(movies_router)

@app.get("/health")
def health():
    return {"status": "ok"}
