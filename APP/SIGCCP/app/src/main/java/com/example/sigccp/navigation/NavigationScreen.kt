package com.example.sigccp.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.sigccp.activity.clients.ui.view.CrearCliente
import com.example.sigccp.activity.pedido.UI.View.ListarPedidos
import com.example.sigccp.activity.menu.UI.View.Menu
import com.example.sigccp.activity.clients.ui.view.RegistrarVisita
import com.example.sigccp.activity.clients.ui.viewmodel.ClienteViewModel

@Composable
fun NavigationScreen(clientViewModel: ClienteViewModel)
{
    val navController=rememberNavController()
    NavHost(navController=navController, startDestination = AppScreen.Menu.route)
    {
        composable(route = AppScreen.Menu.route)
        {
            Menu(navController)
        }
        composable(route = AppScreen.ListarPedidos.route)
        {
            ListarPedidos()
        }
        composable(route = AppScreen.RegistrarVisita.route)
        {
            RegistrarVisita(clientViewModel, navController)
        }
        composable(route = AppScreen.CrearCliente.route)
        {
            CrearCliente(clientViewModel, navController)
        }

    }
}