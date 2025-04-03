package com.example.sigccp.activity.clients.ui.view

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
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.example.sigccp.activity.clients.ui.viewmodel.ClienteViewModel
import com.example.sigccp.ui.View.Components.ScreenContainer
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.Alignment
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.sp
import com.example.sigccp.ui.View.Components.CustomButton

@Composable
fun CrearCliente(viewModel: ClienteViewModel = viewModel(), navController: NavController) {
    val isLoading = viewModel.isLoading.collectAsState().value
    var nombre by remember { mutableStateOf("") }
    var direccion by remember { mutableStateOf("") }
    var correo by remember { mutableStateOf("") }
    var telefono by remember { mutableStateOf("") }

    ScreenContainer(title = "Crear Cliente", false, null) {
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
                        Spacer(modifier = Modifier.height(4.dp))
                        Row {
                            CustomButton(text = "Cancelar") { navController.popBackStack() }
                            CustomButton(text = "Aceptar") {
                                viewModel.createClient(
                                    nombre, correo, direccion, telefono, 0.0, 0.0,
                                    onSuccess = { navController.popBackStack() },
                                    onError = { msg -> println(msg) }
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
        modifier = Modifier.fillMaxWidth(),
        colors = OutlinedTextFieldDefaults.colors(
            focusedBorderColor = Color.DarkGray,
            unfocusedBorderColor = Color.DarkGray
        )
    )
}