package com.example.sigccp.activity.pedido.UI.ViewModel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sigccp.activity.pedido.Data.Network.ApiServicePedido
import com.example.sigccp.activity.pedido.Data.Modelo.DataItemPedido
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class PedidoViewModel @Inject constructor
    (
        private val apiService: ApiServicePedido
    ): ViewModel()
{
    private val _pedidos = MutableStateFlow<List<DataItemPedido>>(emptyList())
    val pedidos: StateFlow<List<DataItemPedido>> get() =_pedidos

    init {
        getPedidos()
    }

    private fun getPedidos() {
        viewModelScope.launch {
            try
            {
                _pedidos.value = apiService.getPedidos()
            }
            catch (e:Exception)
            {
                e.printStackTrace() // Manejo de error
            }

        }
    }
}
