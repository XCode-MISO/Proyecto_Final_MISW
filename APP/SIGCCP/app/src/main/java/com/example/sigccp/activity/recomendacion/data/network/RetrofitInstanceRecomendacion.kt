package com.example.sigccp.activity.recomendacion.data.network

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitInstanceRecomendacion {
    private const val BASE_URL = "https://api-recomendaciones-427368733403.us-central1.run.app/"

    val apiService: ApiServiceRecomendacion by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiServiceRecomendacion::class.java)
    }
}
