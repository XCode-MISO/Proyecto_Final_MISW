import json
from typing import List
import uuid

from logistica.infrastructure.maps.maps import getRouteFromMaps
from logistica.domain.model import Cliente, Parada, Route, Vendedor, parseMapsResponseToRoute
from logistica.infrastructure.db.model import db, Route as DBRoute, Cliente as DBCliente, Vendedor as DBVendedor, Parada as DBParada


def flatten(xss):
    return [x for xs in xss for x in xs]


def paradasToWaypoints(paradas: List[any]):
    listOfLists = list(map(lambda parada: [parada.get("vendedor").get(
        "direccion"), parada.get("cliente").get("direccion")], paradas))
    return flatten(listOfLists)


def generateAndParse(requestJson):
    paradas = requestJson.get("paradas")
    start = requestJson.get("inicio")
    end = requestJson.get("fin")
    waypoints = paradasToWaypoints(paradas)
    calculatedRoute = getRouteFromMaps(start, end, waypoints)
    route: Route = parseMapsResponseToRoute(requestJson, calculatedRoute)
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
    }
    routeUpdated = generateAndParse(filledPutJson).toDBO()

    route.distancia = routeUpdated.distancia
    route.fecha = routeUpdated.fecha
    route.fin = routeUpdated.fin
    route.mapsResponse = routeUpdated.mapsResponse
    route.tiempoEstimado = routeUpdated.tiempoEstimado

    db.session.commit()
    return route


def getDireccion(parada):
    return parada.get("cliente").get("direccion")


def add_stop_route(id, parada):
    route_id = id
    route: Route = DBRoute.query.get(route_id)
    if route == None:
        raise Exception("No route found")
    cliente = parada.get("cliente")
    vendedor = parada.get("vendedor")

    clienteDB = DBCliente.query.get(cliente.get("id",))
    clienteFinal = clienteDB if clienteDB != None else Cliente(
        cliente_id=cliente.get("id", str(uuid.uuid4())),
        direccion=cliente.get("direccion"),
        nombre=cliente.get("nombre")
    ).toDBO()

    vendedorDB = DBVendedor.query.get(vendedor.get("id"))
    vendedorFinal = vendedorDB if vendedorDB != None else Vendedor(
        vendedor_id=vendedor.get("id", str(uuid.uuid4())),
        direccion=vendedor.get("direccion"),
        nombre=vendedor.get("nombre")
    ).toDBO()

    parada = DBParada(
        parada_id=parada.get("id", str(uuid.uuid4())),
        cliente=clienteFinal,
        vendedor=vendedorFinal,
        fecha=parada.get("fecha"),
        nombre=parada.get("nombre"),
    )
    route.paradas.append(parada)
    updatedRoute = generateAndParse(route.toJSON()).toDBO()
    route.mapsResponse = updatedRoute.mapsResponse

    db.session.commit()
    return route
