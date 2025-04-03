package com.example.sigccp.activity.pedido.UI.View

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.sigccp.R
import com.example.sigccp.ui.View.Components.ClientDropdown
import com.example.sigccp.ui.View.Components.PedidoBox
import com.example.sigccp.ui.View.Components.ScreenContainer
import com.example.sigccp.ui.View.Components.locationDropdown
import com.example.sigccp.ui.View.Components.newButton
import com.example.sigccp.ui.View.Components.newMenuButton
import com.example.sigccp.ui.View.clientes
import com.example.sigccp.ui.View.pedidoEjemplo
import com.example.sigccp.ui.theme.AmarilloApp
import com.example.sigccp.ui.theme.AppTypography
import com.example.sigccp.ui.theme.VerdeApp

@Preview
@Composable
fun ListarPedidos()
{
    Pedidos()
}

@Composable
fun Pedidos ()
{
    ScreenContainer(title = stringResource(id = R.string.menuVendedor),false,null) {
        Box(
            modifier = Modifier
                .fillMaxSize(), // Ocupa toda la pantalla para centrar el contenido
            contentAlignment = Alignment.Center // Centra el contenido en la pantalla
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
/*
@Composable
fun Pedido()
{

}*/