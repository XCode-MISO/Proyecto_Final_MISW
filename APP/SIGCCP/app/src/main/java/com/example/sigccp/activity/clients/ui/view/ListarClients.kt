package com.example.sigccp.activity.clients.ui.view

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
import com.example.sigccp.PreferenceKeys
import com.example.sigccp.PreferencesManager
import com.example.sigccp.R
import com.example.sigccp.activity.clients.ui.viewmodel.ClienteViewModel
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.navigation.NavigationController
import com.example.sigccp.ui.View.Components.ListaDeClientes
import com.example.sigccp.ui.View.Components.ScreenContainer


//@Preview
@Composable
fun ListarClientes()
{
    Clients()
}

@Composable
fun Clients (viewModel: ClienteViewModel = viewModel ())
{
    val navController = NavigationController.navController
    BackHandler {
        navController.navigate(AppScreen.Menu.route){
            popUpTo(0)
        }
    }
    viewModel.fetchClientes()
    val clients = viewModel.clientes.collectAsState().value
    val role = PreferencesManager.getString(PreferenceKeys.ROLE)
    val rolEsCliente = (role == "cliente")
    val clientId = PreferencesManager.getString(PreferenceKeys.USER_ID)

    ScreenContainer(title = stringResource(id = R.string.listClients), true,false,true,null,AppScreen.Menu.route) {
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
                        ListaDeClientes(clients)
                    }
                }
            }
        }
    }
}



