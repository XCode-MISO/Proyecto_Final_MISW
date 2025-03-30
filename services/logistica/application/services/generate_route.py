from typing import List

from logistica.infrastructure.maps.maps import getRouteFromListOfRoutes
from logistica.domain.model import Route, parseMapsResponseToRoute
from logistica.infrastructure.db.model import db


def generate_route(listOfPoints: List[str], pedidos: List):
    calculatedRoute = getRouteFromListOfRoutes(listOfPoints)
    route: Route =  parseMapsResponseToRoute(calculatedRoute, pedidos)

    db.session.add(route.toDBO())
    db.session.commit()
    return route