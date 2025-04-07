package com.example.sigccp.activity.pedido.Data.Network

import com.example.sigccp.activity.pedido.Data.Modelo.ClienteClass
import com.example.sigccp.activity.pedido.Data.Modelo.PedidoClass
import com.example.sigccp.activity.pedido.Data.Modelo.PedidoRequest
import com.example.sigccp.activity.producto.Data.Modelo.ProductoClass
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface PedidoService {
    @GET("/pedidos") // reemplaza por la ruta real
    suspend fun obtenerPedidos(): List<PedidoClass>

    @GET("/productos")
    suspend fun obtenerProductos(): List<ProductoClass>

    @POST("/create_pedido")
    suspend fun createPedido(@Body pedido: PedidoRequest): Response<Unit>

    @GET("/clientes")
    suspend fun obtenerClientes(): List<ClienteClass>

}
