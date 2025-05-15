package com.example.sigccp.activity.route.UI.view

import android.util.Log
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.sigccp.R
import com.example.sigccp.activity.route.Data.Modelo.Parada
import com.example.sigccp.activity.route.UI.viewmodel.RouteViewModel
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.navigation.NavigationController
import com.example.sigccp.ui.View.Components.CampoFecha
import com.example.sigccp.ui.View.Components.ListaDeParadas
import com.example.sigccp.ui.View.Components.MapaRuta
import com.example.sigccp.ui.View.Components.ScreenContainer
import java.time.LocalDate
import java.time.format.DateTimeFormatter


@Composable
fun RouteDetail(routeId: String, viewModel: RouteViewModel = viewModel()) {
    val navController = NavigationController.navController
    BackHandler {
        navController.navigate(AppScreen.ListarRutas.route) {
            popUpTo(0)
        }
    }
    val routeDate = "11/05/2025"
    val detalleRuta = viewModel.detalleRuta.collectAsState().value
    val fechaFormateada = if (detalleRuta != null) {
        try {
            LocalDate.parse(detalleRuta.fecha.substring(0, 10))
                .format(DateTimeFormatter.ofPattern("dd/MM/yyyy"))
        } catch (e: Exception) {
            detalleRuta.fecha // fallback en caso de error
        }
    } else {
        routeDate // Valor por defecto si detalleRuta es null
    }
    LaunchedEffect(routeId) {
        viewModel.fetchRouteDetail(routeId)
    }
    /*val paradasEjemplo = listOf(
        Parada(nombre = "Parque Central", minutos = 5, cliente = "Juan Pérez"),
        Parada(nombre = "Estación Norte", minutos = 10, cliente = "Distribuciones Gómez"),
        Parada(nombre = "Zona Industrial", minutos = 8, cliente = "Ferretería Central"),
        Parada(nombre = "Centro Comercial", minutos = 12, cliente = "Súper Tienda LA 14"),
        Parada(nombre = "Barrio El Prado", minutos = 6, cliente = "Doña Marta"),
    )*/
    val routes = viewModel.routes.collectAsState().value
    val context = LocalContext.current

    ScreenContainer(
        title = stringResource(id = R.string.Route),
        true,
        false,
        true,
        null,
        AppScreen.ListarRutas.route
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize(), // Ocupa toda la pantalla para centrar el contenido
            contentAlignment = Alignment.Center // Centra el contenido en la pantalla
        )
        {
            Column(
                modifier = Modifier
                    .fillMaxSize(),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            )
            {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .wrapContentSize(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.Top
                )
                {
                    Column(
                        modifier = Modifier
                            .width(300.dp),
                        verticalArrangement = Arrangement.Center,
                        horizontalAlignment = Alignment.CenterHorizontally
                    )
                    {
                    }
                }
                Row(
                    modifier = Modifier
                        .fillMaxSize(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                )
                {
                    Column(
                        modifier = Modifier
                            .width(300.dp)
                            .padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    )
                    {
                        if (detalleRuta != null) {

                            CampoFecha(fechaFormateada)
                            MapaRuta(detalleRuta.mapsResponse)
                            Log.d("DEBUG_ROUTE", "MapsResponse size: ${detalleRuta.mapsResponse.size}")
                            ListaDeParadas(detalleRuta.paradas.map {

                                Parada(nombre = it.nombre, duration = it.duration, cliente = it.cliente)

                            })

                        } else {
                            CircularProgressIndicator()
                        }


                        //CampoFecha(routeDate)
                        //ListaDeParadas(paradasEjemplo)
                    }
                }
            }
        }
    }
}

