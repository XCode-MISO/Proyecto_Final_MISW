package com.example.sigccp.navigation

import androidx.compose.runtime.Composable
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.sigccp.PreferenceKeys
import com.example.sigccp.PreferencesManager
import com.example.sigccp.activity.clients.ui.view.CrearCliente
import com.example.sigccp.activity.pedido.UI.View.ListarPedidos
import com.example.sigccp.activity.menu.UI.View.Menu
import com.example.sigccp.activity.clients.ui.view.RegistrarVisita
import com.example.sigccp.activity.clients.ui.viewmodel.ClienteViewModel
import com.example.sigccp.activity.pedido.UI.View.AgregarProductos
import com.example.sigccp.activity.pedido.UI.View.CrearPedido
import com.example.sigccp.activity.pedido.UI.ViewModel.PedidoViewModel

@Composable
fun NavigationScreen(clientViewModel: ClienteViewModel)
{
    val token = PreferencesManager.getString(PreferenceKeys.TOKEN)
    val startDestination = if (token.isNotEmpty()) AppScreen.Menu.route else AppScreen.Login.route

    val viewModel: PedidoViewModel = viewModel()
    val navController=rememberNavController()
    NavHost(navController=navController, startDestination = startDestination)
    {
        composable(route = AppScreen.Login.route)
        {
            Login(navController)
        }

        composable(route = AppScreen.Menu.route)
        {
            Menu(navController)
        }
        composable(route = AppScreen.ListarPedidos.route)
        {
            ListarPedidos(navController)
        }
        composable(route = AppScreen.RegistrarVisita.route)
        {
            RegistrarVisita(clientViewModel, navController)
        }
        composable(route = AppScreen.CrearCliente.route)
        {
            CrearCliente(clientViewModel, navController)
        }
        composable(route = AppScreen.CrearPedido.route)
        {
            CrearPedido(navController, viewModel)
        }
        composable(route = AppScreen.AgregarProductos.route)
        {
            AgregarProductos(navController, viewModel)
        }
    }
}