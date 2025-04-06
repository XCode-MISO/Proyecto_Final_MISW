package com.example.sigccp.activity.pedido.Data.Network

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitInstancePedido {
    val api: PedidoService by lazy {
        Retrofit.Builder()
            .baseUrl("http://192.168.10.89:3001")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(PedidoService::class.java)
    }
}