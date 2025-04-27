package com.example.sigccp.activity.recomendacion.data.network

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitInstanceVideo {
    private const val BASE_URL = "https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/"

    val api: ApiServiceVideo by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiServiceVideo::class.java)
    }
}