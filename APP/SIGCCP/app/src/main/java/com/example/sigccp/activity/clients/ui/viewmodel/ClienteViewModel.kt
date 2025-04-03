package com.example.sigccp.activity.clients.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sigccp.activity.clients.data.model.Client
import com.example.sigccp.activity.clients.data.model.ClientPost
import com.example.sigccp.activity.clients.data.model.VisitRequest
import com.example.sigccp.activity.clients.repository.ClienteRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class ClienteViewModel: ViewModel() {
    private val repository = ClienteRepository()

    private val _clientes = MutableStateFlow<List<Client>>(emptyList())
    val clientes = _clientes.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading = _isLoading.asStateFlow()

    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage = _errorMessage.asStateFlow()

    fun fetchClientes() {
        viewModelScope.launch {
            try {
                _isLoading.value = true
                _clientes.value = repository.getClientes()
            } catch (e: Exception) {
                _errorMessage.value = e.localizedMessage
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun sendVisit(idCliente: String, informe: String, onSuccess: () -> Unit, onError: (String) -> Unit) {
        viewModelScope.launch {
            _isLoading.value = true
            val fechaHora = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault()).format(Date())

            try {
                val response = repository.sendVisit(VisitRequest(idCliente, fechaHora, informe, 0.0, 0.0))
                if (response.isSuccessful) {
                    onSuccess()
                } else {
                    onError("Error en el envío: ${response.errorBody()?.string()}")
                }
            } catch (e: Exception) {
                onError(e.localizedMessage ?: "Error desconocido")
            } finally {
                _isLoading.value = false
            }
        }
    }
/**************************************************************************************************/
    fun createClient(nombre: String, correo: String, direccion: String, telefono: String, latitud: Double, longitud: Double, onSuccess: () -> Unit, onError: (String) -> Unit) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = repository.postCliente(ClientPost(nombre, correo, direccion, telefono, latitud, longitud))
                if (response.isSuccessful) {
                    onSuccess()
                } else {
                    onError("Error en el envío: ${response.errorBody()?.string()}")
                }
            } catch (e: Exception) {
                onError(e.localizedMessage ?: "Error desconocido")
            } finally {
                _isLoading.value = false
            }
        }
    }
/**************************************************************************************************/
}