class ApiError(Exception):
    code = 422
    description = "Default message"

class IncompleteParams(ApiError):
    code = 400
    description = "Bad request"
