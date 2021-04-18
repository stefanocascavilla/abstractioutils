from abstractioutils.exceptions.http_exception import HTTPException


class ComputeEngineException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code, message)
