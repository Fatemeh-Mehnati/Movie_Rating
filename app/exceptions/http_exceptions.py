from fastapi import HTTPException


class APIException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail={"code": status_code, "message": message})


class NotFound(APIException):
    def __init__(self, message: str = "Not found"):
        super().__init__(status_code=404, message=message)


class ValidationError(APIException):
    def __init__(self, message: str = "Validation error"):
        super().__init__(status_code=422, message=message)
