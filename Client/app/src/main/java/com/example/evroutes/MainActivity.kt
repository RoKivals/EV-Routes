package com.example.evroutes

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.*
import androidx.compose.material3.Text
import androidx.compose.foundation.layout.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.evroutes.ui.theme.EVRoutesTheme

import com.example.evroutes.data.network.RetrofitClient

import com.example.evroutes.data.repository.AuthRepository
import com.example.evroutes.ui.auth.AuthViewModel
import com.example.evroutes.ui.auth.LoginScreen
import com.example.evroutes.ui.auth.RegisterScreen

import com.example.evroutes.data.repository.MapRepository
import com.example.evroutes.ui.map.MapScreen
import com.example.evroutes.ui.map.MapViewModel

import com.yandex.mapkit.MapKitFactory

// Главная активность приложения
class MainActivity : ComponentActivity() {

    private var hasLocationPermissions = false

    // Регистрируем лаунчер для запроса разрешений
    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        val coarseGranted = permissions[Manifest.permission.ACCESS_COARSE_LOCATION] ?: false
        val fineGranted = permissions[Manifest.permission.ACCESS_FINE_LOCATION] ?: false

        hasLocationPermissions = coarseGranted || fineGranted

        if (hasLocationPermissions) {
            println("✅ Location permissions granted")
        } else {
            println("❌ Location permissions denied")
        }

        // Перезапускаем UI
        setContent {
            EVRoutesTheme {
                EVRoutesApp(hasLocationPermissions)
            }
        }
    }

    private fun checkAndRequestLocationPermissions() {
        val coarseGranted = ContextCompat.checkSelfPermission(
            this, Manifest.permission.ACCESS_COARSE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED

        val fineGranted = ContextCompat.checkSelfPermission(
            this, Manifest.permission.ACCESS_FINE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED

        hasLocationPermissions = coarseGranted || fineGranted

        if (hasLocationPermissions) {
            println("✅ Location permissions already granted")
            setContent {
                EVRoutesTheme {
                    EVRoutesApp(true)
                }
            }
        } else {
            println("⚠️ Requesting location permissions...")
            // Запрашиваем разрешения
            requestPermissionLauncher.launch(
                arrayOf(
                    Manifest.permission.ACCESS_COARSE_LOCATION,
                    Manifest.permission.ACCESS_FINE_LOCATION
                )
            )
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        MapKitFactory.initialize(this)
        checkAndRequestLocationPermissions()
    }

    override fun onStart() {
        super.onStart()

        try {
            MapKitFactory.getInstance().onStart()
        } catch (e: Exception) {
            print("Текст без переноса строки")
        }
    }

    override fun onStop() {
        try {
            MapKitFactory.getInstance().onStop()
        } catch (e: Exception) {
            print("Текст без переноса строки")
        }
        super.onStop()
    }
}

// Настройка навигации приложения
@Composable
fun EVRoutesApp(hasLocationPermissions: Boolean = false) {
    val navController = rememberNavController()

    if (!hasLocationPermissions) {
        // Показываем сообщение о необходимости разрешений
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier.padding(16.dp)
            ) {
                Text("Для работы с картами необходимо")
                Text("разрешение на доступ к местоположению")
                Spacer(modifier = Modifier.height(8.dp))
                Text("Пожалуйста, разрешите доступ в настройках")
            }
        }
        return
    }

    // Репозитории
    val authRepository = AuthRepository(RetrofitClient.authApiService)
    val mapRepository = MapRepository(RetrofitClient.mapApiService)

    // ViewModels
    val authViewModel = AuthViewModel(authRepository)
    val mapViewModel = MapViewModel(mapRepository)

    NavHost(navController = navController, startDestination = "login") {
        composable("login") {
            LoginScreen(viewModel = authViewModel, navController = navController)
        }
        composable("register") {
            RegisterScreen(viewModel = authViewModel, navController = navController)
        }
        composable("map") {
            MapScreen(navController = navController, viewModel = mapViewModel)
        }
    }
}