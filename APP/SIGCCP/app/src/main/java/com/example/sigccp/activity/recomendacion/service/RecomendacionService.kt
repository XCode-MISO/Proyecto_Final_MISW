package com.example.sigccp.activity.recomendacion.service

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log
import android.widget.Toast
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
    /*
        Inicialmente el servicio devuelve 404, not found, entonces se realizan 10 intentos cada 5
        segundos para obtener el resultado.
        Repetimos la consulta hasta que se procese el video
    */
    private fun monitorJobStatus(id: String) {
        serviceScope.launch {
            var intentos = 0
            while (true) {
                intentos++
                val response = try {
                    RetrofitInstanceRecomendacion.apiService.getJobStatus(id)
                } catch (e: Exception) {
                    Log.e("Recomendacion Error($intentos)", e.message.toString())
                    if(intentos > 10){
                        stopSelf()
                        return@launch
                    } else {
                        delay(5_000)
                        continue
                    }
                }
                delay(10_000)

                Log.d("Recomendacion", response.toString())

                if (response.final_state == "processed") {
                    PreferencesManager.saveString(PreferenceKeys.JOB_ID, response.job_id)
                    PreferencesManager.saveString(PreferenceKeys.RECOMENDACION, response.final_recommendation)

                    NotificationHelper.showNotification(applicationContext, response.final_recommendation)

                    val intent = Intent("com.example.sigccp.SERVICE_STOPPED")
                    sendBroadcast(intent)
                    stopSelf()
                    break
                } else {
                    delay(10_000)
                }
            }
        }
    }




    override fun onDestroy() {
        serviceScope.cancel()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
