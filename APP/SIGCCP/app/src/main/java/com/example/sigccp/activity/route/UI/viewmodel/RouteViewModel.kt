package com.example.sigccp.activity.route.UI.viewmodel

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sigccp.activity.pedido.Data.Modelo.ProductoCantidad
import com.example.sigccp.activity.route.Data.Modelo.Leg
import com.example.sigccp.activity.route.Data.Modelo.Parada
import com.example.sigccp.activity.route.Data.Modelo.RouteSimple
import com.example.sigccp.activity.route.Data.Modelo.RouteDetailResponse
import com.example.sigccp.activity.route.Data.Network.RetrofitInstanceRoute
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class RouteViewModel  : ViewModel() {

    private val _routes = MutableStateFlow<List<RouteSimple>>(emptyList())
    val routes: StateFlow<List<RouteSimple>> = _routes
    private val _detalleRuta = MutableStateFlow<RouteDetailResponse?>(null)
    val detalleRuta: StateFlow<RouteDetailResponse?> = _detalleRuta

    init {
        fetchRoutes()
    }

    fun fetchRouteDetail(routeId: String) {
        viewModelScope.launch {
            try {
                val response = RetrofitInstanceRoute.api.obtenerRoutePorId(routeId)

                // Asignar duraciones solo si hay legs y paradas
                val paradasConDuracion = if (response.mapsResponse.isNotEmpty()) {
                    val legs = response.mapsResponse[0].legs
                    asignarDuraciones(response.paradas, legs)
                } else {
                    response.paradas
                }

                // Crear una copia de la respuesta con las paradas actualizadas
                val nuevaRespuesta = response.copy(paradas = paradasConDuracion)

                _detalleRuta.value = nuevaRespuesta
                Log.d("DEBUG_ROUTE", "Ruta recibida: $response")
            } catch (e: Exception) {
                Log.e("DEBUG_ROUTE", "Error: ${e.localizedMessage}", e)
                e.printStackTrace()
            }
        }
    }
    fun asignarDuraciones(paradas: List<Parada>, legs: List<Leg>): List<Parada> {
        var legIndex = 0
        return paradas.mapIndexed { index, parada ->
            val leg: Leg? = when {
                index == 0 -> {
                    // Siempre asignar el primer leg (punto de partida)
                    legs.getOrNull(0)
                }
                else -> {
                    // Buscar el siguiente leg con duración > 0
                    var nextValidLeg: Leg? = null
                    while (legIndex + 1 < legs.size) {
                        legIndex++
                        val candidate = legs[legIndex]
                        if (candidate.duration.value > 0) {
                            nextValidLeg = candidate
                            break
                        }
                    }
                    nextValidLeg
                }
            }
            parada.copy(duration = leg?.duration)
        }
    }

    fun fetchRoutes() {
        viewModelScope.launch {
            try {
                _routes.value = RetrofitInstanceRoute.api.obtenerRoutes()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}