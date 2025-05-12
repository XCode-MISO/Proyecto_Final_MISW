package com.example.sigccp.navigation

sealed class AppScreen(val route:String)
{ //Crear Rutas
    object Login:AppScreen("Login")
    object Menu:AppScreen("Menu")
    object CrearCliente:AppScreen("CrearCliente")
    object ListarPedidos:AppScreen("ListarPedidos")
    object CrearPedido:AppScreen("CrearPedidos")
    object AgregarProductos:AppScreen("AgregarProductos")
    object ListarClientes:AppScreen("ListarClientes")
    object ListarRutas:AppScreen("ListarRutas")
    object DetalleRuta : AppScreen("DetalleRuta/{routeId}") {
        fun idRoute(routeId: String) = "DetalleRuta/$routeId"
    }
    object Recomendacion:AppScreen("Recomendacion")
    object RegistrarVisita:AppScreen("RegistrarVisita")
    object Entregas:AppScreen("Entregas")
}