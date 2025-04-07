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
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.example.sigccp.activity.pedido.UI.ViewModel.PedidoViewModel
import com.example.sigccp.activity.producto.Data.Modelo.ProductosPedidoClass
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.ui.View.Components.ListaDeProductosEditable
import com.example.sigccp.ui.View.Components.ScreenContainer
import com.example.sigccp.ui.View.Components.locationDropdown
import com.example.sigccp.ui.View.Components.newDualButton
import kotlin.collections.set
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import com.example.sigccp.ui.View.moneda


//@Preview
@Composable
fun AgregarProductos( navController: NavController, viewModel: PedidoViewModel)
{
    Producto(navController,viewModel)
}

@Composable
fun Producto( navController: NavController,
              viewModel: PedidoViewModel = viewModel()
)
{
    val productos = viewModel.productosDisponibles
    var cantidades by remember { mutableStateOf<Map<String, Int>>(emptyMap()) }
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
                            locations = moneda,
                            onLocationtSelected = { id -> println("Cliente seleccionado: $id") }
                        )
                        newDualButton(
                                nombreIzquierdo = "Agregar",
                        onClickIzquierdo = {
                            val productosValidados = productos.value.mapNotNull { producto ->
                                val cantidad = cantidades[producto.id]

                                if (cantidad == null || cantidad <= 0) return@mapNotNull null

                                val esValida = cantidad <= producto.amount
                                val total = cantidad * producto.price

                                ProductosPedidoClass(
                                    id = producto.id,
                                    nombre = producto.name,
                                    cantidadRequerida = cantidad,
                                    cantidadDisponible = producto.amount,
                                    precioUnitario = producto.price,
                                    precioTotal = total,
                                    cantidadEsValida = esValida
                                )
                            }

                            viewModel.actualizarProductosSeleccionados(productosValidados)
                            navController.navigate(AppScreen.CrearPedido.route)
                        },
                        nombreDerecho = "Cancelar",
                        onClickDerecho = { navController.popBackStack() },
                            buttonWidth = 300.dp,
                        )

                        ListaDeProductosEditable(
                            productos = productos.value,
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