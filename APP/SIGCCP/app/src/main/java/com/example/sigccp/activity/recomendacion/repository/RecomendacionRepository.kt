package com.example.sigccp.activity.recomendacion.repository

import com.example.sigccp.activity.recomendacion.data.network.RetrofitInstance
import okhttp3.MultipartBody
import okhttp3.ResponseBody
import retrofit2.Response

class RecomendacionRepository {
    val api = RetrofitInstance.api

    suspend fun uploadVideo(file: MultipartBody.Part): Response<ResponseBody> {
        return api.uploadVideo(file)
    }
}