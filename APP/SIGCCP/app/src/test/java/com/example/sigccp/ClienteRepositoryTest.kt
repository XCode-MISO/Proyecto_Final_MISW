package com.example.sigccp

import com.example.sigccp.activity.clients.data.model.Client
import com.example.sigccp.activity.clients.data.model.ClientPost
import com.example.sigccp.activity.clients.data.model.VisitRequest
import com.example.sigccp.activity.clients.data.network.ApiService
import com.example.sigccp.activity.clients.repository.ClienteRepository
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Test
import org.mockito.kotlin.mock
import org.mockito.kotlin.verify
import org.mockito.kotlin.whenever


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


}