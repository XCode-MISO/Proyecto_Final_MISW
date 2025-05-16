package com.example.sigccp.activity.pedido.Data.Network

import com.example.sigccp.utils.getOkHttpClientWithToken
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitInstancePedido {
    val api: PedidoService by lazy {
        Retrofit.Builder()
            .baseUrl("https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api/")
            .client(getOkHttpClientWithToken())
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(PedidoService::class.java)
    }
}