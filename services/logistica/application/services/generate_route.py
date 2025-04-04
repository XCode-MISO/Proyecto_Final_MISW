from typing import List

from logistica.infrastructure.maps.maps import getRouteFromMaps
from logistica.domain.model import Route, parseMapsResponseToRoute
from logistica.infrastructure.db.model import db, Route as DBRoute

def flatten(xss):
    return [x for xs in xss for x in xs]

def paradasToWaypoints(paradas: List[any]):
    listOfLists = list(map(lambda parada: [parada.get("vendedor").get("direccion"), parada.get("cliente").get("direccion")], paradas))
    return flatten(listOfLists)

def generateAndParse(requestJson):
    paradas = requestJson.get("paradas")
    start = requestJson.get("inicio")
    end = requestJson.get("fin")
    waypoints = paradasToWaypoints(paradas)
    calculatedRoute = getRouteFromMaps(start, end, waypoints)
    route: Route =  parseMapsResponseToRoute(requestJson, calculatedRoute)
    return route

def generate_route(requestJson):
    route = generateAndParse(requestJson)

    db.session.add(route.toDBO())
    db.session.commit()
    return route


def update_route(requestJson):
    route_id = requestJson.get("id")
    route: Route = DBRoute.query.get(route_id)
    if route == None:
        raise Exception("No route with that id was found")
    
    filledPutJson = {
        "distancia": requestJson.get("distancia", route.distancia),
        "fecha": requestJson.get("fecha", route.fecha),
        "inicio": requestJson.get("inicio", route.inicio),
        "fin": requestJson.get("fin", route.fin),
        "route_id": requestJson.get("route_id", route.route_id),
        "tiempoEstimado": requestJson.get("tiempoEstimado", route.tiempoEstimado),
        "nombreRuta": requestJson.get("nombreRuta", route.nombreRuta),
        "paradas": requestJson.get("paradas", route.paradas),
    }
    routeUpdated = generateAndParse(filledPutJson).toDBO()

    route.distancia = routeUpdated.distancia
    route.fecha = routeUpdated.fecha
    route.fin = routeUpdated.fin
    route.mapsResponse = routeUpdated.mapsResponse
    route.paradas = routeUpdated.paradas
    route.tiempoEstimado = routeUpdated.tiempoEstimado

    db.session.commit()
    return route

def getDireccion(parada):
    return parada.get("cliente").get("direccion")