package com.example.sigccp

import com.example.sigccp.activity.clients.data.model.Client
import com.example.sigccp.activity.clients.data.model.ClientPost
import com.example.sigccp.activity.clients.data.model.VisitRequest
import com.example.sigccp.activity.clients.data.network.ApiService
import com.example.sigccp.activity.clients.repository.ClienteRepository
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Test
import org.mockito.kotlin.mock
import org.mockito.kotlin.verify
import org.mockito.kotlin.whenever
import org.mockito.kotlin.eq

class ClienteRepositoryTest {
    private lateinit var repository: ClienteRepository
    private lateinit var api: ApiService

    @Before
    fun setup() {
        api = mock()
        repository = ClienteRepository()
        repository.api = api
    }

    @Test
    fun `getClientes should call api getClients`() = runTest {
        // Given
        val mockClients = listOf<Client>()
        whenever(api.getClients()).thenReturn(mockClients)
        // When
        repository.getClientes()
        // Then
        verify(api).getClients()
    }

    @Test
    fun `postCliente should call api postClient with correct data`() = runTest {
        // Given
        val mockRequest = ClientPost(
            nombre = "Test Name",
            correo = "test@email.com",
            direccion = "Test Last Name",
            telefono = "1234567890",
            latitud = 0.0,
            longitud = 0.0
        )
        // When
        repository.postCliente(mockRequest)
        // Then
        verify(api).postClient(eq(mockRequest))
    }

    @Test
    fun `sendVisit should call api sendVisit with correct data`() = runTest {
        // Given
        val mockRequest = VisitRequest(
            client_id = "id",
            fechaVisita = "2023-05-15",
            informe = "informe de visita",
            latitud = 0.0,
            longitud = 0.0
        )
        // When
        repository.sendVisit(mockRequest)
        // Then
        verify(api).sendVisit(eq(mockRequest))
    }
}