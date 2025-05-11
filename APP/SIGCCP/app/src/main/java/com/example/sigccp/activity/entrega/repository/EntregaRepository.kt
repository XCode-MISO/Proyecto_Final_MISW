package com.example.sigccp.activity.entrega.repository

import com.example.sigccp.activity.entrega.data.model.Entrega
import com.example.sigccp.activity.entrega.data.network.RetrofitInstance


class EntregaRepository {
    var api = RetrofitInstance.api

    suspend fun getEntregas(clienteId: String): List<Entrega> = api.obtenerEntregas(clienteId)

}