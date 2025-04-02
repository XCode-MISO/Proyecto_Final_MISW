package com.example.sigccp.activity.clients.data.network

import com.example.sigccp.activity.clients.data.model.Client
import com.example.sigccp.activity.clients.data.model.VisitRequest
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiService {
    @GET("clients")
    suspend fun getClients(): List<Client>

    @POST("visits")
    suspend fun sendVisit(@Body request: VisitRequest): Response<Unit>
}