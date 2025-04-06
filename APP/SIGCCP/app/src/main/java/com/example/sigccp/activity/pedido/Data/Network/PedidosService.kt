package com.example.sigccp.activity.pedido.Data.Network

import com.example.sigccp.activity.pedido.Data.Modelo.PedidoClass
import retrofit2.http.GET

interface PedidoService {
    @GET("/pedidos") // reemplaza por la ruta real
    suspend fun obtenerPedidos(): List<PedidoClass>
}
