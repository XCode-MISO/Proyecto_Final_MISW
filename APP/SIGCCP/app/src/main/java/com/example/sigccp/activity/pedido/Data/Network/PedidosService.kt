package com.example.sigccp.activity.pedido.Data.Network

import com.example.sigccp.activity.pedido.Data.Modelo.PedidoClass
import com.example.sigccp.activity.producto.Data.Modelo.ProductoClass
import retrofit2.http.GET

interface PedidoService {
    @GET("/pedidos") // reemplaza por la ruta real
    suspend fun obtenerPedidos(): List<PedidoClass>

    @GET("/productos")
    suspend fun obtenerProductos(): List<ProductoClass>
}
