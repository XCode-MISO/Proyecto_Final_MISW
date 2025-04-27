package com.example.sigccp.activity.clients.ui.view

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.sigccp.activity.clients.ui.viewmodel.ClienteViewModel
import com.example.sigccp.ui.View.Components.ScreenContainer
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.Alignment
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.sp
import com.example.sigccp.R
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.navigation.NavigationController
import com.example.sigccp.ui.View.Components.CustomButton
import com.google.android.gms.maps.model.CameraPosition
import com.google.android.gms.maps.model.LatLng
import com.google.maps.android.compose.GoogleMap
import com.google.maps.android.compose.Marker
import com.google.maps.android.compose.MarkerState
import com.google.maps.android.compose.rememberCameraPositionState

@Composable
fun CrearCliente(
    viewModel: ClienteViewModel = viewModel()
) {
    val isLoading = viewModel.isLoading.collectAsState().value
    val context = LocalContext.current
    var nombre by remember { mutableStateOf("") }
    var direccion by remember { mutableStateOf("") }
    var correo by remember { mutableStateOf("") }
    var telefono by remember { mutableStateOf("") }

    var selectedPosition by remember { mutableStateOf<LatLng?>(null) }
    val cameraPositionState = rememberCameraPositionState {
        position = CameraPosition.fromLatLngZoom(LatLng(4.6097, -74.0817), 10f) // Bogotá
    }

    fun isEmailValid(email: String): Boolean {
        return android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()
    }

    ScreenContainer(title = stringResource(id = R.string.client), false,false,true, null) {
        Column(Modifier.fillMaxSize().padding(16.dp)) {
            if (isLoading) {
                CircularProgressIndicator()
            } else {
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
                        CustomTextField(
                            label = "Nombre",
                            value = nombre,
                            onValueChange = { nombre = it })
                        CustomTextField(
                            label = "Direccion",
                            value = direccion,
                            onValueChange = { direccion = it })
                        CustomTextField(
                            label = "Correo",
                            value = correo,
                            onValueChange = { correo = it },
                            isEmail = true
                        )
                        CustomTextField(
                            label = "Telefono",
                            value = telefono,
                            onValueChange = { telefono = it },
                            isNumeric = true
                        )
                        // Switch para mostrar u ocultar el mapa
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("Ubicación:")
                            Spacer(modifier = Modifier.width(8.dp))
                        }
                        Spacer(modifier = Modifier.height(4.dp))
                        Box(modifier = Modifier
                            .fillMaxWidth()
                            .fillMaxHeight(0.4f))
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

                        Row {
                            CustomButton(text = "Cancelar") {
                                NavigationController.navigate(AppScreen.Login.route)
                            }
                            CustomButton(text = "Aceptar") {
                                val allFieldsFilled = nombre.isNotBlank() &&
                                        correo.isNotBlank() &&
                                        direccion.isNotBlank() &&
                                        telefono.isNotBlank() &&
                                        selectedPosition != null

                                if (!allFieldsFilled) {
                                    Toast.makeText(context, "Por favor, complete todos los campos.", Toast.LENGTH_SHORT).show()
                                    return@CustomButton
                                }

                                if (!isEmailValid(correo)) {
                                    Toast.makeText(context, "Correo no valido", Toast.LENGTH_SHORT).show()
                                    return@CustomButton
                                }
                                val latitud = selectedPosition?.latitude ?: 0.0
                                val longitud = selectedPosition?.longitude ?: 0.0

                                viewModel.createClient(
                                    nombre, correo, direccion, telefono, latitud, longitud,
                                    onSuccess = {
                                        Toast.makeText(
                                            context,
                                            "Usuario creado, revise su correo", Toast.LENGTH_LONG
                                        ).show()
                                        NavigationController.navigate(AppScreen.Login.route)
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
}

@Composable
fun CustomTextField(
    label: String,
    value: String,
    onValueChange: (String) -> Unit,
    isEmail: Boolean = false,
    isNumeric: Boolean = false
) {
    Text(text = label, fontSize = 16.sp, fontWeight = FontWeight.Bold)
    OutlinedTextField(
        value = value,
        onValueChange = {
            if (isNumeric && it.any { char -> !char.isDigit() && char != '+' }) return@OutlinedTextField
            onValueChange(it)
        },
        singleLine = true,
        keyboardOptions = when {
            isEmail -> KeyboardOptions.Default.copy(keyboardType = KeyboardType.Email)
            isNumeric -> KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number)
            else -> KeyboardOptions.Default
        },
        modifier = Modifier
            .fillMaxWidth()
            .testTag(label),
        colors = OutlinedTextFieldDefaults.colors(
            focusedBorderColor = Color.DarkGray,
            unfocusedBorderColor = Color.DarkGray
        )
    )
}