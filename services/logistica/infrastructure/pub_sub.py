import json
import os
import queue

import requests
from logistica.application.services.generate_route import generate_route
from google.cloud import pubsub_v1

from logistica.domain.model import Route
from logistica.application.command.generate_route import MyException

class CreatePedidoEvent:
    def __init__(
        self,
        name,
        clientId,
        clientName,
        vendedorId,
        vendedorName,
        products,
        price,
        state,
        deliveryDate,
        createdAt,
    ) -> None:
        self.name = name
        self.clientId = clientId
        self.clientName = clientName
        self.vendedorId = vendedorId
        self.vendedorName = vendedorName
        self.products = products
        self.price = price
        self.state = state
        self.deliveryDate = deliveryDate
        self.createdAt = createdAt


class Cliente:
    def __init__(
        self,
        correo,
        direccion,
        id,
        latitud,
        longitud,
        nombre,
        telefono
    ) -> None:
        self.correo = correo
        self.direccion = direccion
        self.id = id
        self.latitud = latitud
        self.longitud = longitud
        self.nombre = nombre
        self.telefono = telefono


class Vendedor:
    def __init__(
        self,
        correo,
        direccion,
        id,
        latitud,
        longitud,
        nombre,
        telefono
    ) -> None:
        self.correo = correo
        self.direccion = direccion
        self.id = id
        self.latitud = latitud
        self.longitud = longitud
        self.nombre = nombre
        self.telefono = telefono


def publish_pedido_despachado(route: Route):
    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
        topic=os.getenv('PEDIDO_DESPACHADO_TOPIC')
    )
    future = publisher.publish(
        topic_name,
        data=route.toJSON().encode()
    )
    try:
        future.result()
    except:
        future.cancel()


def consume_pedido_creado(context):
    subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
        sub=os.getenv('PEDIDO_CREADO_SUB')
    )

    cola = queue.Queue()

    def callback(message):
        if cola.qsize() <= 3:
            cola.put(message)
            print("Se encoló el pedido\n")
            print(message)
            message.ack()
            return
        else:
            paradas = []
            with context:
                while not cola.empty():
                    pedido = cola.get()
                    try:
                        pedidoJson = json.loads(pedido.data)
                        parsedPedido = CreatePedidoEvent(
                            name=pedidoJson.get("name"),
                            clientId=pedidoJson.get("client").get("id"),
                            clientName=pedidoJson.get("client").get("name"),
                            vendedorId=pedidoJson.get("vendedor").get("id"),
                            vendedorName=pedidoJson.get("vendedor").get("name"),
                            products=pedidoJson.get("products"),
                            price=pedidoJson.get("price"),
                            state=pedidoJson.get("state"),
                            deliveryDate=pedidoJson.get("deliveryDate"),
                            createdAt=pedidoJson.get("createdAt"),
                        )

                        response = requests.get(
                            f'http://ventas.default.svc.cluster.local/api/vendedores/{parsedPedido.clientId}')
                        print(response)
                        responseJson = response.json()
                        cliente = Cliente(
                            correo=responseJson.get("correo"),
                            direccion=responseJson.get("direccion"),
                            id=responseJson.get("id"),
                            latitud=responseJson.get("latitud"),
                            longitud=responseJson.get("longitud"),
                            nombre=responseJson.get("nombre"),
                            telefono=responseJson.get("telefono")
                        )

                        response = requests.get(
                            f'http://ventas.default.svc.cluster.local/api/vendedores/{parsedPedido.vendedorId}')
                        print(response)
                        responseJson = response.json()
                        vendedor = Vendedor(
                            correo=responseJson.get("correo"),
                            direccion=responseJson.get("direccion"),
                            id=responseJson.get("id"),
                            latitud=responseJson.get("latitud"),
                            longitud=responseJson.get("longitud"),
                            nombre=responseJson.get("nombre"),
                            telefono=responseJson.get("telefono")
                        )
                        paradas.append({
                            "nombre": parsedPedido.vendedorName,
                            "fecha": parsedPedido.deliveryDate,
                            "cliente": {
                                "nombre": parsedPedido.clientName,
                                "direccion": [cliente.latitud, cliente.longitud]
                            },
                            "vendedor": {
                                "nombre": parsedPedido.vendedorName,
                                "direccion": [vendedor.latitud, vendedor.longitud]
                            }
                        })
                    except MyException as e: 
                        print(e.as_http_error())
                        return e.as_http_error()
                    
                print("Started route")
                print("cola size", cola.qsize())
                print("cola empty", cola.not_empty)
                route = generate_route({
                    "nombre": parsedPedido.name,
                    "inicio": [cliente.latitud, cliente.longitud],
                    "fin": [cliente.latitud, cliente.longitud],
                    "paradas": paradas
                })
                print("Se finalizo el pedido\n")
                print("paradas len: ", len(paradas))
                # print(route.toJSON() + "\n")
                # publish_pedido_despachado(route)
                pedido.ack()

    with pubsub_v1.SubscriberClient() as subscriber:
        print(f'Subscribed succesfully to :{subscription_name}')
        future = subscriber.subscribe(subscription_name, callback)
        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()
