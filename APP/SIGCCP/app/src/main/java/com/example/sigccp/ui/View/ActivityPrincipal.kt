package com.example.sigccp.ui.View

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.sigccp.R
import com.example.sigccp.activity.pedido.Data.Modelo.ClienteClass
import com.example.sigccp.activity.pedido.Data.Modelo.PedidoClass
import com.example.sigccp.activity.pedido.Data.Modelo.Pedidos
import com.example.sigccp.ui.View.Components.ClientDropdown
import com.example.sigccp.ui.View.Components.PedidoBox
import com.example.sigccp.ui.View.Components.ScreenContainer
import com.example.sigccp.ui.View.Components.locationDropdown
import com.example.sigccp.ui.View.Components.newButton
import com.example.sigccp.ui.View.Components.newMenuButton

val clientes = listOf(
    1 to "Juan Pérez",
    2 to "María González",
    3 to "Carlos López"
)

val pedidoEjemplo = PedidoClass(
    id = "57623699-c732-44a7-808f-88580b45d84f",
    name = "Pedido especial",
    price = 150.75,
    state= "Pendiente",
    client = ClienteClass(
        id = "123e4567-e89b-12d3-a456-426614174000",
        name = "pedrito perez"
    )
)

val listaPedidos = Pedidos(
    pedidos = listOf(
        PedidoClass("1", "Pedido 1", 1200050.0, "pendiente", ClienteClass("123e4567-e89b-12d3-a456-426614174000","pedrito perez")),
        PedidoClass("2", "Pedido 2", 75.0, "enviado", ClienteClass("123e4567-e89b-12d3-a456-426614174000","pedrito perez")),
        PedidoClass("2", "Pedido 2", 75.0, "enviado", ClienteClass("123e4567-e89b-12d3-a456-426614174000","pedrito perez")),
        PedidoClass("2", "Pedido 2", 75.0, "enviado", ClienteClass("123e4567-e89b-12d3-a456-426614174000","pedrito perez")),
        PedidoClass("2", "Pedido 2", 75.0, "enviado", ClienteClass("123e4567-e89b-12d3-a456-426614174000","pedrito perez")),
        PedidoClass("2", "Pedido 2", 75.0, "enviado", ClienteClass("123e4567-e89b-12d3-a456-426614174000","pedrito perez")),
        PedidoClass("2", "Pedido 2", 75.0, "enviado", ClienteClass("123e4567-e89b-12d3-a456-426614174000","pedrito perez")),
        PedidoClass("2", "Pedido 2", 75.0, "enviado", ClienteClass("123e4567-e89b-12d3-a456-426614174000","pedrito perez")),
        PedidoClass("2", "Pedido 2", 75.0, "enviado", ClienteClass("123e4567-e89b-12d3-a456-426614174000","pedrito perez")),
        PedidoClass("1", "Pedido 1", 50.0, "pendiente", ClienteClass("123e4567-e89b-12d3-a456-426614174000","pedrito perez"))
    )
)

@Preview
@Composable
fun MainScreen(
       //navController: NavController,
        //menu: Menu
) {
    ScreenContainer(title = "Hola Usuario",true,R.drawable.avatar) {
        Box(
            modifier = Modifier
                .fillMaxSize(),
            contentAlignment = Alignment.Center
        )
        {
            Column(
                modifier = Modifier
                    .fillMaxSize(),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            )
            {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .wrapContentSize(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.Top
                )
                {
                    Column(
                        modifier = Modifier
                            .width(300.dp),
                        verticalArrangement = Arrangement.Center,
                        horizontalAlignment = Alignment.CenterHorizontally
                    )
                    {
                    }
                }
                Row(
                    modifier = Modifier
                        .fillMaxSize(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                )
                {
                    Column(
                        modifier = Modifier
                            .width(300.dp)
                            .padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    )
                    {
                        newButton(onClick = {/*todo*/}, nombre= "Crear Pedido")
                        locationDropdown(
                            locations = clientes,
                            onLocationtSelected = { id -> println("Cliente seleccionado: $id") }
                        )
                        ClientDropdown(
                            clients = clientes,
                            onClientSelected = { id -> println("Cliente seleccionado: $id") }
                        )
                        PedidoBox(pedido = pedidoEjemplo)
                        newMenuButton(
                            onClick = {/*TODO*/ },
                            nombre = "CREAR CLIENTE",
                            imagen = R.drawable.editar,
                            enabled = true
                        )
                    }
                }
            }
        }
    }
}

