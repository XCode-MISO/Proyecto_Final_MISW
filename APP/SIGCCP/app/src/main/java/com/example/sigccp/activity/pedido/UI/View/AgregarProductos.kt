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
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.runtime.LaunchedEffect
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
import androidx.compose.ui.res.stringResource
import com.example.sigccp.R
import com.example.sigccp.navigation.NavigationController
import com.example.sigccp.ui.View.Components.moneda
import com.example.sigccp.ui.theme.AppTypography


//@Preview
@Composable
fun AgregarProductos( viewModel: PedidoViewModel)
{
    Producto(viewModel)
}

@Composable
fun Producto(viewModel: PedidoViewModel)
{
    LaunchedEffect(Unit) {
        viewModel.fetchProductos()
    }
    val productos = viewModel.productosDisponibles
    var cantidades by remember { mutableStateOf<Map<Int, Int>>(emptyMap()) }
    ScreenContainer(title = stringResource(id = R.string.productos), true,false,true,null) {
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
                        Text(
                            text = "Total: $${"%.2f".format(viewModel.precioTotal.value)}",
                            style = AppTypography.labelLarge,
                            modifier = Modifier.padding(end = 16.dp)
                        )

                        newDualButton(
                            nombreIzquierdo = "Agregar",
                            onClickIzquierdo = {
                                val productosValidados = productos.value.mapNotNull { producto ->
                                    val cantidad = cantidades[producto.producto_id]

                                    if (cantidad == null || cantidad <= 0) return@mapNotNull null

                                    val esValida = cantidad <= producto.stock
                                    val total = (producto.precio * cantidad).toFloat()

                                    ProductosPedidoClass(
                                        id = producto.producto_id,
                                        nombre = producto.nombre,
                                        cantidadRequerida = cantidad,
                                        cantidadDisponible = producto.stock,
                                        precioUnitario = producto.precio,
                                        precioTotal = total,
                                        cantidadEsValida = esValida
                                    )
                                }

                                viewModel.actualizarProductosSeleccionados(productosValidados)
                                // viewModel.precioTotal.value = 0f
                                NavigationController.navigate(AppScreen.CrearPedido.route)
                            },
                            nombreDerecho = "Cancelar",
                            onClickDerecho = {
                                viewModel.precioTotal.value = 0f
                                NavigationController.navigate(AppScreen.CrearPedido.route)
                            },
                            buttonWidth = 320.dp
                        )


                        ListaDeProductosEditable(
                            productos = productos.value,
                            cantidades = cantidades,
                            onCantidadChange = { id, nuevaCantidad ->
                                cantidades = cantidades.toMutableMap().apply {
                                    this[id] = nuevaCantidad
                                }

                                val total = cantidades.entries.sumOf { (productoId, cantidad) ->
                                    val producto = productos.value.find { it.producto_id == productoId }
                                    if (producto != null) {
                                        (producto.precio * cantidad).toDouble()
                                    } else {
                                        0.0
                                    }
                                }
                                viewModel.precioTotal.value = total.toFloat()
                            }
                        )
                    }
                }
            }
        }
    }
}