
import datetime
import json
from typing import List
import uuid
from logistica.infrastructure.maps.types import Leg, TypedObject
from logistica.infrastructure.maps.maps import parse_json
from logistica.infrastructure.db.model import Route as DBRoute, Parada as DBParada, Cliente as DBCliente, Vendedor as DBVendedor
import datetime

class Cliente():
    cliente_id = str
    direccion = str
    nombre = str
    
    def __init__(self, cliente_id, direccion, nombre) -> None:
        self.cliente_id = cliente_id
        self.direccion = direccion
        self.nombre = nombre
    
    def toJSON(self):
        return json.dumps(
                self,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4
            )

    def toDBO(self):
        return DBCliente(
            cliente_id=self.cliente_id,
            direccion=self.direccion,
            nombre=self.nombre
        )
    
class Vendedor():
    vendedor_id = str
    direccion = str
    nombre = str
    
    def __init__(self, vendedor_id, direccion, nombre) -> None:
        self.vendedor_id = vendedor_id
        self.direccion = direccion
        self.nombre = nombre
    
    def toJSON(self):
        return json.dumps(
                self,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4
            )

    def toDBO(self):
        return DBVendedor(
            vendedor_id=self.vendedor_id,
            direccion=self.direccion,
            nombre=self.nombre
        )


class Parada():
    parada_id = str
    nombre = str
    fecha = str
    cliente = Cliente
    vendedor = Vendedor

    def __init__(self, parada_id, nombre, fecha, cliente, vendedor) -> None:
        self.parada_id = parada_id
        self.nombre = nombre
        self.fecha = fecha
        self.cliente = cliente
        self.vendedor = vendedor

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    def toDBO(self):
        return DBParada(
            parada_id=self.parada_id,
            nombre=self.nombre,
            fecha=self.fecha,
            cliente=self.cliente.toDBO(),
            vendedor=self.vendedor.toDBO()
        )


class Route():
    route_id = str
    nombreRuta = str
    inicio = str
    fin = str
    distancia = float
    tiempoEstimado = int
    paradas= List[Parada]
    fecha = str
    mapsResponse= any

    def __init__(self, route_id, nombreRuta, distancia, tiempoEstimado, paradas, mapsResponse, fecha, inicio, fin) -> None:
        self.route_id = route_id
        self.nombreRuta = nombreRuta
        self.inicio = inicio
        self.fin = fin
        self.distancia = distancia
        self.tiempoEstimado = tiempoEstimado
        self.paradas = paradas
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
            inicio=self.inicio,
            fin=self.fin,
            distancia=self.distancia,
            tiempoEstimado=self.tiempoEstimado,
            paradas=list(map(lambda parada: parada.toDBO(), self.paradas)),
            mapsResponse=json.dumps(self.mapsResponse),
            fecha=self.fecha
        )


def parseMapsResponseToRoute(requestJson, mapsResponse):
    parsedResponse = next(iter(parse_json(mapsResponse) or []), TypedObject(bounds=[], legs=[]))

    def getDistance(legs):
        return sum(leg.distance.value for leg in legs)

    def getDuration(legs):
        return sum(leg.duration.value for leg in legs)
    
    paradas = requestJson.get("paradas")

    parsedParadas = list(map(lambda parada: Parada(
        cliente=Cliente(
            cliente_id=parada.get("cliente").get("id", str(uuid.uuid4())),
            direccion=parada.get("cliente").get("direccion"),
            nombre=parada.get("cliente").get("nombre")
        ),
        vendedor=Vendedor(
            vendedor_id=parada.get("vendedor").get("id", str(uuid.uuid4())),
            direccion=parada.get("vendedor").get("direccion"),
            nombre=parada.get("vendedor").get("nombre")
        ),
        fecha=parada.get("fecha"),
        nombre=parada.get("nombre"),
        parada_id=parada.get("id", str(uuid.uuid4()))
    ),paradas))

    return Route(
        route_id=requestJson.get("id",(str(uuid.uuid4()))),
        nombreRuta=requestJson.get("nombre"),
        distancia=getDistance(parsedResponse.legs),
        tiempoEstimado=getDuration(parsedResponse.legs),
        paradas=parsedParadas,
        mapsResponse=mapsResponse,
        fecha=parse_datetime_to_dd_mm_yyyy(datetime.datetime.now()),
        inicio=requestJson.get("inicio"),
        fin=requestJson.get("fin"),
    )

def parse_datetime_to_dd_mm_yyyy(dt):
    return dt.isoformat()
