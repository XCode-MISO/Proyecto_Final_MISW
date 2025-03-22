package com.example.sigccp.navigation

import androidx.compose.runtime.Composable
import androidx.compose.ui.res.stringArrayResource
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.sigccp.activity.listarPedido.ListarPedidos
import com.example.sigccp.activity.menu.Menu

@Composable
fun NavigationScreen()
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
            ListarPedidos(navController)
        }
    }
}