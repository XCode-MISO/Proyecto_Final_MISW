class ApiError(Exception):
    code = 422
    description = "Default message"

class IncompleteParams(ApiError):
    code = 400
    description = "Bad request"

class CodigoNoGenerado(ApiError):
    code = 500
    description = "ID not generated"
