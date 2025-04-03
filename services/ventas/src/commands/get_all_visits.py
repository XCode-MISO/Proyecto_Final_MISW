from .base_command import BaseCommannd
from ..models.visit import Visit, VisitJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams
from sqlalchemy import or_

class GetAllVisits(BaseCommannd):
    def __init__(self):
        pass

    def execute(self):
        session = Session()
        visits = session.query(Visit).all()
        session.close()

        schema = VisitJsonSchema(many=True)
        visits_data = schema.dump(visits)
        
        return visits_data