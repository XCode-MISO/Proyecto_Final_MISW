package com.example.sigccp

import android.app.Application
import android.content.Context
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class SIGCCPApp:Application (){
    override fun onCreate() {
        super.onCreate()
        instance = this
    }

    companion object {
        private lateinit var instance: SIGCCPApp
        fun getContext(): Context = instance.applicationContext
    }
}