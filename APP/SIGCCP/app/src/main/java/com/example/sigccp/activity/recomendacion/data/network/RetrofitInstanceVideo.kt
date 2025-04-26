package com.example.sigccp.activity.recomendacion.data.network

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitInstanceVideo {
    val api: ApiServiceVideo by lazy {
        Retrofit.Builder()
            .baseUrl("https://api-video-upload-427368733403.us-central1.run.app/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiServiceVideo::class.java)
    }
}