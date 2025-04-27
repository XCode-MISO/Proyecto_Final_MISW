package com.example.sigccp.activity.recomendacion.ui.view

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.provider.MediaStore
import android.util.Log
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Text
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
import androidx.compose.ui.res.stringResource
import com.example.sigccp.PreferencesManager
import com.example.sigccp.R
import com.example.sigccp.activity.recomendacion.service.RecomendacionService
import com.example.sigccp.activity.recomendacion.ui.viewmodel.RecomendacionServiceViewModel
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
    viewModel: RecomendacionViewModel = viewModel(),
    serviceViewModel: RecomendacionServiceViewModel = viewModel()
) {
    val context = LocalContext.current
    var videoUri by remember { mutableStateOf<Uri?>(null) }
    val isLoading = viewModel.isLoading.collectAsState().value

    val isRunning by serviceViewModel.isServiceRunning.collectAsState()
    val recommendation by serviceViewModel.recommendationText.collectAsState()

    //-------------------------------------------
    val jobId = PreferencesManager.getString("job_id")
    val textoRecomendacion = PreferencesManager.getString("final_recommendation")

    if (jobId.isNotBlank() && textoRecomendacion.isNotBlank()) {
        serviceViewModel.setJobId(jobId)
        serviceViewModel.setRecommendationText(recommendation)
    }


    //-------------------------------------------

    val pickVideoLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        videoUri = uri
        uri?.let {
            val file = FileUtils.getFileFromUri(context, it)
            viewModel.uploadVideoFile(file,
                onSuccess = {jobId ->
                    Log.d("Response", jobId)
                    Toast.makeText(
                        context,
                        "Video Cargado", Toast.LENGTH_LONG
                    ).show()
                    serviceViewModel.setJobId(jobId)
                    serviceViewModel.setServiceRunning(true)
                    serviceViewModel.setRecommendationText("")
                    startJobService(context, jobId)
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
                    serviceViewModel.setJobId(jobId)
                    serviceViewModel.setServiceRunning(true)
                    serviceViewModel.setRecommendationText("")
                    startJobService(context, jobId)

                }, onError = {msg ->
                    Toast.makeText(
                        context,
                        msg, Toast.LENGTH_LONG
                    ).show()
                }
            )
        }
    }

    ScreenContainer(title = stringResource(id = R.string.recomendation), true,false,true, null) {
        Column(Modifier.fillMaxSize().padding(16.dp)) {
            if (isLoading) {
                CircularProgressIndicator()
                Text("Cargando video...")
            } else {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                ) {
                    Column {
                        Row {
                            CustomButton("Grabar\n Video") {
                                if (isRunning) {
                                    Toast.makeText(context, "El proceso ya está en ejecución", Toast.LENGTH_SHORT).show()
                                } else {
                                    val intent = Intent(MediaStore.ACTION_VIDEO_CAPTURE)
                                    captureVideoLauncher.launch(intent)
                                }
                            }
                            CustomButton("Seleccionar\n Video") {
                                if (isRunning) {
                                    Toast.makeText(context, "El proceso ya está en ejecución", Toast.LENGTH_SHORT).show()
                                } else {
                                    pickVideoLauncher.launch("video/*")
                                }
                            }
                        }
                        if (isRunning) {
                            CircularProgressIndicator()
                            Text("Procesando recomendacion...")
                        } else if (recommendation.isNotBlank()) {
                            Text("Recomendación: $recommendation")
                        }
                    }
                }
            }
        }
    }
}

fun startJobService(context: Context, jobId: String) {
    val serviceIntent = Intent(context, RecomendacionService::class.java).apply {
        putExtra("job_id", jobId)
    }
    context.startService(serviceIntent)
}