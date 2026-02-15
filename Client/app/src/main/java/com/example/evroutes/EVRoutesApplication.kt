package com.example.evroutes

import android.app.Application
import com.yandex.mapkit.MapKitFactory

class EVRoutesApplication : Application() {

    companion object {
        private const val MAPKIT_API_KEY = "b328cf2c-247b-45e8-8013-9ecd243b7671"
    }

    override fun onCreate() {
        super.onCreate()
        MapKitFactory.setApiKey(MAPKIT_API_KEY)
        MapKitFactory.initialize(this)
    }
}