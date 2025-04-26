package com.example.sigccp.activity.pedido.Data.Modelo
//APP/SIGCCP/app/src/main/java/com/example/sigccp/activity/pedido/Data/Modelo/DataItemPedido.kt
import androidx.room.PrimaryKey
import com.example.sigccp.activity.cliente.Data.Modelo.DataItemClient
import com.example.sigccp.activity.producto.Data.Modelo.DataItemProducto



data class DataItemPedido(
    @PrimaryKey
    val id:String ="",
    val name:String ="",
    val client: DataItemClient = DataItemClient(),
    val products: List<DataItemProducto> = emptyList(),
    val price:Float=0.0f,
    //val deliveryDate:String="",
)

data class PedidoClass(
    val id: String,
    val name: String,
    val price: Double,
    val state: String,
    val client: ClienteSingleClass
)

data class Pedidos(
    val pedidos: List<PedidoClass>
)

data class ClienteSingleClass(
    val id: String,
    val name: String
)

data class ClienteClass(
    val id: String,
    val nombre: String,
    val correo: String,
    val direccion: String,
    val telefono: String
)

data class PedidoRequest(
    val name: String,
    val clientId: String,
    val clientName: String,
    val vendedorId: String,
    val vendedorName: String,
    val products: List<ProductoCantidad>,
    val price: Double,
    val state: String,
    val deliveryDate: String
)

data class ProductoCantidad(
    val id: Int,
    val amount: Int
)
