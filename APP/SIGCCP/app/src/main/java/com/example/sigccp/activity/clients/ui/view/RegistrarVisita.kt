package com.example.sigccp.activity.clients.ui.view

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.example.sigccp.ui.View.Components.CustomButton
import com.example.sigccp.ui.View.Components.ScreenContainer
import com.example.sigccp.activity.clients.data.model.Client
import com.example.sigccp.activity.clients.ui.viewmodel.ClienteViewModel
import com.example.sigccp.ui.theme.CcpColors

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RegistrarVisita(viewModel: ClienteViewModel = viewModel(), navController: NavController) {
    val clientes = viewModel.clientes.collectAsState().value
    val isLoading = viewModel.isLoading.collectAsState().value

    var selectedCliente by remember { mutableStateOf<Client?>(null) }
    var informe by remember { mutableStateOf("") }
    var expanded by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) { viewModel.fetchClientes() }
    ScreenContainer(title = "Registrar Visita") {
        Column(Modifier.fillMaxSize().padding(16.dp)) {
            if (isLoading) {
                CircularProgressIndicator()
            } else {
                ExposedDropdownMenuBox(
                    expanded = expanded,
                    onExpandedChange = { expanded = it }
                ) {
                    OutlinedTextField(
                        value = selectedCliente?.nombre ?: "Selecciona un cliente",
                        onValueChange = {},
                        readOnly = true,
                        modifier = Modifier.menuAnchor(),
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = CcpColors.GrisApp,
                            unfocusedBorderColor = Color.Gray
                        )
                    )
                    ExposedDropdownMenu(
                        expanded = expanded,
                        onDismissRequest = { expanded = false },
                        modifier = Modifier.exposedDropdownSize(),
                    ) {
                        clientes.forEach { cliente ->
                            DropdownMenuItem(
                                text = { Text(cliente.nombre) },
                                onClick = {
                                    selectedCliente = cliente
                                    expanded = false
                                },
                                modifier = Modifier.background(CcpColors.GradientStart)
                            )
                        }
                    }
                }
            }
            Spacer(modifier = Modifier.height(4.dp))
            selectedCliente?.let {
                Text("Nombre: ${it.nombre}")
                Text("Dirección: ${it.direccion}")
                Text("Teléfono: ${it.telefono}")
            }
            Spacer(modifier = Modifier.height(4.dp))
            Text("Informe:", style = MaterialTheme.typography.bodyLarge)
            OutlinedTextField(
                value = informe,
                onValueChange = { informe = it },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(4.dp))
            Row {
                CustomButton(text ="Cancelar") { navController.popBackStack() }
                CustomButton(text = "Aceptar") {
                    viewModel.sendVisit(
                        selectedCliente?.id ?: "",
                        informe,
                        onSuccess = { navController.popBackStack() },
                        onError = { msg -> println(msg) }
                    )
                }
            }
        }
    }
}
