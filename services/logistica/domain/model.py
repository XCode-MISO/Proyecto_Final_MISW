
import json
from typing import List
import uuid
from logistica.infrastructure.maps.types import Leg, TypedObject
from logistica.infrastructure.maps.maps import parse_json
from logistica.infrastructure.db.model import Route as DBRoute, Pedido as DBPedido


class Pedido():
    pedido_id = str
    direccion = str
    leg = Leg

    def __init__(self, pedido_id, direccion, leg) -> None:
        self.pedido_id = pedido_id
        self.direccion = direccion
        self.leg = leg

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    def toDBO(self):
        return DBPedido(
            pedido_id=self.pedido_id,
            direccion=self.direccion
        )


class Route():
    route_id = str
    nombreRuta = str
    distancia = float
    tiempoEstimado = int
    pedidos= List[Pedido]
    mapsResponse= any

    def __init__(self, route_id, nombreRuta, distancia, tiempoEstimado, pedidos, mapsResponse) -> None:
        self.route_id = route_id
        self.nombreRuta = nombreRuta
        self.distancia = distancia
        self.tiempoEstimado = tiempoEstimado
        self.pedidos = pedidos
        self.mapsResponse = mapsResponse

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    def toDBO(self):
        return DBRoute(
            route_id=self.route_id,
            nombreRuta=self.nombreRuta,
            distancia=self.distancia,
            tiempoEstimado=self.tiempoEstimado,
            pedidos=list(map(lambda pedido: pedido.toDBO(), self.pedidos)),
            mapsResponse=json.dumps(self.mapsResponse)
        )


def parseMapsResponseToRoute(mapsResponse, pedidos):
    parsedResponse: TypedObject = parse_json(mapsResponse)[0]

    def getRouteName(legs: List[Leg]):
        return '_'.join(str(leg.start_address) for leg in legs)

    def getDistance(legs):
        return sum(leg.distance.value for leg in legs)

    def getDuration(legs):
        return sum(leg.duration.value for leg in legs)

    return Route(
        route_id=str(uuid.uuid4()),
        nombreRuta=getRouteName(parsedResponse.legs),
        distancia=getDistance(parsedResponse.legs),
        tiempoEstimado=getDuration(parsedResponse.legs),
        pedidos=[Pedido(
            pedido_id=pedido.get("id"),
            direccion=pedido.get("cliente").get("direccion"),
            leg=parsedResponse.legs[i]
        ) for i, pedido in enumerate(pedidos)],
        mapsResponse=mapsResponse
    )
