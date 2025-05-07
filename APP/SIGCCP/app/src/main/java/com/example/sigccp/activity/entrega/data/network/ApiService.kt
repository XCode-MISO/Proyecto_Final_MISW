package com.example.sigccp.activity.entrega.data.network

import com.example.sigccp.activity.clients.data.model.Client
import com.example.sigccp.activity.entrega.data.model.Entrega
import retrofit2.http.GET
import retrofit2.http.Query

interface ApiService {
    //obtener pedidos del cliente pendientes (entregas)
    @GET("pedidos")
    suspend fun obtenerEntregas(@Query("clientid") clientId: String? = null): List<Entrega>
}