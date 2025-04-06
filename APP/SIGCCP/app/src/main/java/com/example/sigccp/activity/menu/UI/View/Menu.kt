package com.example.sigccp.activity.menu.UI.View

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsHoveredAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.compositeOver
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.example.sigccp.R
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.ui.View.Components.ScreenContainer
import com.example.sigccp.ui.View.Components.newMenuButton
import com.example.sigccp.ui.theme.AmarilloApp
import com.example.sigccp.ui.theme.AppTypography
import com.example.sigccp.ui.theme.VerdeApp

@Composable
fun Menu(navController: NavController)
{
    Options(navController)
}

@Composable
fun Options(navController: NavController)
{
    ScreenContainer(title = stringResource(id = R.string.menuVendedor),false,null) {
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
                        //newMenuButton(onClick = { "navController.navigate(AppScreen.CrearAlarma.route) }", nombre = "CREAR ALARMA", imagen = R.drawable.editar)
                        newMenuButton(
                            onClick = { navController.navigate(AppScreen.ListarPedidos.route) },
                            nombre = "PEDIDOS",
                            imagen = R.drawable.editar,
                            enabled = true
                        )
                        newMenuButton(
                            onClick = {navController.navigate(AppScreen.CrearCliente.route) },
                            nombre = "CREAR CLIENTE",
                            imagen = R.drawable.editar,
                            enabled = true
                        )
                        newMenuButton(
                            onClick = {/*TODO*/ },
                            nombre = "CLIENTES",
                            imagen = R.drawable.ver,
                            enabled = false
                        )
                        newMenuButton(
                            onClick = {/*TODO*/ },
                            nombre = "INVENTARIO",
                            imagen = R.drawable.ver,
                            enabled = false
                        )
                        newMenuButton(
                            onClick = {/*TODO*/ },
                            nombre = "RUTAS",
                            imagen = R.drawable.ia,
                            enabled = false
                        )
                        newMenuButton(
                            onClick = {/*TODO*/ },
                            nombre = "RECOMENDACION",
                            imagen = R.drawable.config,
                            enabled = false
                        )
                        newMenuButton(
                            onClick = { navController.navigate(AppScreen.RegistrarVisita.route) },
                            nombre = "REGISTRAR VISITA",
                            imagen = R.drawable.editar,
                            enabled = true
                        )
                    }
                }
            }
        }
    }
}
