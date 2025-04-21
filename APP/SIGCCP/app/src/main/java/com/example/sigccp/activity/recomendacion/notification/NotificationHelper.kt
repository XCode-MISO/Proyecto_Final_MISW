package com.example.sigccp.activity.recomendacion.notification

import android.app.*
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import com.example.sigccp.R

object NotificationHelper {
    private const val CHANNEL_ID = "job_status_channel"
    private const val NOTIF_ID = 4001// 1 segundo = 1000

    fun createChannel(context: Context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Job Status Updates",
                NotificationManager.IMPORTANCE_HIGH
            )
            context.getSystemService(NotificationManager::class.java)?.createNotificationChannel(channel)
        }
    }

    fun showNotification(context: Context, recommendation: String) {
        val notification = NotificationCompat.Builder(context, CHANNEL_ID)
            .setContentTitle("Resultado disponible")
            .setContentText(recommendation)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setAutoCancel(true)
            .build()

        context.getSystemService(NotificationManager::class.java)
            ?.notify(NOTIF_ID, notification)
    }
}
