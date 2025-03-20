package com.example.sigccp.menu2

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.sigccp.ui.theme.AmarilloApp
import com.example.sigccp.ui.theme.AppTypography
import com.example.sigccp.ui.theme.VerdeApp

@Preview
@Composable
fun Menu2 ()
{
    Options()
}

@Composable
fun Options() {
    Column (
        modifier = Modifier.fillMaxSize()
            .background(
                brush = Brush.verticalGradient(
                    colors = listOf(AmarilloApp, VerdeApp)
                )
            )
            .padding(start = 27.dp, end = 27.dp),
        verticalArrangement = Arrangement.Top,
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Column (
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Text(
                modifier = Modifier.padding(top = 54.dp),
                text = "SIGCCP",
                style = AppTypography.titleLarge
            )
        }
    }
}
