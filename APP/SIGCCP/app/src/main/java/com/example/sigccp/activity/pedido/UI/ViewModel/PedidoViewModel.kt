package com.example.sigccp.activity.pedido.UI.ViewModel

import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sigccp.activity.pedido.Data.Modelo.PedidoClass
import com.example.sigccp.activity.pedido.Data.Network.RetrofitInstancePedido
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import androidx.compose.runtime.State
import com.example.sigccp.activity.producto.Data.Modelo.ProductoClass
import com.example.sigccp.activity.producto.Data.Modelo.ProductosPedidoClass
import java.time.LocalDate
import java.time.format.DateTimeFormatter


class PedidoViewModel : ViewModel() {

    val nombrePedido = mutableStateOf("Pedido #${(1..9999).random()}")
    val clienteId = mutableStateOf("")
    val precioTotal = mutableStateOf(0.0)
    val estado = mutableStateOf("Pendiente")

    val deliveryDate: String = LocalDate.now().plusDays(1).format(DateTimeFormatter.ISO_LOCAL_DATE)

    private val _pedidos = MutableStateFlow<List<PedidoClass>>(emptyList())
    val pedidos: StateFlow<List<PedidoClass>> = _pedidos

    // Productos seleccionados (con cantidades y validación)
    private val _productosSeleccionados = mutableStateOf<List<ProductosPedidoClass>>(emptyList())
    val productosSeleccionados: State<List<ProductosPedidoClass>> = _productosSeleccionados

    private val _productosDisponibles = mutableStateOf<List<ProductoClass>>(emptyList())
    val productosDisponibles: State<List<ProductoClass>> = _productosDisponibles

    fun actualizarProductosSeleccionados(productos: List<ProductosPedidoClass>) {
        val productosValidados = productos.map { producto ->
            val esValida = producto.cantidadRequerida <= producto.cantidadDisponible
            val total = producto.precioUnitario * producto.cantidadRequerida
            producto.copy(
                cantidadEsValida = esValida,
                precioTotal = total
            )
        }
        _productosSeleccionados.value = productosValidados
    }


    init {
        fetchPedidos()
        fetchProductos()
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
    private fun fetchProductos() {
        viewModelScope.launch {
            try {
                val response = RetrofitInstancePedido.api.obtenerProductos()
                _productosDisponibles.value = response
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }


}
