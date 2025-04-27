package com.example.sigccp.activity.recomendacion.ui.viewmodel

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch
import com.example.sigccp.activity.recomendacion.repository.RecomendacionRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import java.io.File
import okhttp3.RequestBody.Companion.asRequestBody
import org.json.JSONObject

class RecomendacionViewModel:ViewModel() {
    private val repository = RecomendacionRepository()
    private val _isLoading = MutableStateFlow(false)
    val isLoading = _isLoading.asStateFlow()

    fun uploadVideoFile(file: File, onSuccess: (String) -> Unit, onError: (String) -> Unit) {
        val maxSize = 10 * 1024 * 1024 // 10 MB
        if (file.length() > maxSize) {
            onError("El archivo es demasiado grande.")
            return
        }

        val requestFile = file.asRequestBody("video/mp4".toMediaTypeOrNull())
        val body = MultipartBody.Part.createFormData("video", file.name, requestFile)

        viewModelScope.launch {
            try {
                _isLoading.value = true
                val response = repository.uploadVideo(body)
                if (response.isSuccessful) {
                    val jsonResponse = response.body()?.string()
                    val jsonObject = JSONObject(jsonResponse.toString())
                    val jobId = jsonObject.getString("job_id")
                    onSuccess(jobId)
                } else {
                    onError("Error en envío: ${response.errorBody()?.string()}")
                }
            } catch (e: Exception) {
                onError(e.localizedMessage ?: "Error desconocido")
            } finally {
                _isLoading.value = false
            }
        }
    }
}