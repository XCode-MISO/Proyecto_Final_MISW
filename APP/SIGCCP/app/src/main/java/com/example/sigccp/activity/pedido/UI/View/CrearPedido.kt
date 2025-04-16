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
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.example.sigccp.R
import com.example.sigccp.activity.pedido.UI.ViewModel.PedidoViewModel
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.navigation.NavigationController
import com.example.sigccp.ui.View.Components.ClientDropdown
import com.example.sigccp.ui.View.Components.ListaDeProductosPedido
import com.example.sigccp.ui.View.Components.ScreenContainer
import com.example.sigccp.ui.View.Components.locationDropdown
import com.example.sigccp.ui.View.Components.newAgregarButton
import com.example.sigccp.ui.View.Components.newDualButton
import com.example.sigccp.ui.View.moneda

//@Preview
@Composable
fun CrearPedido(viewModel: PedidoViewModel)
{
    Pedido()
}

@Composable
fun Pedido( viewModel: PedidoViewModel = viewModel()
)
{
    val productos = viewModel.productosSeleccionados.value
    ScreenContainer(title = stringResource(id = R.string.CrearPedido),false,null) {
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
                        newAgregarButton(onClick = {NavigationController.navigate(AppScreen.AgregarProductos.route)}, nombre= "Agregar")
                        ClientDropdown(
                            clients = viewModel.clientes.value,
                            onClientSelected = { id -> viewModel.clienteId.value = id.toString() }
                        )
                        locationDropdown(
                            locations = moneda,
                            onLocationtSelected = { id -> println("Cliente seleccionado: $id") }
                        )
                        newDualButton(
                            nombreIzquierdo = "Aceptar",
                            onClickIzquierdo = {
                                viewModel.crearPedido(
                                    onSuccess = {
                                        viewModel.limpiarPedido()
                                        NavigationController.navigate(AppScreen.ListarPedidos.route)
                                    },
                                    onError = {
                                        println("Error al crear pedido: ${it.localizedMessage}")
                                    }
                                )
                            },
                            nombreDerecho = "Cancelar",
                            onClickDerecho = {
                                NavigationController.navigate(AppScreen.ListarPedidos.route)
                            },
                            buttonWidth = 320.dp,
                        )
                        ListaDeProductosPedido(productos)

                    }
                }
            }
        }
    }
}