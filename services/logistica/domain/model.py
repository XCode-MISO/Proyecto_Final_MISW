
import datetime
import json
from typing import List
import uuid
from logistica.infrastructure.maps.types import Leg, TypedObject
from logistica.infrastructure.maps.maps import parse_json
from logistica.infrastructure.db.model import Route as DBRoute, Pedido as DBPedido, Cliente as DBCliente
import datetime

class Cliente():
    cliente_id = str
    direccion = str
    
    def __init__(self, cliente_id, direccion) -> None:
        self.cliente_id = cliente_id
        self.direccion = direccion
    
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    def toDBO(self):
        return DBCliente(
            cliente_id=self.cliente_id,
            direccion=self.direccion
        )


class Pedido():
    pedido_id = str
    nombre = str
    fecha = str
    clientes = List[Cliente]

    def __init__(self, pedido_id, nombre, fecha, clientes) -> None:
        self.pedido_id = pedido_id
        self.nombre = nombre
        self.fecha = fecha
        self.clientes = clientes

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    def toDBO(self):
        return DBPedido(
            pedido_id=self.pedido_id,
            nombre=self.nombre,
            fecha=self.fecha,
            clientes=list(map(lambda cliente: cliente.toDBO(), self.clientes)),
        )


class Route():
    route_id = str
    nombreRuta = str
    distancia = float
    tiempoEstimado = int
    pedidos= List[Pedido]
    fecha = str
    mapsResponse= any

    def __init__(self, route_id, nombreRuta, distancia, tiempoEstimado, pedidos, mapsResponse, fecha) -> None:
        self.route_id = route_id
        self.nombreRuta = nombreRuta
        self.distancia = distancia
        self.tiempoEstimado = tiempoEstimado
        self.pedidos = pedidos
        self.mapsResponse = mapsResponse
        self.fecha = fecha

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
            mapsResponse=json.dumps(self.mapsResponse),
            fecha=self.fecha
        )


def parseMapsResponseToRoute(requestJson, mapsResponse):
    parsedResponse: TypedObject = parse_json(mapsResponse)[0]

    def getDistance(legs):
        return sum(leg.distance.value for leg in legs)

    def getDuration(legs):
        return sum(leg.duration.value for leg in legs)
    
    paradas = requestJson.get("paradas")

    parsedParadas = list(map(lambda parada: Pedido(
        clientes=[Cliente(
            cliente_id=parada.get("cliente").get("id", str(uuid.uuid4())),
            direccion=parada.get("cliente").get("direccion")
        )],
        fecha=parada.get("fecha"),
        nombre=parada.get("nombre"),
        pedido_id=parada.get("id", str(uuid.uuid4()))
    ),paradas))

    return Route(
        route_id=requestJson.get("id",(str(uuid.uuid4()))),
        nombreRuta=requestJson.get("nombre"),
        distancia=getDistance(parsedResponse.legs),
        tiempoEstimado=getDuration(parsedResponse.legs),
        pedidos=parsedParadas,
        mapsResponse=mapsResponse,
        fecha=parse_datetime_to_dd_mm_yyyy(datetime.datetime.now()),
    )

def parse_datetime_to_dd_mm_yyyy(dt):
    return dt.isoformat()
