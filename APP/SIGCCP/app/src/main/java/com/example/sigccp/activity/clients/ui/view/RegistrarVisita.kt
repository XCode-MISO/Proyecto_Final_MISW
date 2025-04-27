package com.example.sigccp.activity.clients.ui.view

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.example.sigccp.ui.View.Components.CustomButton
import com.example.sigccp.ui.View.Components.ScreenContainer
import com.example.sigccp.activity.clients.data.model.Client
import com.example.sigccp.activity.clients.ui.viewmodel.ClienteViewModel
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.navigation.NavigationController
import com.example.sigccp.ui.theme.CcpColors
import com.google.android.gms.maps.model.CameraPosition
import com.google.android.gms.maps.model.LatLng
import com.google.maps.android.compose.GoogleMap
import com.google.maps.android.compose.Marker
import com.google.maps.android.compose.MarkerState
import com.google.maps.android.compose.rememberCameraPositionState


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RegistrarVisita(viewModel: ClienteViewModel = viewModel()) {
    val context = LocalContext.current
    val clientes = viewModel.clientes.collectAsState().value
    val isLoading = viewModel.isLoading.collectAsState().value

    var selectedCliente by remember { mutableStateOf<Client?>(null) }
    var informe by remember { mutableStateOf("") }
    var expanded by remember { mutableStateOf(false) }

    var mostrarMapa by remember { mutableStateOf(false) } // Controla la visibilidad del mapa
    var selectedPosition by remember { mutableStateOf<LatLng?>(null) }
    val cameraPositionState = rememberCameraPositionState {
        position = CameraPosition.fromLatLngZoom(LatLng(4.6097, -74.0817), 10f) // Bogotá
    }
    LaunchedEffect(Unit) { viewModel.fetchClientes() }
    ScreenContainer(title = "Registrar Visita",false,true,null) {
        Box(
            modifier = Modifier
                .fillMaxSize(),
            contentAlignment = Alignment.Center
        ){
            Column(
                modifier = Modifier
                    .fillMaxSize(),
                verticalArrangement = Arrangement.Center
            )
            {

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

                // Switch para mostrar u ocultar el mapa
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Agregar ubicación de la visita")
                    Spacer(modifier = Modifier.width(8.dp))
                    Switch(
                        checked = mostrarMapa,
                        onCheckedChange = { mostrarMapa = it }
                    )
                }

                Spacer(modifier = Modifier.height(4.dp))
                if (mostrarMapa) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .fillMaxHeight(0.4f)
                    )
                    {
                        GoogleMap(
                            modifier = Modifier.fillMaxSize(),
                            cameraPositionState = cameraPositionState,
                            onMapClick = { latLng ->
                                selectedPosition = latLng
                            }
                        ) {
                            selectedPosition?.let {
                                Marker(
                                    state = MarkerState(position = it),
                                    title = "Ubicación seleccionada"
                                )
                            }
                        }
                    }
                }
                Spacer(modifier = Modifier.height(4.dp))
                Row {
                    CustomButton(text = "Cancelar") {
                        NavigationController.navigate(AppScreen.Menu.route)
                    }
                    CustomButton(text = "Aceptar") {
                        if (selectedCliente == null || informe.isBlank()) {
                            Toast.makeText(
                                context,
                                "Por favor, complete todos los campos.",
                                Toast.LENGTH_SHORT
                            ).show()
                        } else {
                            val latitud = selectedPosition?.latitude ?: 0.0
                            val longitud = selectedPosition?.longitude ?: 0.0
                            viewModel.sendVisit(
                                selectedCliente?.id ?: "",
                                informe,
                                latitud,
                                longitud,
                                onSuccess = {
                                    Toast.makeText(
                                        context,
                                        "Visita Registrada", Toast.LENGTH_SHORT
                                    ).show()
                                    NavigationController.navigate(AppScreen.Menu.route)
                                },
                                onError = { msg ->
                                    Toast.makeText(
                                        context,
                                        msg, Toast.LENGTH_LONG
                                    ).show()
                                }
                            )
                        }
                    }
                }
            }
        }
    }
}
