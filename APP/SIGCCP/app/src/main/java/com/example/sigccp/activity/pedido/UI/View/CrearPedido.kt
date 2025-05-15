package com.example.sigccp.activity.pedido.UI.View

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.example.sigccp.PreferenceKeys
import com.example.sigccp.PreferencesManager
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
import com.example.sigccp.ui.View.Components.moneda
import com.example.sigccp.ui.theme.AppTypography
import androidx.compose.runtime.*
import com.example.sigccp.ui.theme.AmarilloApp

//@Preview
@Composable
fun CrearPedido(viewModel: PedidoViewModel)
{
    Pedido(viewModel)
}
@Composable
fun Pedido(viewModel: PedidoViewModel) {
    val navController = NavigationController.navController
    BackHandler {
        navController.navigate(AppScreen.ListarPedidos.route) {
            popUpTo(0)
        }
    }
    LaunchedEffect(Unit) {
        viewModel.fetchClientes() // Asumimos que esta es la función para cargar clientes
    }
    var showDialog by remember { mutableStateOf(false) }
    var dialogMessage by remember { mutableStateOf("") }
    val role = PreferencesManager.getString(PreferenceKeys.ROLE)
    val isLoading = viewModel.isLoading.collectAsState().value
    val productos = viewModel.productosSeleccionados.value

    ScreenContainer(title = stringResource(id = R.string.CrearPedido), true,false, true, null, AppScreen.ListarPedidos.route) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Column(
                modifier = Modifier.fillMaxSize(),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth().wrapContentSize(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.Top
                ) {
                    Column(
                        modifier = Modifier.width(300.dp),
                        verticalArrangement = Arrangement.Center,
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) { }
                }

                Row(
                    modifier = Modifier.fillMaxSize(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(
                        modifier = Modifier.width(300.dp).padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        newAgregarButton(
                            onClick = {
                                viewModel.precioTotal.value = 0f
                                NavigationController.navigate(AppScreen.AgregarProductos.route)
                            },
                            nombre = "Agregar"
                        )

                        if (role == "vendedor") {
                            ClientDropdown(
                                clients = viewModel.clientes.value,
                                onClientSelected = { cliente ->
                                    viewModel.clienteId.value = cliente.id
                                    viewModel.clienteNombre.value = cliente.nombre
                                }
                            )
                        }

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
                            nombreIzquierdo = "Aceptar",
                            onClickIzquierdo = {
                                // Validaciones
                                if (productos.isEmpty()) {
                                    dialogMessage = "Debe agregar al menos un producto."
                                    showDialog = true
                                    return@newDualButton
                                }
                                if (role == "vendedor" && viewModel.clienteId.value.isEmpty()) {
                                    dialogMessage = "Debe seleccionar un cliente."
                                    showDialog = true
                                    return@newDualButton
                                }

                                // Crear pedido si todo está correcto
                                viewModel.crearPedido(
                                    onSuccess = {
                                        dialogMessage = "Pedido creado exitosamente."
                                        showDialog = true
                                        viewModel.precioTotal.value = 0f
                                        viewModel.limpiarPedido()
                                    },
                                    onError = {
                                        dialogMessage = "Error al crear pedido: ${it.localizedMessage ?: "Error desconocido"}"
                                        showDialog = true
                                    }
                                )
                            },
                            nombreDerecho = "Cancelar",
                            onClickDerecho = {
                                viewModel.limpiarPedido()
                                viewModel.precioTotal.value = 0f
                                NavigationController.navigate(AppScreen.ListarPedidos.route)
                            },
                            buttonWidth = 320.dp,
                        )

                        if (isLoading) {
                            CircularProgressIndicator()
                        } else {
                            ListaDeProductosPedido(productos)
                        }
                    }
                }
            }
        }

        // Mostrar el AlertDialog fuera de la acción de los botones
        if (showDialog) {
            AlertDialog(
                onDismissRequest = {
                    showDialog = false
                    NavigationController.navigate(AppScreen.ListarPedidos.route)
                },
                title = { Text("Mensaje") },
                text = { Text(dialogMessage) },
                confirmButton = {
                    TextButton(
                        onClick = {
                            showDialog = false
                            NavigationController.navigate(AppScreen.ListarPedidos.route)
                        }
                    ) {
                        Text("OK")
                    }
                },
                containerColor = AmarilloApp,
            )
        }
    }
}
