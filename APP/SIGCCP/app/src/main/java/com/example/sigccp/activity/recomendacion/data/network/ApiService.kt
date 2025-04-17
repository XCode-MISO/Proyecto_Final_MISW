package com.example.sigccp.activity.recomendacion.data.network

import okhttp3.MultipartBody
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

interface ApiService {
    @Multipart
    @POST("api/upload")
    suspend fun uploadVideo(
        @Part file: MultipartBody.Part
    ): Response<ResponseBody>
}