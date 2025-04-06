package com.example.sigccp.activity.clients.repository

import com.example.sigccp.activity.clients.data.model.Client
import com.example.sigccp.activity.clients.data.model.ClientPost
import com.example.sigccp.activity.clients.data.model.VisitRequest
import com.example.sigccp.activity.clients.data.network.RetrofitInstance

class ClienteRepository {
    var api = RetrofitInstance.api

    suspend fun getClientes(): List<Client> = api.getClients()

    suspend fun postCliente(request: ClientPost) = api.postClient(request)

    suspend fun sendVisit(request: VisitRequest) = api.sendVisit(request)
}