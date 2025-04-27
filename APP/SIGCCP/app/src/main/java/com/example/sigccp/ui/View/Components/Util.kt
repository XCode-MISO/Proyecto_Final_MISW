package com.example.sigccp.ui.View.Components

import android.annotation.SuppressLint
import android.app.Activity
import android.content.ContextWrapper
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.PowerSettingsNew
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.*
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults.topAppBarColors
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.sp
import com.example.sigccp.PreferencesManager
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.navigation.NavigationController
import com.example.sigccp.ui.theme.AmarilloApp
import com.example.sigccp.ui.theme.AppTypography
import com.example.sigccp.ui.theme.CcpColors
import com.example.sigccp.ui.theme.MoradoApp
import com.example.sigccp.ui.theme.VerdeApp
import androidx.activity.ComponentActivity
import androidx.activity.compose.LocalOnBackPressedDispatcherOwner

val moneda = listOf(
    1 to "Peso Colombiano",
    2 to "Dolar Americano",
)

@Composable
fun BaseScreen(content: @Composable () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.verticalGradient(
                    colors = listOf(AmarilloApp, VerdeApp)
                )
            )
    ) {
        content()
    }
}

@SuppressLint("ContextCastToActivity")
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScreenContainer(
    title: String,
    salirenabled: Boolean,
    enabled: Boolean,
    showBackButton: Boolean = false,
    imagen:Int? = null,
    backDestination: String? = null,
    content: @Composable ColumnScope.() -> Unit
) {
    val context = LocalContext.current
    val activity = remember {
        context as? ComponentActivity ?: (context as? ContextWrapper)?.baseContext as? ComponentActivity
    }


    BaseScreen {
        Column(
            modifier = Modifier
                .fillMaxSize()
        ) {
            // TopAppBar como PRIMER elemento del Column
            TopAppBar(
                colors = topAppBarColors(
                    containerColor = Color.Transparent,
                    titleContentColor = MaterialTheme.colorScheme.primary,
                ),
                title = {
                    Text(
                        modifier = Modifier.fillMaxWidth()
                            .wrapContentHeight(Alignment.CenterVertically)
                            .testTag(title),
                        textAlign = TextAlign.Center,
                        text = "SIGCCP",
                        style = AppTypography.titleLarge
                    )
                },
                navigationIcon = {
                    IconButton(
                        onClick = {
                            PreferencesManager.clearAll()
                            NavigationController.navigate(AppScreen.Login.route)
                        },
                        modifier = Modifier
                            .padding(start = 20.dp, end = 25.dp)
                            .testTag("logout")
                    ) {

                        if (salirenabled) {
                        Icon(
                            imageVector = Icons.Filled.PowerSettingsNew,
                            contentDescription = "Salir",
                            tint = MoradoApp,
                            modifier = Modifier.size(40.dp)
                        )
                        }
                    }
                },
                actions = {
                    LanguageDropdown(activity)
                }
            )
            // Contenido debajo del AppBar de forma natural
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 16.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Top
            ) {
                Spacer(modifier = Modifier.height(16.dp)) // Espaciado relativo
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp), // altura fija razonable como una barra normal
                    contentAlignment = Alignment.Center
                ) {
                    // Subtitulo siempre al centro
                    SubTitleBar(
                        texto = title,
                        imagen = imagen,
                        enabled = enabled,
                    )

                    // Botón de volver en la esquina izquierda
                    if (showBackButton) {
                        IconButton(
                            onClick = {
                                if (backDestination != null) {
                                    NavigationController.navigate(backDestination)
                                } else {
                                    activity?.onBackPressedDispatcher?.onBackPressed()
                                }
                            },
                            modifier = Modifier
                                .align(Alignment.CenterStart) // Alinearlo al inicio
                                .padding(start = 8.dp)
                                .size(40.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.ArrowBack,
                                contentDescription = "Volver atrás",
                                tint = MoradoApp
                            )
                        }
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
                content()
            }
        }
    }
}

@Composable
fun CustomButton(text: String, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        colors = ButtonDefaults.buttonColors(containerColor = CcpColors.ColorButton),
        modifier = Modifier
            .padding(8.dp)
            .testTag(text)
    ) {
        Text(text, color = CcpColors.ColorText, fontWeight = FontWeight.Bold)
    }
}

@Composable
fun PasswordTextField(
    label: String,
    value: String,
    onValueChange: (String) -> Unit
) {
    var passwordVisible by remember { mutableStateOf(false) }
    Text(text = label, fontSize = 16.sp, fontWeight = FontWeight.Bold)
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        singleLine = true,
        visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
        trailingIcon = {
            val icon = if (passwordVisible) Icons.Default.Visibility else Icons.Default.VisibilityOff
            val description = if (passwordVisible) "Ocultar contraseña" else "Mostrar contraseña"
            IconButton(onClick = { passwordVisible = !passwordVisible }) {
                Icon(imageVector = icon, contentDescription = description, tint = Color.DarkGray)
            }
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
