package com.example.sigccp.navigation

import androidx.compose.runtime.Composable
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
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


class NavigationController {
    companion object {
        lateinit var navController: NavHostController
        fun navigate(route: String) {
            navController.navigate(route)
        }
    }
}

@Composable
fun NavigationScreen(clientViewModel: ClienteViewModel)
{
    val token = PreferencesManager.getString(PreferenceKeys.TOKEN)
    val startDestination = if (token.isNotEmpty()) AppScreen.Menu.route else AppScreen.Login.route

    val viewModel: PedidoViewModel = viewModel()
    NavigationController.navController = rememberNavController()

    NavHost(navController=NavigationController.navController, startDestination = startDestination)
    {
        composable(route = AppScreen.Login.route)
        {
            Login()
        }

        composable(route = AppScreen.Menu.route)
        {
            Menu()
        }
        composable(route = AppScreen.ListarPedidos.route)
        {
            ListarPedidos()
        }
        composable(route = AppScreen.RegistrarVisita.route)
        {
            RegistrarVisita(clientViewModel)
        }
        composable(route = AppScreen.CrearCliente.route)
        {
            CrearCliente(clientViewModel)
        }
        composable(route = AppScreen.CrearPedido.route)
        {
            CrearPedido(viewModel)
        }
        composable(route = AppScreen.AgregarProductos.route)
        {
            AgregarProductos(viewModel)
        }
    }
}