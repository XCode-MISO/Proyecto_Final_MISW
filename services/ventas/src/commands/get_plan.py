from .base_command import BaseCommannd
from ..models.plan import Plan, PlanJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams
from sqlalchemy import or_

class GetPlan(BaseCommannd):
    def __init__(self, id):
        self.id = id

    def execute(self):
        session = Session()
        plan = session.query(Plan).filter(Plan.id == self.id).one()
        session.close()

        schema = PlanJsonSchema()
        plan = schema.dump(plan)
        session.close()

        return plan