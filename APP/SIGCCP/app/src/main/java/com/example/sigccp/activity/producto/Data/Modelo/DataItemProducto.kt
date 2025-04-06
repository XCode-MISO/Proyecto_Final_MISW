package com.example.sigccp.activity.producto.Data.Modelo

import androidx.room.PrimaryKey

data class DataItemProducto(
    @PrimaryKey
    val id:String ="",
    val name:String ="",
    val price: Double =0.0,
    val amount:Int=0,
)

data class ProductoClass(
    val id: String,
    val name: String,
    val price: Double,
    val amount: Int,
)

data class ProductosPedido(
    val productosPedidos: List<ProductoClass>
)

data class ProductosPedidoClass(
    val id: String,
    val nombre: String,
    val precioUnitario: Double,
    val cantidadDisponible: Int,
    val cantidadRequerida: Int = 0,
    val precioTotal: Double = 0.0,
    val cantidadEsValida: Boolean = true
)
