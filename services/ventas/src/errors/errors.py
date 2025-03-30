#./errors/errors.py
class ApiError(Exception):
    code = 401
    description = "El token no es válido o está vencido."

class InvalidToken(ApiError):
    code = 401
    description = "El token no es válido o está vencido."

class FaultToken(ApiError):
    code = 403
    description = "No hay token en la solicitud."

class MissingField(ApiError):
    code = 400
    description = "Faltan campos requeridos."

class InvalidId(ApiError):
    code = 400
    description = "El id de la publicacion no es un valor string con formato uuid."

class InvalidPost(ApiError):
    code = 404
    description = "La publicación con ese id no existe."

class Invalid(ApiError):
    code = 400
    description = "Parámetro inválido."

class DateInvalid(ApiError):
    code = 400
    description = "fecha de expiracion no es un valor string con formato ISO 8601 (yyyy-mm-ddTHH:MM:SS) en UTC."

class DatePast(ApiError):
    code = 412
    description = "La fecha expiración no es válida"