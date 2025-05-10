package com.example.sigccp.activity.route.UI.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sigccp.activity.pedido.Data.Modelo.ProductoCantidad
import com.example.sigccp.activity.route.Data.Modelo.RouteSimple
import com.example.sigccp.activity.route.Data.Network.RetrofitInstanceRoute
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class RouteViewModel  : ViewModel() {

    private val _routes = MutableStateFlow<List<RouteSimple>>(emptyList())
    val routes: StateFlow<List<RouteSimple>> = _routes

    init {
        fetchRoutes()
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