package com.example.sigccp.activity.pedido.UI.View

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.sigccp.ui.theme.AmarilloApp
import com.example.sigccp.ui.theme.AppTypography
import com.example.sigccp.ui.theme.VerdeApp

@Preview
@Composable
fun ListarPedidos()
{
    Pedidos()
}

@Composable
fun Pedidos ()
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
        Row (
            modifier = Modifier.padding(start = 30.dp,top = 60.dp, end = 15.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        )
        {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .background(Color.Red)
            )
            {

            }
            Text(
                text = "SIGCCP",
                style = AppTypography.titleLarge
            )

            Box(
                modifier = Modifier
                    .size(80.dp, 40.dp)
                    .background(Color.Blue)
            )
            {

            }
        }
        Row (
            modifier = Modifier.padding(top = 16.dp),
        )
        {
            Text(
                modifier = Modifier.padding(top = 5.dp),
                text = "!Tus Pedidos!",
                style = AppTypography.titleSmall
            )
        }
        /*TODO*/

    }
}

@Composable
fun Pedido()
{

}