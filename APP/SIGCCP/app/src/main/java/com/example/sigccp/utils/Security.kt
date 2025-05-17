package com.example.sigccp.utils

import com.example.sigccp.PreferenceKeys
import com.example.sigccp.PreferencesManager
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.Response
import android.os.Handler
import android.os.Looper
import android.widget.Toast
import java.io.IOException
import com.example.sigccp.SIGCCPApp
import com.example.sigccp.navigation.AppScreen
import com.example.sigccp.navigation.NavigationController

fun getOkHttpClientWithToken(): OkHttpClient {
    // Create the base OkHttpClient builder
    val builder = OkHttpClient.Builder()

    // Add the interceptor to handle the token
    builder.addInterceptor(object : Interceptor {
        @Throws(IOException::class)
        override fun intercept(chain: Interceptor.Chain): Response {
            val original = chain.request()

            val authToken = PreferencesManager.getString(PreferenceKeys.TOKEN, "")

            val requestBuilder = original.newBuilder()
                .header("Authorization", "Bearer $authToken") // Replace YOUR_AUTH_TOKEN with your actual token
                .method(original.method, original.body)

            val request = requestBuilder.build()
            return chain.proceed(request)
        }
    })

    // Add the AuthInterceptor to handle expired tokens
    builder.addInterceptor(AuthInterceptor()) // Add your expired token interceptor here

    // Build the OkHttpClient
    return builder.build()
}

fun logout() {
    PreferencesManager.clearAll()
    val mainHandler = Handler(Looper.getMainLooper())
    mainHandler.post {
        NavigationController.navigate(AppScreen.Login.route)
    }
}

class AuthInterceptor() : Interceptor {

    @Throws(IOException::class)
    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        val response = chain.proceed(originalRequest)

        if (response.code == 401 || response.code == 403) {
            val appContext = SIGCCPApp.getContext()

            appContext.let {
                Handler(Looper.getMainLooper()).post {
                    Toast.makeText(it, "Ingrese sus credenciales nuevamente.", Toast.LENGTH_LONG).show()
                }
            }

            logout()
        }

        return response
    }
}

