package com.example.sigccp.activity.route.repository

import com.example.sigccp.activity.route.Data.Modelo.RouteDetailResponse
import com.example.sigccp.activity.route.Data.Modelo.RouteSimple
import com.example.sigccp.activity.route.Data.Network.RouteService
import com.example.sigccp.activity.route.Data.Network.RetrofitInstanceRoute

class RouteRepository {
    var api: RouteService = RetrofitInstanceRoute.api

    suspend fun obtenerTodasLasRutas(): List<RouteSimple> {
        return api.obtenerRoutes()
    }

    suspend fun obtenerRutaPorId(id: String): RouteDetailResponse {
        return api.obtenerRoutePorId(id)
    }
}
