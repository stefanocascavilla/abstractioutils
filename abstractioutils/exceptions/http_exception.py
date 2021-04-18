class HTTPException(Exception):
    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code

    def get_status_code(self) -> int:
        return self.status_code

    def get_message(self) -> str:
        return self.__str__()
