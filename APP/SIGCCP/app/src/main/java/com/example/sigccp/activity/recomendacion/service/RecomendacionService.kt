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
        Inicialmente el servicio devuelve 404, not found, entonces se realizan 60 intentos cada 5
        segundos (durante 5 minutos) para obtener el resultado.
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
                    if(intentos > 60){
                        val finalRecommendation = "Sugerencia:\n- No se identificó una categoría clara.\n\nRecomendados:\nazucar, cerveza"

                        PreferencesManager.saveString(PreferenceKeys.JOB_ID, "0")
                        PreferencesManager.saveString(PreferenceKeys.RECOMENDACION, finalRecommendation)

                        NotificationHelper.showNotification(applicationContext, "Tiempo de espera caducado")
                        val intent = Intent("com.example.sigccp.SERVICE_STOPPED")
                        sendBroadcast(intent)
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
                    val theRecomendation =
                        if (response.final_recommendation.isEmpty())
                            "Gracias por su freferencia!"
                        else
                            response.final_recommendation
                    val recomendedProducts =
                        if (response.recommended_products.isNotEmpty())
                            response.recommended_products.joinToString(", ") { it.nombre }
                        else
                            "azucar, cerveza"
                    val finalRecommendation = "Sugerencia:\n$theRecomendation\n\nRecomendados:\n$recomendedProducts"

                    PreferencesManager.saveString(PreferenceKeys.JOB_ID, response.job_id)
                    PreferencesManager.saveString(PreferenceKeys.RECOMENDACION, finalRecommendation)

                    NotificationHelper.showNotification(applicationContext, finalRecommendation)

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
