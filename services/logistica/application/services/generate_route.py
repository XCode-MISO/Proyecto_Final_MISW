from typing import List

from logistica.infrastructure.maps.maps import getRouteFromMaps
from logistica.domain.model import Route, parseMapsResponseToRoute
from logistica.infrastructure.db.model import db


def generate_route(requestJson):
    paradas = requestJson.get("paradas")
    start = requestJson.get("inicio")
    end = requestJson.get("fin")
    calculatedRoute = getRouteFromMaps(start, end, list(map(getDireccion, paradas)))
    route: Route =  parseMapsResponseToRoute(requestJson, calculatedRoute)

    db.session.add(route.toDBO())
    db.session.commit()
    return route


def update_route(requestJson):
    paradas = requestJson.get("paradas")
    start = requestJson.get("inicio")
    end = requestJson.get("fin")
    calculatedRoute = getRouteFromMaps(start, end, list(map(getDireccion, paradas)))
    route: Route =  parseMapsResponseToRoute(requestJson, calculatedRoute)

    db.session.add(route.toDBO())
    db.session.commit()
    return route

def getDireccion(parada):
    return parada.get("cliente").get("direccion")