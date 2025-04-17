package com.example.sigccp.activity.recomendacion.ui.view

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.provider.MediaStore
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.sigccp.activity.recomendacion.ui.viewmodel.RecomendacionViewModel
import com.example.sigccp.ui.View.Components.ScreenContainer
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.getValue
import com.example.sigccp.ui.View.Components.CustomButton
import java.io.File
import java.io.FileOutputStream

object FileUtils {
    fun getFileFromUri(context: Context, uri: Uri): File {
        val inputStream = context.contentResolver.openInputStream(uri)
        val file = File(context.cacheDir, "upload_video.mp4")
        val outputStream = FileOutputStream(file)
        inputStream?.copyTo(outputStream)
        inputStream?.close()
        outputStream.close()
        return file
    }
}

@Composable
fun Recomendacion(
    viewModel: RecomendacionViewModel = viewModel()
) {
    val context = LocalContext.current
    var videoUri by remember { mutableStateOf<Uri?>(null) }
    val isLoading = viewModel.isLoading.collectAsState().value

    val pickVideoLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        videoUri = uri
        uri?.let {
            val file = FileUtils.getFileFromUri(context, it)
            viewModel.uploadVideoFile(file,
                onSuccess = {
                    Toast.makeText(
                        context,
                        "Video Cargado", Toast.LENGTH_LONG
                    ).show()
                }, onError = {msg ->
                    Toast.makeText(
                        context,
                        msg, Toast.LENGTH_LONG
                    ).show()
                }
            )
        }
    }

    val captureVideoLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        val uri = result.data?.data
        uri?.let {
            videoUri = it
            val file = FileUtils.getFileFromUri(context, it)
            viewModel.uploadVideoFile(file,
                onSuccess = {
                Toast.makeText(
                    context,
                    "Video Cargado", Toast.LENGTH_LONG
                ).show()
            }, onError = {msg ->
                    Toast.makeText(
                        context,
                        msg, Toast.LENGTH_LONG
                    ).show()
                }
            )
        }
    }

    ScreenContainer(title = "Recomendacion", false, null) {
        Column(Modifier.fillMaxSize().padding(16.dp)) {
            if (isLoading) {
                CircularProgressIndicator()
            } else {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                ) {
                    Row {
                        CustomButton("Grabar\n Video") {
                            val intent = Intent(MediaStore.ACTION_VIDEO_CAPTURE)
                            captureVideoLauncher.launch(intent)
                        }
                        CustomButton("Seleccionar\n Video"){
                            pickVideoLauncher.launch("video/*")
                        }

                    }
                }
            }
        }
    }
}