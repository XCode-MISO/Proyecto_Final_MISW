package com.example.sigccp.activity.recomendacion.data.network

import com.example.sigccp.utils.getOkHttpClientWithToken
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitInstanceRecomendacion {
    private const val BASE_URL = "https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/"

    val apiService: ApiServiceRecomendacion by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(getOkHttpClientWithToken())
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiServiceRecomendacion::class.java)
    }
}
