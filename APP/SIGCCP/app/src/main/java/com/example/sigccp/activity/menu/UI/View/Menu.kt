package com.example.sigccp.activity.menu.UI.View

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
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.example.sigccp.PreferenceKeys
import com.example.sigccp.PreferencesManager
import com.example.sigccp.R
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.navigation.NavigationController
import com.example.sigccp.ui.View.Components.ScreenContainer
import com.example.sigccp.ui.View.Components.MenuButton
import androidx.activity.compose.BackHandler
//import com.example.sigccp.BuildConfig



@Composable
fun Menu()
{
    Options()
}

@Composable
fun Options()
{
    val navController = NavigationController.navController
    BackHandler {
        navController.navigate(AppScreen.Menu.route) {
            popUpTo(0)
        }
    }
    val role = PreferencesManager.getString(PreferenceKeys.ROLE)
    val rolEsCliente = (role == "cliente")
    val saludo = if (rolEsCliente) stringResource(id = R.string.menuCliente) else stringResource(id = R.string.menuVendedor)

    ScreenContainer(title = saludo, true,false,false, null) {
        Box(
            modifier = Modifier
                .fillMaxSize(),
            contentAlignment = Alignment.Center
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
                        MenuButton(
                            onClick = { NavigationController.navigate(AppScreen.ListarPedidos.route) },
                            nombre = stringResource(id = R.string.pedidos),
                            imagen = R.drawable.editar
                        )
                        if(!rolEsCliente){
                            MenuButton(
                                onClick = {NavigationController.navigate(AppScreen.ListarClientes.route)},
                                nombre = stringResource(id = R.string.clientes),
                                imagen = R.drawable.ver
                            )
                        }
                        MenuButton(
                            onClick = {/*TODO*/ },
                            nombre = stringResource(id = R.string.inventario),
                            imagen = R.drawable.ver
                        )
                        if(!rolEsCliente) {
                            MenuButton(
                                onClick = {NavigationController.navigate(AppScreen.ListarRutas.route)},
                                nombre = stringResource(id = R.string.rutas),
                                imagen = R.drawable.ia
                            )
                        }
                        if(!rolEsCliente){
                            MenuButton(
                                onClick = {NavigationController.navigate(AppScreen.Recomendacion.route) },
                                nombre = stringResource(id = R.string.recomendacion),
                                imagen = R.drawable.config
                            )
                        }
                        if(!rolEsCliente) {
                            MenuButton(
                                onClick = { NavigationController.navigate(AppScreen.RegistrarVisita.route) },
                                nombre = stringResource(id = R.string.visita),
                                imagen = R.drawable.editar
                            )
                        }
                        if(rolEsCliente) {
                            MenuButton(
                                onClick = { NavigationController.navigate(AppScreen.Entregas.route) },
                                nombre = stringResource(id = R.string.delivery),
                                imagen = R.drawable.editar
                            )
                        }
                    }
                }
            }
            androidx.compose.material3.Text(
                text = "aplicacion-app@0.0.3",
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .padding(bottom = 16.dp)
            )
        }
    }
}
