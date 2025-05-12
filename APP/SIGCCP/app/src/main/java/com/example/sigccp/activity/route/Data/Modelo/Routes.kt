package com.example.sigccp.activity.route.Data.Modelo
import com.google.gson.annotations.SerializedName
import java.time.LocalDate
import java.time.format.DateTimeFormatter

data class RouteSimple(
    @SerializedName("id") val routeId: String,
    val nombreRuta: String,
    val fecha: String
)

data class MapsResponse(
    val polyline: String // Ajusta según estructura real del JSON
)

data class RouteDetailResponse(
    val id: String,
    val nombreRuta: String?,
    val distancia: Float,
    val inicio: String,
    val fin: String,
    val tiempoEstimado: Int?,
    val paradas: List<Parada>,
    val mapsResponse: List<Route>,
    val fecha: String
)


data class Route(
    val bounds: Bounds,
    val legs: List<Leg>,
    val copyrights: String? = null
)

data class Bounds(
    val northeast: LatLng,
    val southwest: LatLng
)

data class LatLng(
    val lat: Double,
    val lng: Double
)

data class Leg(
    val steps: List<Step>,
    val duration: Duracion
)

data class Step(
    val polyline: Polyline,
)

data class Polyline(
    val points: String
)

data class Parada(
    val nombre: String,
    val duration: Duracion? = null,
    val cliente: Cliente
)

data class Cliente(
    val nombre: String,
    val codigo: String
)
data class Duracion(
    val text: String,
    val value: Int
)