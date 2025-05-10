package com.example.sigccp.activity.route.Data.Modelo

data class RouteSimple(
    val routeId: String,
    val nombreRuta: String,
    val fecha: String
)

data class RouteFull(
    val routeId: String,
    val nombreRuta: String,
    val inicio: String,
    val fin: String,
    val distancia: Double,
    val tiempoEstimado: Int,
    val paradas: List<Parada>,
    val mapsResponse: String, // o usa un tipo más específico si tienes uno
    val fecha: String
)

data class Parada(
    val nombre: String,
    val fecha: String
)
