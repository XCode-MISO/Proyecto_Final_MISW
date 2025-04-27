package com.example.sigccp.activity.producto.Data.Modelo

import androidx.room.PrimaryKey

data class DataItemProducto(
    @PrimaryKey
    val id:String ="",
    val name:String ="",
    val price: Float =0.0f,
    val amount:Int=0,
)

data class ProductoClass(
    val producto_id: Int,
    val nombre: String,
    val precio: Float,
    val stock: Int
)

data class ProductosPedido(
    val productosPedidos: List<ProductoClass>
)

data class ProductosPedidoClass(
    val id: Int,
    val nombre: String,
    val precioUnitario: Float,
    val cantidadDisponible: Int,
    val cantidadRequerida: Int = 0,
    val precioTotal: Float = 0.0f,
    val cantidadEsValida: Boolean = true
)
