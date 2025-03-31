package com.example.sigccp.activity.pedido.Data.Network

import com.example.sigccp.activity.pedido.Data.Modelo.DataItemPedido
import retrofit2.http.GET
import retrofit2.http.Path

//cliente que cosume  el servicio
interface ApiServicePedido {
    @GET("pedido")
    suspend fun getPedidos(): List<DataItemPedido>

    @GET("pedido/{pedidoId}")
    suspend fun getPedidoId(@Path("pedidoId") pedidoId:String):DataItemPedido
}
