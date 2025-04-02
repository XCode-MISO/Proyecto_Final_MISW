package com.example.sigccp.ui.View

import android.provider.CalendarContract.Colors
import android.view.Menu
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.PowerSettingsNew
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults.topAppBarColors
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.example.sigccp.R
import com.example.sigccp.activity.menu.UI.View.newButton
import com.example.sigccp.activity.pedido.Data.Modelo.ClienteClass
import com.example.sigccp.activity.pedido.Data.Modelo.PedidoClass
import com.example.sigccp.ui.View.Components.ClientDropdown
import com.example.sigccp.ui.View.Components.LanguageDropdown
import com.example.sigccp.ui.View.Components.PedidoBox
import com.example.sigccp.ui.View.Components.SubTitleBar
import com.example.sigccp.ui.View.Components.newMenuButton
import com.example.sigccp.ui.theme.AppTypography
import com.example.sigccp.ui.theme.MoradoApp

val clientes = listOf(
    1 to "Juan Pérez",
    2 to "María González",
    3 to "Carlos López"
)

val pedidoEjemplo = PedidoClass(
    id = "57623699-c732-44a7-808f-88580b45d84f",
    name = "Pedido especial",
    price = 150.75,
    state= "Pendiente",
    client = ClienteClass(
        id = "123e4567-e89b-12d3-a456-426614174000",
        name = "pedrito perez"
    )
)

@Preview
@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(
    //navController: NavController,
    //menu: Menu
    )
{
    Scaffold (
        topBar = {
            TopAppBar(
                colors = topAppBarColors(
                    containerColor = Color.Transparent,
                    titleContentColor = MaterialTheme.colorScheme.primary,
                ),
                title = {
                    Text(
                        modifier = Modifier.fillMaxSize()
                            .wrapContentHeight(Alignment.CenterVertically),
                        textAlign = TextAlign.Center,
                        text = "SIGCCP",
                        style = AppTypography.titleLarge
                    )
                },
                navigationIcon = {
                    IconButton(
                        onClick = {/*todo*/},
                        modifier = Modifier.padding(start = 20.dp, end = 25.dp)
                    )
                    {
                        Icon(
                            imageVector = Icons.Filled.PowerSettingsNew, contentDescription = "Salir",
                            tint = MoradoApp,
                            modifier = Modifier.size(40.dp)
                        )
                    }

                },
                actions = {
                    LanguageDropdown()
                }
            )
        }
    )
    {
        innerPadding ->
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
                        .wrapContentSize()
                        .padding(innerPadding),
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
                        SubTitleBar(
                            texto = "Hola, usuario",
                            imagen = R.drawable.avatar,
                            enabled = true
                        )
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
                        ClientDropdown(
                            clients = clientes,
                            onClientSelected = { id -> println("Cliente seleccionado: $id") }
                        )
                        PedidoBox(pedido = pedidoEjemplo)
                        newMenuButton(
                            onClick = {/*TODO*/ },
                            nombre = "CREAR CLIENTE",
                            imagen = R.drawable.editar,
                            enabled = true
                        )
                    }
                }
            }
        }
    }
}

