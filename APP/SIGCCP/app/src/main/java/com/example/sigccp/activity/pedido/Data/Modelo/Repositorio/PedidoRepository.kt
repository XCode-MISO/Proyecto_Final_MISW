package com.example.sigccp.activity.pedido.Data.Repository

import com.example.sigccp.activity.pedido.Data.Modelo.PedidoClass
import com.example.sigccp.activity.pedido.Data.Modelo.PedidoRequest
import com.example.sigccp.activity.producto.Data.Modelo.ProductoClass
import com.example.sigccp.activity.pedido.Data.Modelo.ClienteClass
import com.example.sigccp.activity.pedido.Data.Network.PedidoService
import com.example.sigccp.activity.pedido.Data.Network.RetrofitInstancePedido

class PedidoRepository {
    var api: PedidoService = RetrofitInstancePedido.api

    suspend fun obtenerPedidos(clientId: String? = null): List<PedidoClass> =
        api.obtenerPedidos(clientId)

    suspend fun obtenerProductos(): List<ProductoClass> =
        api.obtenerProductos()

    suspend fun crearPedido(request: PedidoRequest) =
        api.createPedido(request)

    suspend fun obtenerClientes(): List<ClienteClass> =
        api.obtenerClientes()
}
