package com.example.sigccp

import android.annotation.SuppressLint
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.sigccp.activity.clients.ui.viewmodel.ClienteViewModel
import com.example.sigccp.activity.recomendacion.ui.viewmodel.RecomendacionServiceViewModel
import com.example.sigccp.navigation.NavigationScreen
import com.example.sigccp.ui.theme.SIGCCPTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    private lateinit var viewModel: RecomendacionServiceViewModel

    private val serviceStopReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            val recommendation = PreferencesManager.getString(PreferenceKeys.RECOMENDACION, "")
            viewModel.setServiceRunning(false)
            viewModel.setRecommendationText(recommendation)
        }
    }

    @SuppressLint("UnspecifiedRegisterReceiverFlag")
    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        PreferencesManager.init(this)

        viewModel = RecomendacionServiceViewModel()
        registerReceiver(serviceStopReceiver, IntentFilter("com.example.sigccp.SERVICE_STOPPED"))

        enableEdgeToEdge()
        setContent {
            SIGCCPTheme {
                Surface (
                    modifier = Modifier.fillMaxSize(),
                    color = Color.Transparent
                )
                {
                    NavigationScreen(viewModel)
                }
            }
        }
    }

    override fun onDestroy() {
        unregisterReceiver(serviceStopReceiver)
        super.onDestroy()
    }
}
