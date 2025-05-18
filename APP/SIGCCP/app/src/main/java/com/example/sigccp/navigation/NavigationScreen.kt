package com.example.sigccp.navigation

import android.util.Log
import androidx.compose.runtime.Composable
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.example.sigccp.PreferenceKeys
import com.example.sigccp.PreferencesManager
import com.example.sigccp.activity.clients.ui.view.CrearCliente
import com.example.sigccp.activity.clients.ui.view.ListarClientes
import com.example.sigccp.activity.pedido.UI.View.ListarPedidos
import com.example.sigccp.activity.menu.UI.View.Menu
import com.example.sigccp.activity.clients.ui.view.RegistrarVisita
import com.example.sigccp.activity.clients.ui.viewmodel.ClienteViewModel
import com.example.sigccp.activity.entrega.ui.view.ListarEntregas
import com.example.sigccp.activity.entrega.ui.viewmodel.ListarEntregasViewModel
import com.example.sigccp.activity.pedido.UI.View.AgregarProductos
import com.example.sigccp.activity.pedido.UI.View.CrearPedido
import com.example.sigccp.activity.pedido.UI.ViewModel.PedidoViewModel
import com.example.sigccp.activity.recomendacion.ui.view.Recomendacion
import com.example.sigccp.activity.recomendacion.ui.viewmodel.RecomendacionServiceViewModel
import com.example.sigccp.activity.recomendacion.ui.viewmodel.RecomendacionViewModel
import com.example.sigccp.activity.route.UI.view.ListarRutas
import com.example.sigccp.activity.route.UI.view.RouteDetail


class NavigationController {
    companion object {
        lateinit var navController: NavHostController
        fun navigate(route: String) {
            navController.navigate(route)
        }
    }
}

@Composable
fun NavigationScreen(recomendacionServiceViewModel: RecomendacionServiceViewModel)
{
    val token = PreferencesManager.getString(PreferenceKeys.TOKEN)
    val startDestination = if (token.isNotEmpty()) AppScreen.Menu.route else AppScreen.Login.route

    val clientViewModel: ClienteViewModel = viewModel()
    val recomendacionViewModel: RecomendacionViewModel = viewModel()
    val entregasViewModel: ListarEntregasViewModel = viewModel()
    val pedidoViewModel: PedidoViewModel = viewModel()

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
        composable(route = AppScreen.ListarClientes.route)
        {
            ListarClientes()
        }
        composable(route = AppScreen.ListarRutas.route)
        {
            ListarRutas()
        }
        composable(
            route = AppScreen.DetalleRuta.route,
            arguments = listOf(navArgument("routeId") { type = NavType.StringType })
        ) { backStackEntry ->
            val routeId = backStackEntry.arguments?.getString("routeId")
            if (routeId != null) {
                RouteDetail(routeId = routeId)
            }
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
            CrearPedido(pedidoViewModel)
        }
        composable(route = AppScreen.AgregarProductos.route)
        {
            AgregarProductos(pedidoViewModel)
        }
        composable(route = AppScreen.Recomendacion.route)
        {
            Recomendacion(recomendacionViewModel, recomendacionServiceViewModel)
        }
        composable(route = AppScreen.Entregas.route)
        {
            ListarEntregas(entregasViewModel)
        }
    }
}