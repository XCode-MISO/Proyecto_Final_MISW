from .base_command import BaseCommannd
from ..models.plan import Plan, PlanJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams
from sqlalchemy import or_

class GetAllPlans(BaseCommannd):
    def __init__(self):
        pass

    def execute(self):
        session = Session()
        plans = session.query(Plan).all()
        session.close()

        schema = PlanJsonSchema(many=True)
        plans_data = schema.dump(plans)
        
        return plans_data