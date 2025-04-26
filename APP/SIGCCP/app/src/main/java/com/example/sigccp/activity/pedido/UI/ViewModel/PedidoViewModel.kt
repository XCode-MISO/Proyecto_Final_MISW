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
import com.example.sigccp.PreferenceKeys
import com.example.sigccp.PreferencesManager
import com.example.sigccp.activity.pedido.Data.Modelo.ClienteClass
import com.example.sigccp.activity.pedido.Data.Modelo.PedidoRequest
import com.example.sigccp.activity.pedido.Data.Modelo.ProductoCantidad
import com.example.sigccp.activity.producto.Data.Modelo.ProductoClass
import com.example.sigccp.activity.producto.Data.Modelo.ProductosPedidoClass
import java.time.LocalDate
import java.time.format.DateTimeFormatter


class PedidoViewModel : ViewModel() {
    private val _clientes = mutableStateOf<List<ClienteClass>>(emptyList())
    val clientes: State<List<ClienteClass>> = _clientes

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
        precioTotal.value = productosValidados.sumOf { it.precioTotal.toDouble() }
    }


    init {
        fetchPedidos()
        fetchProductos()
        fetchClientes()
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
    fun crearPedido(onSuccess: () -> Unit, onError: (Throwable) -> Unit) {
        viewModelScope.launch {
            try {
                val productos = productosSeleccionados.value.map {
                    ProductoCantidad(
                        id = it.id,
                        amount = it.cantidadRequerida
                    )
                }
                val role = PreferencesManager.getString(PreferenceKeys.ROLE)
                val userId = PreferencesManager.getString(PreferenceKeys.USER_ID)
                val userName = PreferencesManager.getString(PreferenceKeys.USER_NAME)

                val clientIdValue: String
                val clientNameValue: String
                val vendedorIdValue: String
                val vendedorNameValue: String

                if (role == "vendedor") {
                    // Si es vendedor, el cliente y el vendedor son el usuario actual
                    clientIdValue = userId ?: ""
                    clientNameValue = userName ?: ""
                    vendedorIdValue = userId ?: ""
                    vendedorNameValue = userName ?: ""
                } else {
                    // Si no es vendedor, usa el cliente seleccionado y el usuario actual como vendedor
                    clientIdValue = clienteId.value
                    clientNameValue = clientes.value.find { it.id == clienteId.value }?.nombre ?: ""
                    vendedorIdValue = userId ?: ""
                    vendedorNameValue = userName ?: ""
                }

                val pedido = PedidoRequest(
                    name = nombrePedido.value,
                    clientId = clientIdValue,
                    clientName = clientNameValue,
                    vendedorId = vendedorIdValue,
                    vendedorName = vendedorNameValue,
                    products = productos,
                    price = precioTotal.value,
                    state = estado.value,
                    deliveryDate = deliveryDate
                )

                println("Enviando pedido: $pedido")

                val response = RetrofitInstancePedido.api.createPedido(pedido)

                println("Respuesta: ${response.code()}")

                if (response.isSuccessful) {
                    onSuccess()
                } else {
                    throw Exception("Error del servidor: ${response.code()} - ${response.errorBody()?.string()}")
                }
            } catch (e: Exception) {
                println("Error en crearPedido: ${e.localizedMessage}")
                onError(e)
            }
        }
    }

    private fun fetchClientes() {
        viewModelScope.launch {
            try {
                val response = RetrofitInstancePedido.api.obtenerClientes()
                _clientes.value = response
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
    fun limpiarPedido() {
        clienteId.value = ""
        _productosSeleccionados.value = emptyList()
        nombrePedido.value = "Pedido #${(1..9999).random()}"
        precioTotal.value = 0.0
    }


}
