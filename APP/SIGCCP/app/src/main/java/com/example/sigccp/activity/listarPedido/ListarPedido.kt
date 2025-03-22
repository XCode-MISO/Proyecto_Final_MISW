package com.example.sigccp.activity.listarPedido

import android.widget.Button
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.example.sigccp.menu2.newButton
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.ui.theme.AmarilloApp
import com.example.sigccp.ui.theme.AppTypography
import com.example.sigccp.ui.theme.VerdeApp

@Composable
fun ListarPedidos(navController: NavController)
{
    Pedidos(navController)
}

@Composable
fun Pedidos (navController: NavController)
{
    Column (
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.verticalGradient(
                    colors = listOf(AmarilloApp, VerdeApp)
                )
            )
            .padding(start = 27.dp, end = 27.dp),
        verticalArrangement = Arrangement.Top,
        horizontalAlignment = Alignment.CenterHorizontally,
    )
    {
        Button(
            enabled = true,
            onClick = { navController.navigate(AppScreen.Menu.route) },
            colors = ButtonDefaults.buttonColors(
                containerColor = Color.Transparent // Hacer el botón transparente
            ),
        )
        {
            Text(text = "MENU",
                style = AppTypography.labelLarge)
        }
    }
}