package com.example.sigccp.activity.route.UI.view

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
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.sigccp.R
import com.example.sigccp.activity.route.UI.viewmodel.RouteViewModel
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.navigation.NavigationController
import com.example.sigccp.ui.View.Components.ScreenContainer
import android.app.DatePickerDialog
import android.widget.DatePicker
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import com.example.sigccp.activity.route.Data.Modelo.RouteSimple
import com.example.sigccp.ui.View.Components.ListaDeRutas
import com.example.sigccp.ui.theme.AppTypography
import com.example.sigccp.ui.theme.MoradoApp
import java.util.*

@Composable
fun ListarRutas()
{
    RoutesList()
}

@Composable
fun RoutesList(viewModel: RouteViewModel = viewModel()) {
    val navController = NavigationController.navController
    BackHandler {
        navController.navigate(AppScreen.Menu.route){
            popUpTo(0)
        }
    }

    val routes=viewModel.routes.collectAsState().value

    val context = LocalContext.current
    val calendar = Calendar.getInstance()
    val year = calendar.get(Calendar.YEAR)
    val month = calendar.get(Calendar.MONTH)
    val day = calendar.get(Calendar.DAY_OF_MONTH)
    var selectedDate by remember { mutableStateOf("") }
    val showDatePicker = {
        DatePickerDialog(
            context,
            { _: DatePicker, selectedYear: Int, selectedMonth: Int, selectedDayOfMonth: Int ->
                selectedDate = "${selectedDayOfMonth.toString().padStart(2, '0')}/" +
                        "${(selectedMonth + 1).toString().padStart(2, '0')}/" +
                        "$selectedYear"
            },
            year, month, day
        ).show()
    }

    val rutasSimples = listOf(
        RouteSimple(routeId = "R001", nombreRuta = "Ruta Norte", fecha = "2025-05-10"),
        RouteSimple(routeId = "R002", nombreRuta = "Ruta Sur", fecha = "2025-05-11")
    )
    ScreenContainer(title = stringResource(id = R.string.listRoutes), true,false,true,null,AppScreen.Menu.route) {
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
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .border(2.dp, MoradoApp, RoundedCornerShape(12.dp))
                                .clickable { showDatePicker() }
                                .padding(horizontal = 16.dp, vertical = 12.dp)
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = if (selectedDate.isEmpty()) "Seleccionar fecha" else selectedDate,
                                    style = AppTypography.labelLarge
                                )

                                Icon(
                                    painter = painterResource(id = R.drawable.date),
                                    contentDescription = "Fecha de Ruta",
                                    tint = MoradoApp,
                                    modifier = Modifier.size(30.dp)
                                )
                            }
                        }
                        val formattedSelectedDate = remember(selectedDate) {
                        if (selectedDate.isNotEmpty()) {
                            val parts = selectedDate.split("/")
                            "${parts[2]}-${parts[1].padStart(2, '0')}-${parts[0].padStart(2, '0')}"
                        } else ""
                    }

                        val filteredRoutes = if (formattedSelectedDate.isNotEmpty()) {
                            routes.filter { it.fecha.startsWith(formattedSelectedDate) }
                        } else {
                            routes
                        }
                        ListaDeRutas(filteredRoutes) { selectedRouteId ->
                            navController.navigate("detalleRuta/$selectedRouteId")
                        }

                    }
                }
            }
        }
    }
}