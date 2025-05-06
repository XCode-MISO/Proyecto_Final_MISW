package com.example.sigccp.activity.entrega.ui.view

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sigccp.activity.entrega.data.model.Entrega
import com.example.sigccp.activity.entrega.repository.EntregaRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ListarEntregasViewModel:ViewModel() {
    private val repository = EntregaRepository()

    private val _entregas = MutableStateFlow<List<Entrega>>(emptyList())
    val entregas = _entregas.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading = _isLoading.asStateFlow()

    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage = _errorMessage.asStateFlow()

    fun fetchEntregas(clienteId: String){
        viewModelScope.launch {
            try {
                _isLoading.value = true
                _entregas.value = repository.getEntregas(clienteId)
            } catch (e: Exception) {
                _errorMessage.value = e.localizedMessage
            } finally {
                _isLoading.value = false
            }
        }
    }
}