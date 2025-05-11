from src.models.seller import Seller
from ..commands.util import registrarUsuarioEnFirebase
from .base_command import BaseCommannd
from ..models.plan import Plan, PlanSchema, CreatedPlanJsonSchema
from ..session import Session
from ..errors.errors import CodigoNoGenerado, IncompleteParams
from sqlalchemy import or_

class CreatePlan(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
        try:
            posted_plan = PlanSchema(
                only=('vendedores', 'fecha','descripcion')
            ).load(self.data)
            session = Session()

            vendedoresIdList = list(map(lambda vendedor: str(vendedor.get("id")),posted_plan.get("vendedores")))

            vendedores = session.query(Seller).filter(Seller.id.in_(vendedoresIdList)).all()
            if len(vendedores) < 1:
                print("no hay vendedores")
                raise IncompleteParams()
            
            posted_plan["vendedores"] = vendedores

            plan = Plan(**posted_plan)

            session.add(plan)
            session.commit()

            new_plan = CreatedPlanJsonSchema().dump(plan)
            session.close()

            return new_plan
        except TypeError:
            raise IncompleteParams()