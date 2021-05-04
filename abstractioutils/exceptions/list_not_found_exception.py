from abstractioutils.exceptions.http_exception import HTTPException


class HelpersException(HTTPException):
    def __init__(self, message: str):
        super().__init__(404, message)
