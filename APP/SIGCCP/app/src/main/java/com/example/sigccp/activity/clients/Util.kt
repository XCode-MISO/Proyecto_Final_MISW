package com.example.sigccp.activity.clients

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import com.example.sigccp.ui.theme.CcpColors

@Composable
fun BaseScreen(content: @Composable () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.verticalGradient(
                    colors = listOf(CcpColors.GradientStart, CcpColors.GradientEnd)
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

@Composable
fun ScreenContainer(
    title: String,
    content: @Composable ColumnScope.() -> Unit
) {
    BaseScreen {
        Scaffold(
            topBar = { AppTopBar(title = "SIGCCP") },
            containerColor = Color.Transparent
        ) { paddingValues ->
            Column(
                modifier = Modifier
                    .padding(paddingValues)
                    .fillMaxSize(),
                horizontalAlignment = Alignment.CenterHorizontally
            ){
                Text(
                    text = title,
                    fontWeight = FontWeight.Bold,
                    fontSize = 24.sp,
                    modifier = Modifier.padding(16.dp)
                )
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

