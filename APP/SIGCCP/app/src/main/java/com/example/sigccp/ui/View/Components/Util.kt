package com.example.sigccp.ui.View.Components

import android.annotation.SuppressLint
import android.app.Activity
import android.content.ContextWrapper
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.PowerSettingsNew
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults.topAppBarColors
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import com.example.sigccp.ui.theme.AmarilloApp
import com.example.sigccp.ui.theme.AppTypography
import com.example.sigccp.ui.theme.CcpColors
import com.example.sigccp.ui.theme.MoradoApp
import com.example.sigccp.ui.theme.VerdeApp

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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppTopBar(title: String) {
    TopAppBar(
        title = { Text(title, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.Center) },
        colors = TopAppBarDefaults.topAppBarColors(
            containerColor = CcpColors.ColorAppBar // Color sólido similar al degradado
        ),
        actions = {
            IconButton(onClick = { /* Cambiar idioma */ }) {
                Icon(Icons.Default.Settings, contentDescription = "Idioma")
            }
        }
    )
}

@SuppressLint("ContextCastToActivity")
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScreenContainer(
    title: String,
    enabled: Boolean,
    imagen:Int? = null,
    content: @Composable ColumnScope.() -> Unit
) {
    val context = LocalContext.current
    val activity =
        remember { context as? Activity ?: (context as? ContextWrapper)?.baseContext as? Activity }

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
                            .wrapContentHeight(Alignment.CenterVertically),
                        textAlign = TextAlign.Center,
                        text = "SIGCCP",
                        style = AppTypography.titleLarge
                    )
                },
                navigationIcon = {
                    IconButton(
                        onClick = {/* TODO */ },
                        modifier = Modifier.padding(start = 20.dp, end = 25.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Filled.PowerSettingsNew,
                            contentDescription = "Salir",
                            tint = MoradoApp,
                            modifier = Modifier.size(40.dp)
                        )
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
                SubTitleBar(
                    texto = title,
                    imagen = imagen,
                    enabled = enabled,
                )
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
        modifier = Modifier.padding(8.dp)
    ) {
        Text(text, color = CcpColors.ColorText, fontWeight = FontWeight.Bold)
    }
}

