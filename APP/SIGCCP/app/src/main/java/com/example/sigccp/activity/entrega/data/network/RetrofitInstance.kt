package com.example.sigccp.activity.entrega.data.network

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import com.example.sigccp.utils.getOkHttpClientWithToken

object RetrofitInstance {
    val api: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl("https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api/")
            .client(getOkHttpClientWithToken())
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}