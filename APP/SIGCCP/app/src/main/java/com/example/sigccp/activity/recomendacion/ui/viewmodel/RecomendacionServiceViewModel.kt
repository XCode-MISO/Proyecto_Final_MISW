package com.example.sigccp.activity.recomendacion.ui.viewmodel

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class RecomendacionServiceViewModel: ViewModel() {
    private val _jobId = MutableStateFlow("")
    val jobId: StateFlow<String> = _jobId

    private val _isServiceRunning = MutableStateFlow(false)
    val isServiceRunning: StateFlow<Boolean> = _isServiceRunning

    private val _recommendationText = MutableStateFlow("")
    val recommendationText: StateFlow<String> = _recommendationText

    fun setJobId(id: String) {
        _jobId.value = id
    }

    fun setServiceRunning(running: Boolean) {
        _isServiceRunning.value = running
    }

    fun setRecommendationText(text: String) {
        _recommendationText.value = text
    }
}