package com.example.sigccp.activity.clients.data.model

data class VisitRequest(
    val client_id: String,
    val fechaVisita: String,
    val informe: String,
    val latitud: Double,
    val longitud: Double
)
