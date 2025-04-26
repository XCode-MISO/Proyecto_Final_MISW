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
    //obtener todos los pedidos
    @GET("pedidos")
    suspend fun obtenerPedidos(): List<PedidoClass>

    // obtener productos
    @GET("inventarios/pedidos")
    suspend fun obtenerProductos(): List<ProductoClass>

    // Crear pedido
    @POST("pedidos/create_pedido")
    suspend fun createPedido(@Body pedido: PedidoRequest): Response<Unit>

    //obtener todos los clientes
    @GET("clients")
    suspend fun obtenerClientes(): List<ClienteClass>

}
