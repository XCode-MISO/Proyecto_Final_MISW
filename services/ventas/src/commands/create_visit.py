from .base_command import BaseCommannd
from ..models.visit import Visit, VisitSchema, CreatedVisitJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams
from sqlalchemy import or_

class CreateVisit(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
        try:
            posted_visit = VisitSchema(
                only=('client_id', 'informe', 'fechaVisita', 'latitud', 'longitud')
            ).load(self.data)
            visit = Visit(**posted_visit)
            session = Session()

            session.add(visit)
            session.commit()

            new_visit = CreatedVisitJsonSchema().dump(visit)
            session.close()

            return new_visit
        except TypeError:
            raise IncompleteParams()
        
