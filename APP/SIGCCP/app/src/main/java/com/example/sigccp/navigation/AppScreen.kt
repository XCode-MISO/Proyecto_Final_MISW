package com.example.sigccp.navigation

sealed class AppScreen(val route:String)
{ //Crear Rutas
    object Menu:AppScreen("Menu")
    object ListarPedidos:AppScreen("ListarPedidos")
    object CrearPedido:AppScreen("CrearPedidos")
    object ListarClientes:AppScreen("ListarClientes")
    object Inventario:AppScreen("Inventario")
    object Rutas:AppScreen("Rutas")
    object Recomendacion:AppScreen("Recomendacion")
    object RegistrarVisita:AppScreen("RegistrarVisita")
}