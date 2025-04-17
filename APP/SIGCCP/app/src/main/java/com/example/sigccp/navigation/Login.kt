package com.example.sigccp.navigation

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.example.sigccp.PreferenceKeys
import com.example.sigccp.PreferencesManager
import com.example.sigccp.activity.clients.ui.view.CustomTextField
import com.example.sigccp.ui.View.Components.PasswordTextField
import com.example.sigccp.ui.View.Components.ScreenContainer
import com.example.sigccp.ui.View.Components.newButton
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.GetTokenResult

fun loginAndExtractRole(
    email: String,
    password: String,
    onSuccess: () -> Unit,
    onError: (String) -> Unit
) {
    val auth = FirebaseAuth.getInstance()

    auth.signInWithEmailAndPassword(email, password)
        .addOnCompleteListener { loginTask ->
            if (loginTask.isSuccessful) {
                val user = auth.currentUser
                val userId = user?.uid
                val userName = user?.displayName ?: user?.email

                user?.getIdToken(true)
                    ?.addOnCompleteListener { tokenTask ->
                        if (tokenTask.isSuccessful) {
                            val tokenResult: GetTokenResult? = tokenTask.result
                            val claims = tokenResult?.claims
                            val role = claims?.get("role") as? String
                            val theToken = tokenResult?.token

                            if (role != null && theToken != null && userId != null && userName != null) {
                                PreferencesManager.saveString(PreferenceKeys.ROLE, role)
                                PreferencesManager.saveString(PreferenceKeys.TOKEN, theToken)
                                PreferencesManager.saveString(PreferenceKeys.USER_ID, userId)
                                PreferencesManager.saveString(PreferenceKeys.USER_NAME, userName)
                                onSuccess()
                            } else {
                                onError("Faltan datos en el token.")
                            }
                        } else {
                            val error = tokenTask.exception
                            onError("Error al obtener token: ${error?.localizedMessage}")
                        }
                    }
            } else {
                val error = loginTask.exception
                onError("Error en autenticación: ${error?.localizedMessage}")
            }
        }
}

@Composable
fun Login() {
    var correo by remember { mutableStateOf("") }
    var contrasena by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    fun isEmailValid(email: String): Boolean {
        return android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()
    }

    fun isPasswordValid(password: String): Boolean {
        return password.length >= 6
    }

    ScreenContainer(title = "Iniciar Sesión", false, null) {
        Column(Modifier.fillMaxSize().padding(16.dp)) {
            Column(
                modifier = Modifier.fillMaxSize(),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                CustomTextField(label = "Correo", value = correo, onValueChange = { correo = it })
                PasswordTextField(label = "Contraseña", value = contrasena, onValueChange = { contrasena = it })

                if (isLoading) {
                    CircularProgressIndicator()
                }

                errorMessage?.let {
                    Text(it, color = Color.Red, style = MaterialTheme.typography.bodyMedium)
                }

                newButton(
                    onClick = {
                        errorMessage = null
                        if (!isEmailValid(correo)) {
                            errorMessage = "Correo inválido"
                            return@newButton
                        }
                        if (!isPasswordValid(contrasena)) {
                            errorMessage = "La contraseña debe tener al menos 6 caracteres"
                            return@newButton
                        }

                        isLoading = true
                        loginAndExtractRole(
                            email = correo,
                            password = contrasena,
                            onSuccess = {
                                isLoading = false
                                NavigationController.navigate(AppScreen.Menu.route)
                            },
                            onError = {
                                isLoading = false
                                errorMessage = it
                            }
                        )
                        NavigationController.navigate(AppScreen.Menu.route)
                    },
                    nombre = "Ingresar"
                )

                newButton(
                    onClick = { NavigationController.navigate(AppScreen.CrearCliente.route) },
                    nombre = "Crear Cliente"
                )
            }
        }
    }
}
