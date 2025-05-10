package com.example.sigccp.activity.route.Data.Network

import com.example.sigccp.activity.route.Data.Modelo.RouteSimple
import retrofit2.http.GET
import retrofit2.http.Path


interface RouteService {
    // Obtener todas las rutas
    @GET("route")
    suspend fun obtenerRoutes(): List<RouteSimple>

    // Obtener ruta por ID
    @GET("route/{id}")
    suspend fun obtenerRoutePorId(@Path("id") id: String): RouteSimple
}