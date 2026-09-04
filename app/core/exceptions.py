class AppException(Exception):
    status_code = 400

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ResourceNotFound(AppException):
    status_code = 404


class DuplicateResource(AppException):
    status_code = 409


class BusinessRuleError(AppException):
    status_code = 400
