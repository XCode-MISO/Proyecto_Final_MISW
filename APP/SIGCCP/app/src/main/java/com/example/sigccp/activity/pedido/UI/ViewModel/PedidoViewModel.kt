package com.example.sigccp.activity.pedido.UI.ViewModel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sigccp.activity.pedido.Data.Modelo.PedidoClass
import com.example.sigccp.activity.pedido.Data.Network.RetrofitInstancePedido
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class PedidoViewModel : ViewModel() {

    private val _pedidos = MutableStateFlow<List<PedidoClass>>(emptyList())
    val pedidos: StateFlow<List<PedidoClass>> = _pedidos

    init {
        fetchPedidos()
    }

    private fun fetchPedidos() {
        viewModelScope.launch {
            try {
                val response = RetrofitInstancePedido.api.obtenerPedidos()
                _pedidos.value = response
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}
