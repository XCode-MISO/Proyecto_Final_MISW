package com.example.sigccp

import com.example.sigccp.activity.pedido.Data.Modelo.*
import com.example.sigccp.activity.pedido.Data.Network.PedidoService
import com.example.sigccp.activity.pedido.Data.Repository.PedidoRepository
import com.example.sigccp.activity.producto.Data.Modelo.ProductoClass
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Test
import org.mockito.kotlin.*

class PedidosTests {

    private lateinit var repository: PedidoRepository
    private lateinit var api: PedidoService

    @Before
    fun setup() {
        api = mock()
        repository = PedidoRepository()
        repository.api = api
    }

    @Test
    fun `obtenerPedidos should call api with null clientId`() = runTest {
        // Given
        val mockPedidos = listOf<PedidoClass>()
        whenever(api.obtenerPedidos(null)).thenReturn(mockPedidos)

        // When
        repository.obtenerPedidos()

        // Then
        verify(api).obtenerPedidos(null)
    }

    @Test
    fun `obtenerPedidos should call api with a specific clientId`() = runTest {
        // Given
        val clientId = "123"
        val mockPedidos = listOf<PedidoClass>()
        whenever(api.obtenerPedidos(clientId)).thenReturn(mockPedidos)

        // When
        repository.obtenerPedidos(clientId)

        // Then
        verify(api).obtenerPedidos(eq(clientId))
    }

    @Test
    fun `obtenerProductos should call api obtenerProductos`() = runTest {
        // Given
        val mockProductos = listOf<ProductoClass>()
        whenever(api.obtenerProductos()).thenReturn(mockProductos)

        // When
        repository.obtenerProductos()

        // Then
        verify(api).obtenerProductos()
    }

    @Test
    fun `crearPedido should call api createPedido with correct request`() = runTest {
        // Given
        val pedidoRequest = PedidoRequest(
            name = "Pedido Test",
            clientId = "1",
            clientName = "Cliente Uno",
            vendedorId = "10",
            vendedorName = "Vendedor Uno",
            products = listOf(ProductoCantidad(id = 1, amount = 2)),
            price = 100.0f,
            state = "pendiente",
            deliveryDate = "2025-05-15"
        )
        // When
        repository.crearPedido(pedidoRequest)

        // Then
        verify(api).createPedido(eq(pedidoRequest))
    }

    @Test
    fun `obtenerClientes should call api obtenerClientes`() = runTest {
        // Given
        val mockClientes = listOf<ClienteClass>()
        whenever(api.obtenerClientes()).thenReturn(mockClientes)

        // When
        repository.obtenerClientes()

        // Then
        verify(api).obtenerClientes()
    }
}
