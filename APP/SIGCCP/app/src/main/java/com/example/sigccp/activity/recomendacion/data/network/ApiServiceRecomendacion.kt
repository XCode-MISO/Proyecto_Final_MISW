package com.example.sigccp.activity.recomendacion.data.network

import com.example.sigccp.activity.recomendacion.data.model.StatusResponse
import retrofit2.http.GET
import retrofit2.http.Query

interface ApiServiceRecomendacion {
    @GET("api/recommend")
    suspend fun getJobStatus(@Query("job_id") jobId: String): StatusResponse
}
