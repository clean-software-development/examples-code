class ProjectException(Exception):

    ERROR_CODE: int = 500
    ERROR_NAME: str = "INTERNAL_ERROR"

    def __init__(self, message: str = ""):
        self.name = self.ERROR_NAME
        self.status_code = self.ERROR_CODE
        self.message = message
        super().__init__(self.message)


class UnknowError(ProjectException):

    ERROR_CODE: int = 500
    ERROR_NAME: str = "INTERNAL_ERROR"


class ConflictError(ProjectException):

    ERROR_CODE: int = 400
    ERROR_NAME: str = "CONFLICT_ERROR"


class NotFoundError(ProjectException):

    ERROR_CODE: int = 404
    ERROR_NAME: str = "NOT_FOUND_ERROR"
