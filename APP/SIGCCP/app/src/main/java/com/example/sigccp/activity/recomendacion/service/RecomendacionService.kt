package com.example.sigccp.activity.recomendacion.service

import android.app.Service
import android.content.Intent
import android.os.IBinder
import com.example.sigccp.PreferenceKeys
import com.example.sigccp.PreferencesManager
import com.example.sigccp.activity.recomendacion.data.network.RetrofitInstanceRecomendacion
import com.example.sigccp.activity.recomendacion.notification.NotificationHelper
import kotlinx.coroutines.*

class RecomendacionService : Service() {
    private var jobId: String? = null
    private val serviceScope = CoroutineScope(Dispatchers.IO + Job())

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        jobId = intent?.getStringExtra("job_id")
        NotificationHelper.createChannel(this)
        jobId?.let {
            monitorJobStatus(it)
        }
        return START_STICKY
    }

    private fun monitorJobStatus(id: String) {
        serviceScope.launch {
            while (true) {
                val response = try {
                    RetrofitInstanceRecomendacion.apiService.getJobStatus(id)
                } catch (e: Exception) {
                    stopSelf()
                    return@launch
                }

                if (response.final_state != "pending") {
                    PreferencesManager.saveString(PreferenceKeys.JOB_ID, response.job_id)
                    PreferencesManager.saveString(PreferenceKeys.RECOMENDACION, response.final_recommendation)

                    NotificationHelper.showNotification(applicationContext, response.final_recommendation)

                    val intent = Intent("com.example.sigccp.SERVICE_STOPPED")
                    sendBroadcast(intent)
                    stopSelf()
                    break
                }
                delay(10_000)
            }
        }
    }




    override fun onDestroy() {
        serviceScope.cancel()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
