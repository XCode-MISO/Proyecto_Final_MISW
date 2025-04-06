package com.example.sigccp.activity.pedido.UI.View

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
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.sigccp.R
import com.example.sigccp.ui.View.Components.ClientDropdown
import com.example.sigccp.ui.View.Components.ListaDeProductosEditable
import com.example.sigccp.ui.View.Components.ListaDeProductosPedido
import com.example.sigccp.ui.View.Components.ScreenContainer
import com.example.sigccp.ui.View.Components.locationDropdown
import com.example.sigccp.ui.View.Components.newAgregarButton
import com.example.sigccp.ui.View.Components.newDualButton
import com.example.sigccp.ui.View.clientes
import com.example.sigccp.ui.View.pedidosDePrueba
import com.example.sigccp.ui.View.productos
import kotlin.collections.set


@Preview
@Composable
fun AgregarProducto()
{
    Producto()
}

@Composable
fun Producto()
{
    var cantidades by remember { mutableStateOf(productos.associate { it.id to 0 }) }

    ScreenContainer(title = "!Productos¡",false,null) {
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
                        locationDropdown(
                            locations = clientes,
                            onLocationtSelected = { id -> println("Cliente seleccionado: $id") }
                        )
                        newDualButton(
                            nombreIzquierdo = "Agregar",
                            onClickIzquierdo = { /* Acción Agregar */ },
                            nombreDerecho = "Cancelar",
                            onClickDerecho = { /* Acción Cancelar */ },
                            buttonWidth = 300.dp,
                        )
                        ListaDeProductosEditable(
                            productos = productos,
                            cantidades = cantidades,
                            onCantidadChange = { id, nuevaCantidad ->
                                cantidades = cantidades.toMutableMap().apply {
                                    this[id] = nuevaCantidad
                                }
                            }
                        )
                    }
                }
            }
        }
    }
}