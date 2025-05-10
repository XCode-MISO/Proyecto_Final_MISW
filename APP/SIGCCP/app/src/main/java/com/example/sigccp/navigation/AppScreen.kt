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
    object Inventario:AppScreen("Inventario")
    object Rutas:AppScreen("Rutas")
    object Recomendacion:AppScreen("Recomendacion")
    object RegistrarVisita:AppScreen("RegistrarVisita")
    object Entregas:AppScreen("Entregas")
}