package com.example.sigccp

import com.example.sigccp.activity.entrega.data.model.Entrega
import com.example.sigccp.activity.entrega.data.network.ApiService
import com.example.sigccp.activity.entrega.repository.EntregaRepository
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Test
import org.mockito.kotlin.mock
import org.mockito.kotlin.verify
import org.mockito.kotlin.whenever

class EntregasTests {
    private lateinit var repository: EntregaRepository
    private lateinit var api: ApiService

    @Before
    fun setup() {
        api = mock()
        repository = EntregaRepository()
        repository.api = api
    }

    @Test
    fun `obtenerEntregas should call api getEntregas`() = runTest {
        // Given
        val mockEntregas = listOf<Entrega>()
        whenever(api.obtenerEntregas()).thenReturn(mockEntregas)
        val clientId = "idCliente"
        // When
        repository.getEntregas(clientId)
        // Then
        verify(api).obtenerEntregas(clientId)
    }

    @Test
    fun `obtenerEntregas should return list of entregas`() = runTest {
        // Given
        val mockEntregas = listOf(Entrega("idCliente", "Pedido1", "Cliente1", 20.00, "Estado1"))
        whenever(api.obtenerEntregas("idCliente")).thenReturn(mockEntregas)
        val clientId = "idCliente"
        // When
        val result = repository.getEntregas(clientId)
        // Then
        assert(result == mockEntregas)
    }

    @Test
    fun `obtenerEntregas should handle empty list`() = runTest {
        // Given
        val mockEntregas = emptyList<Entrega>()
        whenever(api.obtenerEntregas("idCliente")).thenReturn(mockEntregas)
        val clientId = "idCliente"
        // When
        val result = repository.getEntregas(clientId)
        // Then
        assert(result.isEmpty())
    }
}