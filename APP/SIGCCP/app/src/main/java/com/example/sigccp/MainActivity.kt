package com.example.sigccp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModelProvider
import com.example.sigccp.activity.clients.ui.viewmodel.ClienteViewModel
import com.example.sigccp.navigation.NavigationScreen
import com.example.sigccp.ui.theme.AppTypography
import com.example.sigccp.ui.theme.SIGCCPTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    private lateinit var clientViewModel: ClienteViewModel
    override fun onCreate(savedInstanceState: Bundle?) {
        clientViewModel = ViewModelProvider(this).get(ClienteViewModel::class.java)

        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            SIGCCPTheme {
                Surface (
                    modifier = Modifier.fillMaxSize(),
                    color = Color.Transparent
                )
                {
                    NavigationScreen(clientViewModel)
                }
            }
        }
    }
}
