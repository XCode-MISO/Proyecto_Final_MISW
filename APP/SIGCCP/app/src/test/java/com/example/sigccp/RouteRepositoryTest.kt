package com.example.sigccp

import com.example.sigccp.activity.route.Data.Modelo.RouteDetailResponse
import com.example.sigccp.activity.route.Data.Modelo.RouteSimple
import com.example.sigccp.activity.route.Data.Modelo.Parada
import com.example.sigccp.activity.route.Data.Modelo.Route
import com.example.sigccp.activity.route.Data.Network.RouteService
import com.example.sigccp.activity.route.repository.RouteRepository
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Test
import org.mockito.kotlin.*

class RouteRepositoryTest {
    private lateinit var repository: RouteRepository
    private lateinit var api: RouteService

    @Before
    fun setup() {
        api = mock()
        repository = RouteRepository()
        repository.api = api
    }

    @Test
    fun `obtenerTodasLasRutas debe llamar a api obtenerRoutes`() = runTest {
        // Given
        val mockRoutes = listOf<RouteSimple>()
        whenever(api.obtenerRoutes()).thenReturn(mockRoutes)

        // When
        repository.obtenerTodasLasRutas()

        // Then
        verify(api).obtenerRoutes()
    }

    @Test
    fun `obtenerRutaPorId debe llamar a api obtenerRoutePorId con id correcto`() = runTest {
        // Given
        val routeId = "123"
        val mockDetail = RouteDetailResponse(
            id = routeId,
            nombreRuta = "Ruta 1",
            distancia = 15.0f,
            inicio = "Inicio",
            fin = "Fin",
            tiempoEstimado = 30,
            paradas = listOf<Parada>(),
            mapsResponse = listOf<Route>(),
            fecha = "2023-10-01"
        )
        whenever(api.obtenerRoutePorId(routeId)).thenReturn(mockDetail)

        // When
        repository.obtenerRutaPorId(routeId)

        // Then
        verify(api).obtenerRoutePorId(eq(routeId))
    }
}
