package com.example.sigccp.activity.route.Data.Network

import com.example.sigccp.utils.getOkHttpClientWithToken
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitInstanceRoute {
    val api: RouteService by lazy {
        Retrofit.Builder()
            .baseUrl("https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api/")
            .client(getOkHttpClientWithToken())
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(RouteService::class.java)
    }
}